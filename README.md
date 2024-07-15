# IoMBian Remote Configurator

This service allows to configure the IoMBian device through a [remote application](https://iombian-configurator.web.app/) (based on Firebase).


## Installation

- Define project name in an environment variable:

> ```PROJECT_NAME=iombian-remote-configurator```

- Clone the repo into a temp folder:

> ```git clone https://github.com/Tknika/${PROJECT_NAME}.git /tmp/${PROJECT_NAME} && cd /tmp/${PROJECT_NAME}```

- Create the installation folder and move the appropiate files (edit the user):

> ```sudo mkdir /opt/${PROJECT_NAME}```

> ```sudo cp requirements.txt /opt/${PROJECT_NAME}```

> ```sudo cp -r src/* /opt/${PROJECT_NAME}```

> ```sudo cp systemd/${PROJECT_NAME}.service /etc/systemd/system/```

> ```sudo chown -R iompi:iompi /opt/${PROJECT_NAME}```

- Create the virtual environment and install the dependencies:

> ```cd /opt/${PROJECT_NAME}```

> ```python3 -m venv venv```

> ```source venv/bin/activate```

> ```pip install --upgrade pip```

> ```pip install -r requirements.txt```

- Start the script

> ```sudo systemctl enable ${PROJECT_NAME}.service && sudo systemctl start ${PROJECT_NAME}.service```

## Docker

To build the docker image, from the cloned repository, execute the `docker build` command in the same level as the Dockerfile.
In this case replace the variables like `${IMAGE_NAME}` with a value.

`docker build -t ${IMAGE_NAME}:${IMAGE_VERSION} .`

For example:
`docker build -t iombian-remote-configurator:latest .`

After building the image, execute it with docker run.

`docker run --name ${CONTAINER_NAME} -e CONFIG_HOST=127.0.0.1 -e CONFIG_PORT=5555 -e LOG_LEVEL=DEBUG iombian-remote-configurator:latest`

- **--name** is used to define the name of the created container.

- **--rm** can be used to delete the container when it stops.
This parameter is optional.

- **-d** is used to run the container detached.
This way the container will run in the background.
This parameter is optional.

- **-e** can be used to define the environment variables:
    - CONFIG_HOST: the host where the service needs to connect to send the configuration values. Default value is "127.0.0.1".
    - CONFIG_PORT: The port where the service needs to connect to send the configuration values.
    Default port is 5555.
    - LOG_LEVEL: define the log level for the python logger.
    This can be NOTSET, DEBUG, INFO, WARNING, ERROR or CRITICAL.
    Default value is INFO.


## Author

(c) 2024 [Aitor Iturrioz Rodríguez](https://github.com/bodiroga)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.