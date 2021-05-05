#!/bin/bash

docker-compose up exec app bash
python manage.py createsuperuser 
python manage.py migrate