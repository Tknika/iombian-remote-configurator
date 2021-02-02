# IoMBian Remote Configurator

This service allows to configure the IoMBian device through a [remote application](https://iombian-configurator.web.app/) (based on Firebase).


## Installation

- Clone the repo into a temp folder:

> ```git clone https://github.com/Tknika/iombian-remote-configurator.git /tmp/iombian-remote-configurator && cd /tmp/iombian-remote-configurator```

- Create the installation folder and move the appropiate files (edit the user):

> ```sudo mkdir /opt/iombian-remote-configurator```

> ```sudo cp requirements.txt /opt/iombian-remote-configurator```

> ```sudo cp -r src/* /opt/iombian-remote-configurator```

> ```sudo cp systemd/iombian-remote-configurator.service /etc/systemd/system/```

> ```sudo chown -R iompi:iompi /opt/iombian-remote-configurator```

- Create the virtual environment and install the dependencies:

> ```cd /opt/iombian-remote-configurator```

> ```python3 -m venv venv```

> ```source venv/bin/activate```

> ```pip install --upgrade pip```

> ```pip install -r requirements.txt```

- Start the script

> ```sudo systemctl enable iombian-remote-configurator.service && sudo systemctl start iombian-remote-configurator.service```


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