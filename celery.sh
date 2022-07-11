#!/bin/bash
celery -A core worker  --loglevel=info --logfile=celery.log
