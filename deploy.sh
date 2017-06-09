#!/bin/bash

export API_APPKEY=$(cat /var/www/eatpotmovie-tca-ci/appkey)

uwsgi --http 127.0.0.1:7575 --manage-script-name --mount /=manage:app --virtualenv ./venv/

exit 0
