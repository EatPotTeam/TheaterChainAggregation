#!/bin/bash

virtualenv venv

source ./venv/bin/activate

export API_APPKEY=$(cat /var/www/eatpotmovie-tca-ci/appkey)

pip3 install -r requirement.txt

exit 0
