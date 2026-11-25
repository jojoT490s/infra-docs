# GrafanaAutomation

## Overview

GrafanaAutomation is a Python-based monitoring automation project using Selenium WebDriver to log into Grafana and navigate through selected dashboards and panels across multiple Grafana instances.

It collects system metrics from selected panels, checks resource utilization against configured thresholds, records results in Google Sheets, and sends Discord notifications when conditions are detected.

## Features

- Selenium-based automated Grafana login
- Monitoring of multiple Grafana instances
- Navigation through selected dashboards and panels
- CPU utilization monitoring
- Memory utilization monitoring
- Disk and partition utilization monitoring
- Threshold-based alerts
- Google Sheets reporting
- Discord notifications

## Technologies

- Python
- Selenium WebDriver
- Firefox and GeckoDriver
- Grafana
- Google Sheets API
- Discord Webhooks
- Ansible
- Linux

## Workflow

1. Selenium logs into configured Grafana instances.
2. The automation navigates selected dashboards and panels.
3. It collects selected system health metrics.
4. Metrics are checked against configured thresholds.
5. Results are recorded in Google Sheets.
6. Discord notifications are sent when configured thresholds are exceeded.

## Security

Credentials, API tokens, passwords, Discord webhooks, Google service-account files, and sensitive infrastructure configuration must not be committed to version control.

Sensitive configuration files should be excluded through `.gitignore`.

## Purpose

This project demonstrates infrastructure monitoring automation, browser automation, multi-instance monitoring, metric collection, threshold-based alerting, spreadsheet reporting, and notification integrations.
