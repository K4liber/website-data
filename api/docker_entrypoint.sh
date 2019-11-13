#!/bin/bash

set -e

exec python ./flaskapi/worker.py &
exec python ./flaskapi/run.py