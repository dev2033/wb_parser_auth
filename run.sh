#!/bin/bash

. env/bin/activate
# shellcheck disable=SC2164
cd src/
uvicorn web_service:app --reload
exit