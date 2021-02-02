#!/usr/bin/env python3

from iombian_firestore_handler import IoMBianFirestoreHandler
import logging

logger = logging.getLogger(__name__)


class IoMBianRemoteConfiguratorHandler(object):

    def __init__(self, config_handler):
        self.config_handler = config_handler
        self.db_handler = None
        self.initialized = True
        self.api_key = None
        self.project_id = None
        self.refresh_token = None
        self.device_id = None

    def start(self):
        logger.debug("Starting IoMBian Remote Configurator Handler")
        self.api_key = self.config_handler.execute_command("get_api_key")
        self.project_id = self.config_handler.execute_command("get_project_id")
        self.refresh_token = self.config_handler.execute_command("get_refresh_token")
        self.device_id = self.config_handler.execute_command("get_device_id")

        if not self.api_key or not self.project_id or not self.refresh_token:
            logger.error("'parameters.yml' file does not contain remote credentials")
            self.stop()
            return

        self.db_handler = IoMBianFirestoreHandler(self.api_key, self.project_id, self.refresh_token, self.device_id)
        self.db_handler.on_device_update(self.device_handler)
        self.db_handler.initialize_db()

    def stop(self):
        logger.debug("Stopping IoMBian Remote Configurator Handler")
        if self.db_handler:
            self.db_handler.stop_db()

    def compare_configs(self, local_config, cloud_config):
        local_config_date = local_config.get("config_date", "2000-01-01T00:00:00")
        cloud_config_date = cloud_config.get("config_date")

        if not cloud_config_date:
            logger.error("Invalid cloud configuration!")
            return

        if cloud_config_date == local_config_date:
            logger.info(f"Both configs are equal, nothing has changed ({local_config_date})")
        elif cloud_config_date > local_config_date:
            logger.info("There is a new configuration in the cloud")
            self.config_handler.execute_command("save_config", cloud_config)
        elif cloud_config_date < local_config_date:
            logger.warn("The cloud config is old, uploading the local one")
            self.db_handler.upload_config(local_config)

    def get_last_cloud_config(self, device_snapshot):
        device_configurations = device_snapshot[-1].to_dict().get("parameters", {})
        if not device_configurations: return {}
        last_configuration_key = sorted(device_configurations.keys())[-1]
        last_configuration = device_configurations.get(last_configuration_key, {})
        return last_configuration

    def device_handler(self, doc_snapshot, changes, read_time):
        if not doc_snapshot:
            logger.error(f"Device '{self.device_id}' does not exit in the cloud")
        else:
            cloud_config = self.get_last_cloud_config(doc_snapshot)
            local_config = self.config_handler.execute_command("get_config")
            if not cloud_config:
                logger.warn("No configuration available in the cloud, uploading the local one")
                self.db_handler.upload_config(local_config)
            else:
                self.compare_configs(local_config, cloud_config)