FROM sbrumley/opendxl

RUN apt-get update
RUN apt-get install -y git

ADD scripts/common.sh scripts/common.sh
ADD scripts/bootstrap.sh scripts/bootstrap.sh
ADD scripts/service.sh scripts/service.sh
ADD tests/ tests/

ADD opendxl_web_api.py opendxl_web_api.py

RUN /scripts/bootstrap.sh
