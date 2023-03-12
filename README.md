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


## Author

(c) 2021 [Aitor Iturrioz Rodríguez](https://github.com/bodiroga)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.