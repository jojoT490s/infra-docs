# INSTALL ANSIBLE

```bash
sudo apt update
sudo apt install -y ansible
```
# Verify
```bash
 ansible --version
```
# Create an inventory to manage local machine
```bash
nano inventory.ini
```
# Add the followin to it:
```bash
[prometheus]
localhost ansible_connection=local
```
# Create a prometheus playbook
```bash
nano install-prometheus.yml
```
# add to the config file:
```bash
---
- name: Install Prometheus
  hosts: prometheus
  become: yes

  vars:
    prometheus_version: "2.53.0"

  tasks:

    - name: Update apt cache
      apt:
        update_cache: yes

    - name: Install required packages
      apt:
        name:
          - wget
          - tar
        state: present

    - name: Create Prometheus user
      user:
        name: prometheus
        shell: /usr/sbin/nologin
        system: yes

    - name: Create directories
      file:
        path: "{{ item }}"
        state: directory
        owner: prometheus
        group: prometheus
        mode: '0755'
      loop:
        - /etc/prometheus
        - /var/lib/prometheus

    - name: Download Prometheus
      get_url:
        url: "https://github.com/prometheus/prometheus/releases/download/v{{ prometheus_version }}/prometheus-{{ prometheus_version }}.linux-amd64.tar.gz"
        dest: /tmp/prometheus.tar.gz

    - name: Extract Prometheus
      unarchive:
        src: /tmp/prometheus.tar.gz
        dest: /tmp
        remote_src: yes

    - name: Copy Prometheus binary
      copy:
        src: "/tmp/prometheus-{{ prometheus_version }}.linux-amd64/prometheus"
        dest: /usr/local/bin/prometheus
        mode: '0755'
        remote_src: yes

    - name: Copy promtool
      copy:
        src: "/tmp/prometheus-{{ prometheus_version }}.linux-amd64/promtool"
        dest: /usr/local/bin/promtool
        mode: '0755'
        remote_src: yes

    - name: Copy configuration
      copy:
        src: "/tmp/prometheus-{{ prometheus_version }}.linux-amd64/prometheus.yml"
        dest: /etc/prometheus/prometheus.yml
        remote_src: yes

    - name: Create systemd service
      copy:
        dest: /etc/systemd/system/prometheus.service
        content: |
          [Unit]
          Description=Prometheus
          Wants=network-online.target
          After=network-online.target

          [Service]
          User=prometheus
          Group=prometheus

          ExecStart=/usr/local/bin/prometheus \
            --config.file=/etc/prometheus/prometheus.yml \
            --storage.tsdb.path=/var/lib/prometheus

          Restart=always

          [Install]
          WantedBy=multi-user.target

    - name: Reload systemd
      systemd:
        daemon_reload: yes

    - name: Enable Prometheus
      systemd:
        name: prometheus
        enabled: yes
        state: started
```
# Test ansible connectivity
```bash
ansible all -i inventory.ini -m ping
```
# Run the playbook
```bash
ansible-playbook -i inventory.ini install-prometheus.yml
```
#  verify
```bash
sudo systemctl status prometheus
curl http://localhost:9090
```
#  Open in browser
```bash
http://SERVER_IP:9090
```

# REDIRECT PROMETHEUS TO PORT 443
# Open haproxy config
```bash
sudo nano /etc/haproxy/haproxy.cfg
```
# Make sure it looks like this
```bash
frontend web-frontend
    bind *:80
    bind *:443 ssl crt /etc/haproxy/certs/haproxy.pem

    redirect scheme https if !{ ssl_fc }
    
    default_backend prometheus



backend web-backend
    balance roundrobin
    server web1 192.168.84.54:8080 check

backend prometheus
    mode http
    server prom1 192.168.84.54:9090 check

```
# Validate  config file
```bash
sudo haproxy -c -f /etc/haproxy/haproxy.cfg
```
# Check status
```bash
sudo systemctl status haproxy
```
# Open ui on
```bash
https://192.168.84.54/
```

# SET UP PROMETHEUS TO MONITOR HAPROXY AND THE LINUX VM.
#Download node -exporter
```bash
cd /tmp

wget https://github.com/prometheus/node_exporter/releases/download/v1.9.1/node_exporter-1.9.1.linux-amd64.tar.gz
```
# Extract
```bash
tar -xzf node_exporter-1.9.1.linux-amd64.tar.gz
```
# Install binary and give permissions
```bash
sudo cp node_exporter-1.9.1.linux-amd64/node_exporter /usr/local/bin/
sudo chmod +x /usr/local/bin/node_exporter
```
# Verify installation
```bash
node_exporter --version
```
# Start it on one terminal
```bash
node_exporter
```
# On another run
```bash
curl http://192.168.84.54:9100/metrics
```
# Enable haproxy metrics 
# Open haproxy config
```bash
sudo nano /etc/haproxy/haproxy.cfg
```
# Add the following:
```bash
listen stats
    bind *:8404
    mode http
    stats enable
    stats uri /stats
    http-request use-service prometheus-exporter if { path /metrics }
```
# Restart haproxy
```bash
sudo systemctl restart haproxy
```
# Curl
```bash
curl http://192.168.84.54:8404/metrics
```
# Configure prometheus 
```bash
sudo nano /etc/prometheus/prometheus.yml
```
# Add the following lines below:
```bash
- job_name: "node"

static_configs:
- targets:
- "localhost:9100"

- job_name: "haproxy"

metrics_path: /metrics

static_configs:
- targets:
- "localhost:8404"
```
# Check on targets in ui
```bash
https://192.168.84.54/targets
```
# They should be up



