# Build Development Environment

[Prerequisites](Prerequisites.md)

## Build In Vagrant

1. git clone https://github.com/scottbrumley/opendxl_web_api
2. cd opendxl_web_api/
3. ./vssh.sh (On Windows Launch from Git Bash)
4. cd /vagrant
5. Copy broker certificates to brokercerts/ directory
6. Copy client certificates to the certs/ directory
7. Copy dxlclient.config to your / root directory
8. Configure your monitor.config for DXL Monitoring Service

## Run
* /vagrant/scripts/service.sh **start** (other options **stop** and **status**)

## Test
* **Automated Tests:** /vagrant/tests/urltests.sh (Runs all tests that run on start)
* **Manual Test:** Connect http://127.0.0.1:5000/about?token=<security token> to Test


## Default Security Token
**Please Change:**
27612211994137900087

"Lives in the function called authenticate"

