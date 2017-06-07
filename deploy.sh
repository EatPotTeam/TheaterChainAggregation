#!/bin/bash

uwsgi --http 127.0.0.1:7575 --manage-script-name --mount /=manage:app

exit 0
