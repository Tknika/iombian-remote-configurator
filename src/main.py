#!/usr/bin/env python3

import logging
import signal

from communication_module import CommunicationModule
from firestore_parameters_handler import FirestoreParametersHandler

logging.basicConfig(format='%(asctime)s %(levelname)-8s - %(name)-16s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def stop():
    logger.info("Stopping IoMBian Remote Configurator Service")
    if firestore_parameters_handler: firestore_parameters_handler.stop()
    if comm_module: comm_module.stop()


def signal_handler(sig, frame):
    stop()


def on_firestore_parameters_update(firestore_config):
    local_config = comm_module.execute_command("get_config")
    if not firestore_config:
        logger.warning("No configuration available in the cloud, uploading the local one")
        firestore_parameters_handler.upload_config(local_config)
        return
    
    local_config_date = local_config.get("config_date", "2000-01-01T00:00:00")
    firestore_config_date = firestore_config.get("config_date")

    if not firestore_config_date:
        logger.error("Invalid cloud configuration!")
        return

    if firestore_config_date == local_config_date:
        logger.info(f"Both configs are equal, nothing has changed ({local_config_date})")
    elif firestore_config_date > local_config_date:
        logger.info("There is a new configuration in the cloud, saving it locally")
        comm_module.execute_command("save_config", firestore_config)
    elif firestore_config_date < local_config_date:
        logger.warning("The cloud config is old, uploading the local one")
        firestore_parameters_handler.upload_config(local_config)    


if __name__ == "__main__":
    logger.info("Starting IoMBian Remote Configurator Service")

    comm_module, firestore_parameters_handler = None, None

    comm_module = CommunicationModule(host="127.0.0.1", port=5555)
    comm_module.start()

    api_key = comm_module.execute_command("get_api_key")
    project_id = comm_module.execute_command("get_project_id")
    refresh_token = comm_module.execute_command("get_refresh_token")
    device_id = comm_module.execute_command("get_device_id")

    firestore_parameters_handler = FirestoreParametersHandler(api_key, project_id, refresh_token, device_id, on_firestore_parameters_update)
    firestore_parameters_handler.start()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.pause()