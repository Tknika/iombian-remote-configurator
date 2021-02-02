#!/usr/bin/env python3

import logging
import signal

from communication_module import CommunicationModule
from iombian_remote_configurator_handler import IoMBianRemoteConfiguratorHandler

logging.basicConfig(format='%(asctime)s %(levelname)-8s - %(name)-16s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def signal_handler(sig, frame):
    logger.info("Stopping IoMBian Remote Configurator Service")
    remote_configurator_handler.stop()
    comm_module.stop()


if __name__ == "__main__":
    logger.info("Starting IoMBian Remote Configurator Service")

    comm_module = CommunicationModule(host="127.0.0.1", port=5555)
    comm_module.start()

    remote_configurator_handler = IoMBianRemoteConfiguratorHandler(comm_module)
    remote_configurator_handler.start()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.pause()