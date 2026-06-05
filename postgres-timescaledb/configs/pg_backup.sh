#!/bin/bash

DATE=$(date +%F_%H-%M-%S)

pg_dump -U postgres metricsdb > /var/backups/postgresql/metricsdb_$DATE.sql
