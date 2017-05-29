# OpenDXL Web API

The OpenDXL Web API was designed to allow the building of a scalable web tier.  The Web API can easily allow a single host to run the API or clusters in a cloud environment such as AWS, Google, or Apache Mesos.  

## Challenges To Solve
* **Lack of Python Support:**

     Many vendors allow automation from their equipment, but this support is often limited to technologies such as syslog, snmp, or URL POST/GET.
*  **Certificate Spread:**

     Certificate based authentication management and security can be a challenge as certficates become spread across and enterprise with each new deployment.  A couple of the problems this often causes in operations are:
            
    1. **Certificate Mismatch**
    
        Certificates are deployed with a fire and forget mindset.  The trouble occurs when certificates are reissued.  Typically there is no way to track clients that are using the original certificate.   
    2. **Outdated Certificates**
    
        Clients using certificates are a challenge for operations to track therefore they will use the original certificate and never reissue certificates.
* **Wrapper Services**
    While building a wrapper is a fine work around, it creates an operational challenge because it has to be maintained in tandem to the code being wrapped.  These types of services are easily forgotten upon upgrades.  Specifically to creater of Cuckoo said please do not create wrapper.

## Architecture
![Web API](docs/images/webapi.png)

### Horizontal Scaling Criteria
* **Scalable** - Ability to add new instances of this project to increase performance.
* **Composable** - resources are logically pooled so administrators do not have to physically configure hardware.
* **Autonomous** - The project code should be able to stand on its own without dependencies

## Use Cases
* Cuckoo Notification set TIE reputation with GET request (Using Generic Set)
* FireEye Notification set set TIE reputation with POST JSON
* Generic set TIE reputation with GET request
* Generic get TIE reputation with GET request
* Real-Time DXL Bus Monitoring

## Features
* Token Authentication
* Scalable Web API Tier
* Automated Build Development Environment
* Automated Deployment
* Set TIE file Reputation from HTTP
* Get TIE file Reputation from HTTP
* Set TIE file Reputation from FireEye Notification

## Build Development Environment / Deploy To Production

How to perform the automated build for this project.  As well as how to deploy the code into a remote production system or test system.

[Build / Run Documentation](docs/build.md)

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


### LICENSE
Copyright 2017 McAfee, Inc.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.