# OpenDXL Web API

The OpenDXL Web API was designed to allow the building of a scalable web tier.  The Web API can easily allow a single host to run the API or clusters in a cloud environment such as AWS, Google, or Apache Mesos.  

The OpenDXL Web API supports running in a "standalone" mode as well as execution within a "Vagrant portable development environment". The steps for running in each of these modes are detailed below.

## Architecture
![Web API](docs/images/webapi.png)

List of Challenges can be found [here](docs/challenges.md)<br>
Pre-requisites can be found [here](docs/Prerequisites.md)

### Horizontal Scaling Criteria
* **Scalable** - Ability to add new instances of this project to increase performance.
* **Composable** - resources are logically pooled so administrators do not have to physically configure hardware.
* **Autonomous** - The project code should be able to stand on its own without dependencies

## Use Cases
* Cuckoo Notification set TIE reputation with GET request (Using Generic Set)
* FireEye Notification set set TIE reputation with POST JSON
* Generic set TIE reputation with GET request
* Generic get TIE reputation with GET request
* Real-Time DXL Bus Monitoring [Instructions](docs/dxlmonitoring.md)

## Features
* Token Authentication
* Scalable Web API Tier
* Automated Build Development Environment
* Automated Deployment
* Set TIE file Reputation from HTTP
* Get TIE file Reputation from HTTP
* Set TIE file Reputation from FireEye Notification
* Streaming Monitoring Service for DXL Messages

## Usage (Standalone)

List of Challenges can be found [here](docs/challenges.md)<br>
Pre-requisites can be found [here](docs/Prerequisites.md)

The following steps walk through running the OpenDXL Slack/TIE integration in standalone mode:

* Download the latest release of the OpenDXL WebAPI release
* Extract the downloaded release
* Provision the files necessary for an OpenDXL client (dxlclient.config and related certificate files).
    The steps are identical to those described in the OpenDXL Client [Samples Configuration](https://opendxl.github.io/opendxl-client-python/pydoc/sampleconfig.html) documentation.
* Place the dxlclient.config and related certificate files into the same directory as the opendxl_web_api.py file (in the extracted release)
* Install the required Python dependencies using the requirements.txt in the release:
    pip install -r requirements.txt
        
    If the above command fails on any of the following, you can navigate to the associated link, download the release, and install the library manually:
    - dxltieclient - https://github.com/opendxl/opendxl-tie-client-python
    - dxlmarclient - https://github.com/opendxl/opendxl-mar-client-python
    - dxlepoclient - https://github.com/opendxl/opendxl-epo-client-python

* Run the opendxl_web_api.py file using python:
    python opendxl_web_api.py
* When you see the following confirmation, the server is now ready to receive HTTP requests: 
![Output Example](docs/images/standalone-run.png)  

* To verify the server is operational, you may try accessing the "About" page on the localhost.
    http://127.0.0.1:5000/about?token=27612211994137900087

* If you have the OpenDXL Tie Client library installed ("dxltieclient"), you can try checking file reputation by SHA1 Hash
    http://127.0.0.1:5000/tie/getfile/?sha1=D4186881780D48BF55D4D59171B115634E3C7BA6&token=27612211994137900087
    
    ![Sample Tie Reputation](docs/images/sample-tie-rep.png)  

* For more information about available commands, see the [API Taxonomy](docs/taxonomy.md)

## Usage (Docker)
[Quick Start](docs/quickstart.md)

## Development, Build, Deploy 

### Build Your Development Environment
If you are interested in coding then this will build your Development Environment in a virtual machine using Vagrant.
[Build Development](docs/dev.md)

### Deploy Using Docker To Production
For a portable environment free of dependencies Docker is a good choice.
[Deploy Docker](docs/dockerdeploy.md)

### Deploy Using Docker Swarm To Production
For a self-healing fault-tolerant environment Docker Swarm is a simple choice.
[Deploy Docker Swarm](docs/dockerswarm.md)


## SSL Encryption
The best way to enable SSL encryption is through an external load balancers (nginx, haproxy, Netscalers, or F5).  The load balancer can terminate the SSL encryption from the client.  This allows the backend to remain free and composable.

## TAXONOMY Of API

Taxonomy of the API is documented in the taxonomy documentation.  This highlights how the web api paths are structured and how it should be going forward.

[Taxonomy Documentation](docs/taxonomy.md)

### McAfee Trust Level Defined
[McAfee Trust Levels](docs/trustlevels.md)

## Vendor Support
### Cuckoo

#### Configuration Examples
[Cuckoo Notification Configuration](docs/cuckoo.md)

### FireEye

#### Configuration Example
[FireEye Notification Configuration](docs/fireeye.md)


## More Documentation
For more on the technologies used in this project see.
[Miscellaneous](docs/misc.md)

### LICENSE
Copyright 2017 McAfee, Inc.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
