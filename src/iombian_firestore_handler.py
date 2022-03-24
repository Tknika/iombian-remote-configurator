#!/usr/bin/env python3

from datetime import datetime
from firestore_handler import FirestoreHandler
import logging
import time

logger = logging.getLogger(__name__)


class IoMBianFirestoreHandler(FirestoreHandler):

    KEYWORD = "parameters"

    def __init__(self, api_key, project_id, refresh_token, device_id):
        super().__init__(api_key, project_id, refresh_token, self.__on_expired_token)
        self.device_id = device_id
        self.devices_path = None
        self.telemetry_path = None
        self.device_update_callback = None
        self.device_snapshot = None

    def initialize_db(self):
        super().initialize_db()
        if not self.db:
            logger.error("DB connection not ready")
            return
        self.devices_path = f"users/{self.user_id}/devices"
        self.db.collection(self.devices_path).document(self.device_id).update({"last_connection": int(time.time())})
        self.db.collection(self.devices_path).document(self.device_id).update({"connected": True})
        if not self.device_snapshot:
            self.device_snapshot = self.db.collection(self.devices_path).document(self.device_id).on_snapshot(self.device_update_callback)

    def stop_db(self):
        self.db.collection(self.devices_path).document(self.device_id).update({"connected": False})
        super().stop_db()

    def upload_config(self, config):
        config_date = config.get("config_date")
        if not config_date:
            config_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        config.update({"config_date": config_date})
        self.add_parameters(config, config_date)

    def create_device(self):
        if not self.db:
            self.initialize_db()
        initial_data = { "creation_date": datetime.now().strftime("%Y/%m/%dT%H:%M:%S"), "last_connection": 0, self.KEYWORD: {} }
        self.db.collection(self.devices_path).add(initial_data, self.device_id)

    def add_parameters(self, parameters_value, parameters_key):
        if not self.db:
            self.initialize_db()
        updated_field = { f"{self.KEYWORD}.{parameters_key}" : parameters_value }
        self.db.collection(self.devices_path).document(self.device_id).update(updated_field)

    def on_device_update(self, callback):
        self.device_update_callback = callback

    def __on_expired_token(self):
        logger.debug("Refreshing Token Id")
        if self.device_snapshot:
            self.device_snapshot.unsubscribe()
            self.device_snapshot = None
        self.db = None
        self.initialize_db()