FROM sbrumley/opendxl:0.1.1

RUN apk add --no-cache bash wget

ADD scripts/common.sh scripts/common.sh
ADD scripts/bootstrap.sh scripts/bootstrap.sh
ADD scripts/service.sh scripts/service.sh
ADD scripts/vars.sh scripts/vars.sh
ADD templates/ templates/
ADD tests/ tests/
ADD opendxl-tie-client-python/ opendxl-tie-client-python/

##  MY code
ADD opendxl_web_api.py opendxl_web_api.py

### Python Common
RUN echo "Installing Python Common"
RUN pip install common

RUN pip install Flask
## Setup Flask Environment
ENV FLASK_APP=/opendxl_web_api.py

### Install Open DXL TIE Client
RUN echo "Installing Open DXL TIE Client"
RUN cd / && cd /opendxl-tie-client-python && python setup.py install

CMD /scripts/service.sh start

