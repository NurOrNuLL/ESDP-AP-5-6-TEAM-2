#!/bin/bash
celery -A core worker --loglevel=DEBUG
