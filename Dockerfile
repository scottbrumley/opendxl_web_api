FROM sbrumley/opendxl

RUN apt-get update
RUN apt-get install -y git

ADD brokercerts/ brokdercerts/
ADD certs/ certs/
ADD dxlclient.config dxlclient.config

ADD scripts/vars.sh scripts/vars.sh
ADD scripts/common.sh scripts/common.sh
ADD scripts/bootstrap.sh scripts/bootstrap.sh

RUN scripts/bootstrap.sh
