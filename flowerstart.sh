#!/bin/bash

sleep 3 
cd src
celery  -A core flower --address=0.0.0.0 --port=${FLOWER_PORT}