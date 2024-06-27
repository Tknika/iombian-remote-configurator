#!/usr/bin/env python3

from datetime import datetime
from firestore_client_handler import FirestoreClientHandler
import logging
import threading

logger = logging.getLogger(__name__)


class FirestoreParametersHandler(FirestoreClientHandler):

    KEYWORD = "parameters"
    RESTART_DELAY_TIME_S = 0.5

    def __init__(self, api_key, project_id, refresh_token, device_id, parameters_update_callback=lambda _: None):
        super().__init__(api_key, project_id, refresh_token)
        self.device_id = device_id
        self.parameters_update_callback = parameters_update_callback
        self.devices_path = None
        self.device_update_callback = None
        self.device_subscription = None

    def start(self):
        logger.debug("Starting Firestore Parameters Handler")
        self.initialize_client()

    def stop(self):
        logger.debug("Stopping Firestore Parameters Handler")
        try:
            self.client.collection(self.devices_path).document(self.device_id).update({"connected": False}, timeout=2)
        except Exception as e:
            pass
        if self.device_subscription:
            self.device_subscription.unsubscribe()
            self.device_subscription = None
        self.stop_client()

    def restart(self):
        logger.debug("Restarting Firestore Parameters Handler")
        self.stop()
        self.start()

    def on_client_initialized(self):
        logger.info("Firestore client initialized")
        self.devices_path = f"users/{self.user_id}/devices"
        self.client.collection(self.devices_path).document(self.device_id).update({"last_connection": int(int(datetime.now().timestamp()))}, timeout=2)
        self.client.collection(self.devices_path).document(self.device_id).update({"connected": True}, timeout=2)
        if self.device_subscription:
            return
        self.device_subscription = self.client.collection(self.devices_path).document(self.device_id).on_snapshot(self._on_device_update)

    def on_server_not_responding(self):
        logger.error("Firestore server not responding")
        threading.Timer(self.RESTART_DELAY_TIME_S, self.restart).start()

    def on_token_expired(self):
        logger.debug("Refreshing Firebase client token id")
        threading.Timer(self.RESTART_DELAY_TIME_S, self.restart).start()

    def upload_config(self, config):
        config_date = config.get("config_date")
        if not config_date:
            config_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            config.update({"config_date": config_date})

        for key, value in config.items():
            self.add_parameters(value, key)

    def create_device(self):
        self.initialize_client(notify=False)
        if not self.client:
            logger.debug("Firebase client not ready, cannot create device")
            return
        initial_data = { "creation_date": datetime.now().strftime("%Y/%m/%dT%H:%M:%S"), "last_connection": 0, self.KEYWORD: {} }
        try:
            self.client.collection(self.devices_path).add(initial_data, self.device_id, timeout=2)
        except Exception as e:
            logger.error("Firebase client error, restart the handler")
            threading.Timer(self.RESTART_DELAY_TIME_S, self.restart).start()

    def add_parameters(self, parameters_value, parameters_key):
        self.initialize_client(notify=False)
        if not self.client:
            logger.debug("Firebase client not ready, add new parameters configuration")
            return
        updated_field = { f"{self.KEYWORD}.{parameters_key}" : parameters_value }
        try:
            self.client.collection(self.devices_path).document(self.device_id).update(updated_field, timeout=2)
        except Exception as e:
            logger.error("Firebase client error, restart the handler")
            threading.Timer(self.RESTART_DELAY_TIME_S, self.restart).start()

    def _on_device_update(self, document_snapshot, changes, read_time):
        if len(document_snapshot) != 1:
            return
        device_info = document_snapshot[0].to_dict()

        cloud_config = self._filter_last_configuration(document_snapshot)

        threading.Thread(target=self.parameters_update_callback, args=[cloud_config]).start()

    def _filter_last_configuration(self, device_snapshot):
        device_configurations = device_snapshot[-1].to_dict().get(self.KEYWORD, {})
        if not device_configurations: return {}
        last_configuration_key = sorted(device_configurations.keys())[-1]
        last_configuration = device_configurations.get(last_configuration_key, {})
        return last_configuration
