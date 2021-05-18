#!/bin/bash

python /home/psiweb/Docker/jupyter_pass.py
cd /home/CORHEL_Kamodo/ && mkdocs serve -a 0.0.0.0:8000 &
jupyter notebook ${JUPYTER_NOTEBOOKS} --port=${JUPYTER_PORT} --no-browser --ip=0.0.0.0 --allow-root

