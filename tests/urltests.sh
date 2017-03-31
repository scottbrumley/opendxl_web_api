#!/usr/bin/env bash

wget 'http://127.0.0.1:5000/tie/getfile/?sha1=D4186881780D48BF55D4D59171B115634E3C7BA6&json=true' -O - >> hi.json
wget 'http://127.0.0.1:5000/tie/getfile/?sha256=2859635FEBCC5C38470828DAAECFF49179716ADDFC5AD9FADEB89722842B381A&json=true' -O - >> hi.json
wget 'http://127.0.0.1:5000/tie/getfile/?md5=836E935C5539ED23FAD863CB823C0A8A&json=true' -O - >> hi.json


wget --spider -O - -S "http://127.0.0.1:5000/about" 2>&1 | grep "HTTP/" | awk '{print $2}'