#PATRONI + HA CLUSTER

# INSTALLATION

# Postgres installation
```bash
sudo apt update
sudo apt install -y postgresql-common
sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh

sudo apt update
sudo apt install -y postgresql postgresql-contrib

Stop postgres:
sudo systemctl stop postgresql
sudo systemctl disable postgresql
```
# Install etcd
```bash
sudo apt update
sudo apt-get install -y wget curl
 
#Install  latest release:
```bash
wget https://github.com/etcd-io/etcd/releases/download/v3.5.17/etcd-v3.5.17-linux-amd64.tar.gz
```
# Uncompress and rename.
```bash
tar xvf etcd-v3.5.17-linux-amd64.tar.gz
mv etcd-v3.5.17-linux-amd64 etcd
```

# Move all binaries into /usr/local/bin/ for later use.:
```bash
sudo mv etcd/etcd* /usr/local/bin/
```
# Check version:
```bash
etcd --version
```
# Let’s create a user for etcd service:
```bash
sudo useradd --system --home /var/lib/etcd --shell /bin/false etcd
```

# Let’s configure etcd.
# Make dir and edit file.
```bash
sudo mkdir -p /etc/etcd
sudo mkdir -p /etc/etcd/ssl
```
# ON YOUR MACHINE
# Make sure openssl is installed
```bash
sudo apt install openssl
```
# Generate and configure  certs:
```bash
mkdir certs
cd certs
```
# Generate certs authority:
```bash
openssl genrsa -out ca.key 2048
openssl req -x509 -new -nodes -key ca.key -subj "/CN=etcd-ca" -days 7300 -out ca.crt
openssl genrsa -out etcd-node1.key 2048
```
# Create temp file for config
```bash
cat > temp.cnf <<EOF
[ req ]
distinguished_name = req_distinguished_name
req_extensions = v3_req
[ req_distinguished_name ]
[ v3_req ]
subjectAltName = @alt_names
[ alt_names ]
IP.1 = 100.98.227.25
IP.2 = 127.0.0.1
EOF
```
# Create a csr
```bash
openssl req -new -key etcd-node1.key -out etcd-node1.csr \
  -subj "/C=US/ST=YourState/L=YourCity/O=YourOrganization/OU=YourUnit/CN=etcd-node1" \
  -config temp.cnf
```
# Sign the cert
```bash
openssl x509 -req -in etcd-node1.csr -CA ca.crt -CAkey ca.key -CAcreateserial \
  -out etcd-node1.crt -days 7300 -sha256 -extensions v3_req -extfile temp.cnf
```
# Verify the cert and be sure you see Subject Name Alternative
```bash
openssl x509 -in etcd-node1.crt -text -noout | grep -A1 "Subject Alternative Name"
```
# Remove temp file
```bash
rm temp.cnf
```
# Generate a private key
```bash
openssl genrsa -out etcd-node2.key 2048
```
# Create temp file for config
```bash
cat > temp.cnf <<EOF
[ req ]
distinguished_name = req_distinguished_name
req_extensions = v3_req
[ req_distinguished_name ]
[ v3_req ]
subjectAltName = @alt_names
[ alt_names ]
IP.1 = 100.88.198.128
IP.2 = 127.0.0.1
EOF
```

# Create a csr
```bash
openssl req -new -key etcd-node2.key -out etcd-node2.csr \
  -subj "/C=US/ST=YourState/L=YourCity/O=YourOrganization/OU=YourUnit/CN=etcd-node2" \
  -config temp.cnf
```
# Sign the cert
```bash
openssl x509 -req -in etcd-node2.csr -CA ca.crt -CAkey ca.key -CAcreateserial \
  -out etcd-node2.crt -days 7300 -sha256 -extensions v3_req -extfile temp.cnf
```
# Verify the cert and be sure you see Subject Name Alternative
```bash
openssl x509 -in etcd-node2.crt -text -noout | grep -A1 "Subject Alternative Name"
```
# Remove temp file
```bash
rm temp.cnf
```
# Generate a private key
```bash
openssl genrsa -out etcd-node3.key 2048
```
# Create temp file for config
```bash
cat > temp.cnf <<EOF
[ req ]
distinguished_name = req_distinguished_name
req_extensions = v3_req
[ req_distinguished_name ]
[ v3_req ]
subjectAltName = @alt_names
[ alt_names ]
IP.1 = 100.94.193.99
IP.2 = 127.0.0.1
EOF
```
# Create a csr
```bash
openssl req -new -key etcd-node3.key -out etcd-node3.csr \
  -subj "/C=US/ST=YourState/L=YourCity/O=YourOrganization/OU=YourUnit/CN=etcd-node3" \
  -config temp.cnf
```
# Sign the cert
```bash
openssl x509 -req -in etcd-node3.csr -CA ca.crt -CAkey ca.key -CAcreateserial \
  -out etcd-node3.crt -days 7300 -sha256 -extensions v3_req -extfile temp.cnf
```
# Verify the cert and be sure you see Subject Name Alternative
```bash
openssl x509 -in etcd-node3.crt -text -noout | grep -A1 "Subject Alternative Name"
```
# Remove temp file
```bash
rm temp.cnf
```
# Secure copy (scp) the certs to each node:
```bash

scp ca.crt etcd-node1.crt etcd-node1.key serveradmin@100.98.227.25:/tmp/
scp ca.crt etcd-node2.crt etcd-node2.key serveradmin@100.88.198.128:/tmp/
scp ca.crt etcd-node3.crt etcd-node3.key serveradmin@100.94.193.99:/tmp/
```
# See files on each node:
```bash
ls /tmp
```
# on each nodeSee files on each node, We need to move certs from /tmp to ssl location (/etc/etcd/ssl)
```bash
sudo mkdir -p /etc/etcd/ssl
sudo mv /tmp/etcd-node*.crt /etc/etcd/ssl/
sudo mv /tmp/etcd-node*.key /etc/etcd/ssl/
sudo mv /tmp/ca.crt /etc/etcd/ssl/
sudo chown -R etcd:etcd /etc/etcd/
sudo chmod 600 /etc/etcd/ssl/etcd-node*.key
sudo chmod 644 /etc/etcd/ssl/etcd-node*.crt /etc/etcd/ssl/ca.crt
```
# Check certs are there:
```bash
ls /etc/etcd/ssl
```
# Configure
#Create our config
```bash
sudo nano /etc/etcd/etcd.env
```

# in the config file add

# Node 1
```bash
ETCD_NAME="postgresql-01"
ETCD_DATA_DIR="/var/lib/etcd"
ETCD_INITIAL_CLUSTER="postgresql-01=https://100.98.227.25:2380,postgresql-02=https://100.88.198.128:2380,postgresql-03=https://100.94.193.99:2380"
ETCD_INITIAL_CLUSTER_STATE="new"
ETCD_INITIAL_CLUSTER_TOKEN="etcd-cluster"
ETCD_INITIAL_ADVERTISE_PEER_URLS="https://100.98.227.25:2380"
ETCD_LISTEN_PEER_URLS="https://0.0.0.0:2380"
ETCD_LISTEN_CLIENT_URLS="https://0.0.0.0:2379"
ETCD_ADVERTISE_CLIENT_URLS="https://100.98.227.25:2379"
ETCD_CLIENT_CERT_AUTH="true"
ETCD_TRUSTED_CA_FILE="/etc/etcd/ssl/ca.crt"
ETCD_CERT_FILE="/etc/etcd/ssl/etcd-node1.crt"
ETCD_KEY_FILE="/etc/etcd/ssl/etcd-node1.key"
ETCD_PEER_CLIENT_CERT_AUTH="true"
ETCD_PEER_TRUSTED_CA_FILE="/etc/etcd/ssl/ca.crt"
ETCD_PEER_CERT_FILE="/etc/etcd/ssl/etcd-node1.crt"
ETCD_PEER_KEY_FILE="/etc/etcd/ssl/etcd-node1.key"
```
# Node 2
```bash
ETCD_NAME="postgresql-02"
ETCD_DATA_DIR="/var/lib/etcd"
ETCD_INITIAL_CLUSTER="postgresql-01=https://100.98.227.25:2380,postgresql-02=https://100.88.198.128:2380,postgresql-03=https://100.94.193.99:2380"
ETCD_INITIAL_CLUSTER_STATE="new"
ETCD_INITIAL_CLUSTER_TOKEN="etcd-cluster"
ETCD_INITIAL_ADVERTISE_PEER_URLS="https://100.88.198.128:2380"
ETCD_LISTEN_PEER_URLS="https://0.0.0.0:2380"
ETCD_LISTEN_CLIENT_URLS="https://0.0.0.0:2379"
ETCD_ADVERTISE_CLIENT_URLS="https://100.88.198.128:2379"
ETCD_CLIENT_CERT_AUTH="true"
ETCD_TRUSTED_CA_FILE="/etc/etcd/ssl/ca.crt"
ETCD_CERT_FILE="/etc/etcd/ssl/etcd-node2.crt"
ETCD_KEY_FILE="/etc/etcd/ssl/etcd-node2.key"
ETCD_PEER_CLIENT_CERT_AUTH="true"
ETCD_PEER_TRUSTED_CA_FILE="/etc/etcd/ssl/ca.crt"
ETCD_PEER_CERT_FILE="/etc/etcd/ssl/etcd-node2.crt"
ETCD_PEER_KEY_FILE="/etc/etcd/ssl/etcd-node2.key"
```
# Node 3
```bash
ETCD_NAME="postgresql-03"
ETCD_DATA_DIR="/var/lib/etcd"
ETCD_INITIAL_CLUSTER="postgresql-01=https://100.98.227.25:2380,postgresql-02=https://100.88.198.128:2380,postgresql-03=https://100.94.193.99:2380"
ETCD_INITIAL_CLUSTER_STATE="new"
ETCD_INITIAL_CLUSTER_TOKEN="etcd-cluster"
ETCD_INITIAL_ADVERTISE_PEER_URLS="https://100.94.193.99:2380"
ETCD_LISTEN_PEER_URLS="https://0.0.0.0:2380"
ETCD_LISTEN_CLIENT_URLS="https://0.0.0.0:2379"
ETCD_ADVERTISE_CLIENT_URLS="https://100.94.193.99:2379"
ETCD_CLIENT_CERT_AUTH="true"
ETCD_TRUSTED_CA_FILE="/etc/etcd/ssl/ca.crt"
ETCD_CERT_FILE="/etc/etcd/ssl/etcd-node3.crt"
ETCD_KEY_FILE="/etc/etcd/ssl/etcd-node3.key"
ETCD_PEER_CLIENT_CERT_AUTH="true"
ETCD_PEER_TRUSTED_CA_FILE="/etc/etcd/ssl/ca.crt"
ETCD_PEER_CERT_FILE="/etc/etcd/ssl/etcd-node3.crt"
ETCD_PEER_KEY_FILE="/etc/etcd/ssl/etcd-node3.key"
```

# let’s create a service for etcd on all 3 nodes
```bash
sudo nano /etc/systemd/system/etcd.service
```
# Add:
```bash
[Unit]
Description=etcd key-value store
Documentation=https://github.com/etcd-io/etcd
After=network-online.target
Wants=network-online.target

[Service]
Type=notify
WorkingDirectory=/var/lib/etcd
EnvironmentFile=/etc/etcd/etcd.env
ExecStart=/usr/local/bin/etcd
Restart=always
RestartSec=10s
LimitNOFILE=40000
User=etcd
Group=etcd

[Install]
WantedBy=multi-user.target
```
# We need to create a directory for etcd ETCD_DATA_DIR defined in service file.
```bash
sudo mkdir -p /var/lib/etcd 
sudo chown -R etcd:etcd /var/lib/etcd
```

# Reload and start
```bash
sudo systemctl daemon-reload
sudo systemctl enable etcd

sudo systemctl start etcd
sudo systemctl status etcd
```
# Check Logs:
```bash
journalctl -xeu etcd.service
```
# Once cluster is running, we should verify it’s working on each by running
```bash
sudo ETCDCTL_API=3 etcdctl \
--endpoints=https://100.98.227.25:2379 \
--cacert=/etc/etcd/ssl/ca.crt \
--cert=/etc/etcd/ssl/etcd-node1.crt \
--key=/etc/etcd/ssl/etcd-node1.key \
endpoint health
```
# To see member lists:
```bash
sudo etcdctl \
--endpoints=https://100.98.227.25:2379 \
--cacert=/etc/etcd/ssl/ca.crt \
--cert=/etc/etcd/ssl/etcd-node1.crt \
--key=/etc/etcd/ssl/etcd-node1.key \
member list
```
# To check for the leader:
```bash
sudo etcdctl   --endpoints=http://100.98.227.25:2379,http://100.88.198.128:2379,http://100.94.193.99:2379   --cacert=/etc/etcd/ssl/ca.crt   --cert=/etc/etcd/ssl/etcd-node1.crt   --key=/etc/etcd/ssl/etcd-node1.key   endpoint status --write-out=table
```
#Once this is all set up and working, we can now configure postgres and patroni.
#We need to create some dirs for postgres on each node.
```bash

sudo mkdir -p /var/lib/postgresql/data
sudo mkdir -p /var/lib/postgresql/ssl
```

# On your laptop

#Generate a self-signed certificate

#(this will last 20 years)
```bash	

openssl genrsa -out server.key 2048 # private key
openssl req -new -key server.key -out server.req # csr
openssl req -x509 -key server.key -in server.req -out server.crt -days 7300 # generate cert, valid for 20 years
```
#Update permissions:
```bash
chmod 600 server.key
```

#scp them to node1, node2, and node3
```bash	
scp server.crt server.key server.req jay@100.98.227.25:/tmp
scp server.crt server.key server.req jay2@100.88.198.128:/tmp
scp server.crt server.key server.req jay3@100.94.193.99 :/tmp
```
#On the servers (not your local machine) move files
```bash
cd /tmp
sudo mv server.crt server.key server.req /var/lib/postgresql/ssl
```
#Update permissions on certificate
```bash

sudo chmod 600 /var/lib/postgresql/ssl/server.key
sudo chmod 644 /var/lib/postgresql/ssl/server.crt
sudo chmod 600 /var/lib/postgresql/ssl/server.req
sudo chown postgres:postgres /var/lib/postgresql/data
sudo chown postgres:postgres /var/lib/postgresql/ssl/server.*
```
#We will need to give the postgres user read access to the etcd certificates using acls
	
```bash
sudo apt update
sudo apt install -y acl
```
#Node 1
```bash
sudo setfacl -m u:postgres:r /etc/etcd/ssl/ca.crt
sudo setfacl -m u:postgres:r /etc/etcd/ssl/etcd-node1.crt
sudo setfacl -m u:postgres:r /etc/etcd/ssl/etcd-node1.key
```
#Node 2
```bash
sudo setfacl -m u:postgres:r /etc/etcd/ssl/ca.crt
sudo setfacl -m u:postgres:r /etc/etcd/ssl/etcd-node2.crt
sudo setfacl -m u:postgres:r /etc/etcd/ssl/etcd-node2.key
```
#Node 3
```bash
sudo setfacl -m u:postgres:r /etc/etcd/ssl/ca.crt
sudo setfacl -m u:postgres:r /etc/etcd/ssl/etcd-node3.crt
sudo setfacl -m u:postgres:r /etc/etcd/ssl/etcd-node3.key
```
#now time to configure patroni to operate or drive postgres

#Installing Patroni
```bash	

sudo apt install -y patroni
```
#Make a dir for patroni
```bash	

sudo mkdir -p /etc/patroni/
```
# Configuring Patroni

#Create a config file and edit
	
```bash
sudo nano /etc/patroni/config.yml
```
#Node 1
```bash
scope: postgresql-cluster
namespace: /service/
name: postgresql-01  # node1

etcd3:
  hosts: 100.98.227.25:2379,100.88.198.128:2379,100.94.193.99:2379  # etcd cluster nodes
  protocol: https
  cacert: /etc/etcd/ssl/ca.crt
  cert: /etc/etcd/ssl/etcd-node1.crt  # node1's etcd certificate
  key: /etc/etcd/ssl/etcd-node1.key  # node1's etcd key

restapi:
  listen: 0.0.0.0:8008
  connect_address: 100.98.227.25:8008  # IP for node1's REST API
  certfile: /var/lib/postgresql/ssl/server.pem

bootstrap:
  dcs:
    ttl: 30
    loop_wait: 10
    retry_timeout: 10
    maximum_lag_on_failover: 1048576  # Failover parameters
    postgresql:
        parameters:
            ssl: 'on'  # Enable SSL
            ssl_cert_file: /var/lib/postgresql/ssl/server.crt  # PostgreSQL server certificate
            ssl_key_file: /var/lib/postgresql/ssl/server.key  # PostgreSQL server key
        pg_hba:  # Access rules
        - hostssl replication replicator 127.0.0.1/32 md5
        - hostssl replication replicator 100.98.227.25/32 md5
        - hostssl replication replicator 100.88.198.128/32 md5
        - hostssl replication replicator 100.94.193.99/32 md5
        - hostssl all all 127.0.0.1/32 md5
        - hostssl all all 0.0.0.0/0 md5
  initdb:
    - encoding: UTF8
    - data-checksums

postgresql:
  listen: 0.0.0.0:5432
  connect_address: 100.98.227.25:5432  # IP for node1's PostgreSQL
  data_dir: /var/lib/postgresql/data
  bin_dir: /usr/lib/postgresql/18/bin  # Binary directory for PostgreSQL 17
  authentication:
    superuser:
      username: postgres
      password: cnV2abjbDpbh64e12987wR4mj5kQ3456Y0Qf  # Superuser password - be sure to change
    replication:
      username: replicator
      password: sad9a23jga8jsuedrwtsskj74567suiuwe23  # Replication password - be sure to change
  parameters:
    max_connections: 100
    shared_buffers: 256MB

tags:
  nofailover: false
  noloadbalance: false
  clonefrom: false
```
#Node 2
```bash
scope: postgresql-cluster
namespace: /service/
name: postgresql-02  # node2

etcd3:
  hosts: 100.98.227.25:2379,100.88.198.128:2379,100.94.193.99:2379  # etcd cluster nodes
  protocol: https
  cacert: /etc/etcd/ssl/ca.crt
  cert: /etc/etcd/ssl/etcd-node2.crt  # node2's etcd certificate
  key: /etc/etcd/ssl/etcd-node2.key  # node2's etcd key

restapi:
  listen: 0.0.0.0:8008
  connect_address: 100.88.198.128:8008  # IP for node2's REST API
  certfile: /var/lib/postgresql/ssl/server.pem

bootstrap:
  dcs:
    ttl: 30
    loop_wait: 10
    retry_timeout: 10
    maximum_lag_on_failover: 1048576  # Failover parameters
    postgresql:
        parameters:
            ssl: 'on'  # Enable SSL
            ssl_cert_file: /var/lib/postgresql/ssl/server.crt  # PostgreSQL server certificate
            ssl_key_file: /var/lib/postgresql/ssl/server.key  # PostgreSQL server key
        pg_hba:  # Access rules
        - hostssl replication replicator 127.0.0.1/32 md5
        - hostssl replication replicator 100.98.227.25/32 md5
        - hostssl replication replicator 100.88.198.128/32 md5
        - hostssl replication replicator 100.94.193.99/32 md5
        - hostssl all all 127.0.0.1/32 md5
        - hostssl all all 0.0.0.0/0 md5
  initdb:
    - encoding: UTF8
    - data-checksums

postgresql:
  listen: 0.0.0.0:5432
  connect_address: 100.88.198.128:5432  # IP for node1's PostgreSQL
  data_dir: /var/lib/postgresql/data
  bin_dir: /usr/lib/postgresql/18/bin  # Binary directory for PostgreSQL 17
  authentication:
    superuser:
      username: postgres
      password: cnV2abjbDpbh64e12987wR4mj5kQ3456Y0Qf  # Superuser password - be sure to change
    replication:
      username: replicator
      password: sad9a23jga8jsuedrwtsskj74567suiuwe23  # Replication password - be sure to change
  parameters:
    max_connections: 100
    shared_buffers: 256MB

tags:
  nofailover: false
  noloadbalance: false
  clonefrom: false

```


#Node 3
```bash
scope: postgresql-cluster
namespace: /service/
name: postgresql-03  # node3

etcd3:
  hosts: 100.98.227.25:2379,100.88.198.128:2379,100.94.193.99:2379  # etcd cluster nodes
  protocol: https
  cacert: /etc/etcd/ssl/ca.crt
  cert: /etc/etcd/ssl/etcd-node3.crt  # node3's etcd certificate
  key: /etc/etcd/ssl/etcd-node3.key  # node3's etcd key

restapi:
  listen: 0.0.0.0:8008
  connect_address: 100.94.193.99:8008  # IP for node1's REST API
  certfile: /var/lib/postgresql/ssl/server.pem

bootstrap:
  dcs:
    ttl: 30
    loop_wait: 10
    retry_timeout: 10
    maximum_lag_on_failover: 1048576  # Failover parameters
    postgresql:
        parameters:
            ssl: 'on'  # Enable SSL
            ssl_cert_file: /var/lib/postgresql/ssl/server.crt  # PostgreSQL server certificate
            ssl_key_file: /var/lib/postgresql/ssl/server.key  # PostgreSQL server key
        pg_hba:  # Access rules
        - hostssl replication replicator 127.0.0.1/32 md5
        - hostssl replication replicator 100.98.227.25/32 md5
        - hostssl replication replicator 100.88.198.128/32 md5
        - hostssl replication replicator 100.94.193.99/32 md5
        - hostssl all all 127.0.0.1/32 md5
        - hostssl all all 0.0.0.0/0 md5
  initdb:
    - encoding: UTF8
    - data-checksums

postgresql:
  listen: 0.0.0.0:5432
  connect_address: 100.94.193.99:5432  # IP for node1's PostgreSQL
  data_dir: /var/lib/postgresql/data
  bin_dir: /usr/lib/postgresql/18/bin  # Binary directory for PostgreSQL 17
  authentication:
    superuser:
      username: postgres
      password: cnV2abjbDpbh64e12987wR4mj5kQ3456Y0Qf  # Superuser password - be sure to change
    replication:
      username: replicator
      password: sad9a23jga8jsuedrwtsskj74567suiuwe23  # Replication password - be sure to change
  parameters:
    max_connections: 100
    shared_buffers: 256MB

tags:
  nofailover: false
  noloadbalance: false
  clonefrom: false
```
#Let’s also use a certificate for this, requires a pem
```bash	

sudo sh -c 'cat /var/lib/postgresql/ssl/server.crt /var/lib/postgresql/ssl/server.key > /var/lib/postgresql/ssl/server.pem'
sudo chown postgres:postgres /var/lib/postgresql/ssl/server.pem
sudo chmod 600 /var/lib/postgresql/ssl/server.pem
```
#verify with:
```bash	

sudo openssl x509 -in /var/lib/postgresql/ssl/server.pem -text -noout
```
#Restart the service
```bash	

 sudo systemctl restart patroni
```
#Check logs
```bash	

journalctl -u patroni -f
```
#Reconfiguring our etcd Cluster
```bash	

sudo nano /etc/etcd/etcd.env
```
#Change
```bash	

ETCD_INITIAL_CLUSTER_STATE="new"
```

#to
	
```bash
ETCD_INITIAL_CLUSTER_STATE="existing"
```
#Verifying Our Postgres Cluster
```bash
curl -k https://100.98.227.25:8008/primary
curl -k https://100.88.198.128:8008/primary
curl -k https://100.94.193.99:8008/primary
```
# HA Proxy

#Installing HA Proxy

```bash
sudo apt -y install haproxy
sudo nano /etc/haproxy/haproxy.cfg

```
#add the following to your config file:
```bash
frontend postgres_frontend
    bind *:5432
    mode tcp
    default_backend postgres_backend

backend postgres_backend
    mode tcp
    option tcp-check
    option httpchk GET /primary  # patroni provides an endpoint to check node roles
    http-check expect status 200  # expect 200 for the primary node
    timeout connect 5s
    timeout client 30s
    timeout server 30s
    server postgresql-01 100.98.227.25:5432 port 8008 check check-ssl verify none
    server postgresql-02 100.88.198.128:5432 port 8008 check check-ssl verify none
    server postgresql-03 100.94.193.99:5432 port 8008 check check-ssl verify none
```
#restart
```bash
sudo systemctl reload haproxy
```
#check logs
``` bash	

sudo tail -f /var/log/syslog | grep haproxy
```
#keepalived
#Installing keepalived

# we need to install keepalived to create a VIP
```bash	

sudo apt update
sudo apt install keepalived -y
```
#Confuring keepalived
```bash
sudo nano /etc/keepalived/keepalived.conf
```

#in the config add

#Node 1
```bash
global_defs {
    enable_script_security
    script_user keepalived_script
}

vrrp_script check_haproxy {
    script "/etc/keepalived/check_haproxy.sh"
    interval 2
    fall 3
    rise 2
}

vrrp_instance VI_1 {
    state MASTER
    interface tailscale0 # update with your nic
    virtual_router_id 51
    priority 100
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass tDHjh7by # change
    }
    virtual_ipaddress {
        192.168.82.110
    }
    track_script {
        check_haproxy
    }
}

```

#Node 2
```bash
global_defs {
    enable_script_security
    script_user keepalived_script
}

vrrp_script check_haproxy {
    script "/etc/keepalived/check_haproxy.sh"
    interval 2
    fall 3
    rise 2
}

vrrp_instance VI_1 {
    state MASTER
    interface tailscale0 # update with your nic
    virtual_router_id 51
    priority 100
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass tDHjh7by # change
    }
    virtual_ipaddress {
        192.168.82.110
    }
    track_script {
        check_haproxy
    }
}

```
#Node 3
```bash
global_defs {
    enable_script_security
    script_user keepalived_script
}

vrrp_script check_haproxy {
    script "/etc/keepalived/check_haproxy.sh"
    interval 2
    fall 3
    rise 2
}

vrrp_instance VI_1 {
    state MASTER
    interface tailscale0 # update with your nic
    virtual_router_id 51
    priority 100
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass tDHjh7by # change
    }
    virtual_ipaddress {
        192.168.82.110
    }
    track_script {
        check_haproxy
    }
}
```
# create a script on each node
```bash

sudo nano /etc/keepalived/check_haproxy.sh
```
#add
```bash
#!/bin/bash

# Define the port to check (e.g., HAProxy frontend port)
PORT=5432

# Check if HAProxy is running
if ! pidof haproxy > /dev/null; then
    echo "HAProxy is not running"
    exit 1
fi

# Check if HAProxy is listening on the expected port
if ! ss -ltn | grep -q ":${PORT}"; then
    echo "HAProxy is not listening on port ${PORT}"
    exit 2
fi

# All checks passed
exit 0
```

#execute these scripts
	
```bash
sudo useradd -r -s /bin/false keepalived_script
```
#permissions
```bash
sudo chmod +x /etc/keepalived/check_haproxy.sh
sudo chown keepalived_script:keepalived_script /etc/keepalived/check_haproxy.sh
sudo chmod 700 /etc/keepalived/check_haproxy.sh
```
#Starting keepalived
```bash	

sudo systemctl restart keepalived
```
#Check logs
```bash	

sudo journalctl -u keepalived -f
```
#we should now be able to ping the VIP
	
```bash
ping 192.168.60.110
```
# Connecting with PGAdmin

#Connected with a client
```bash
https://www.pgadmin.org/
```
#create a server with the keepalive ip
#use the password set in :sudo nano /etc/patroni/config.yml
#mine is:
```bash
cnV2abjbDpbh64e12987wR4mj5kQ3456Y0Qf 
```
#add data
```bash
-- Create a table for Nintendo characters
CREATE TABLE nintendo_characters (
    character_id SERIAL PRIMARY KEY, -- Unique identifier for each character
    name VARCHAR(50) NOT NULL,       -- Name of the character
    game_series VARCHAR(50),         -- Game series the character belongs to
    debut_year INT,                  -- Year the character debuted
    description TEXT,                -- Brief description of the character
    is_playable BOOLEAN DEFAULT TRUE -- Whether the character is playable
);

-- Insert some example characters
INSERT INTO nintendo_characters (name, game_series, debut_year, description, is_playable)
VALUES
    ('Mario', 'Super Mario', 1981, 'The iconic plumber and hero of the Mushroom Kingdom.', TRUE),
    ('Link', 'The Legend of Zelda', 1986, 'A courageous hero tasked with saving Hyrule.', TRUE),
    ('Samus Aran', 'Metroid', 1986, 'A bounty hunter equipped with a powerful Power Suit.', TRUE),
    ('Donkey Kong', 'Donkey Kong', 1981, 'A powerful gorilla and protector of the jungle.', TRUE),
    ('Princess Zelda', 'The Legend of Zelda', 1986, 'The princess of Hyrule and possessor of the Triforce of Wisdom.', FALSE),
    ('Bowser', 'Super Mario', 1985, 'The King of the Koopas and Marios arch-nemesis.', FALSE),
    ('Kirby', 'Kirby', 1992, 'A pink puffball with the ability to inhale enemies and copy their powers.', TRUE),
    ('Pikachu', 'Pokémon', 1996, 'An Electric-type Pokémon and mascot of the Pokémon series.', TRUE),
    ('Fox McCloud', 'Star Fox', 1993, 'A skilled pilot and leader of the Star Fox team.', TRUE),
    ('Captain Falcon', 'F-Zero', 1990, 'A bounty hunter and expert racer known for his Falcon Punch.', TRUE);

-- Select all rows to verify the table creation and data insertion
SELECT * FROM nintendo_characters;

```
```bash
SELECT * FROM nintendo_characters;
```
#insert more characters
```bash 
-- Insert additional Nintendo characters into the table
INSERT INTO nintendo_characters (name, game_series, debut_year, description, is_playable)
VALUES
    ('Yoshi', 'Super Mario', 1990, 'A friendly green dinosaur and Marios trusted companion.', TRUE),
    ('Luigi', 'Super Mario', 1983, 'Marios younger brother and a skilled ghost hunter.', TRUE),
    ('King Dedede', 'Kirby', 1992, 'The self-proclaimed king of Dream Land and occasional ally of Kirby.', TRUE),
    ('Meta Knight', 'Kirby', 1993, 'A mysterious swordsman who often challenges Kirby.', TRUE),
    ('Marth', 'Fire Emblem', 1990, 'A legendary hero and prince from the Fire Emblem series.', TRUE),
    ('Ness', 'EarthBound', 1994, 'A young boy with psychic powers and a bat-wielding hero.', TRUE),
    ('Jigglypuff', 'Pokémon', 1996, 'A Balloon Pokémon known for its singing abilities.', TRUE),
    ('Villager', 'Animal Crossing', 2001, 'A customizable character from the Animal Crossing series.', TRUE),
    ('Isabelle', 'Animal Crossing', 2012, 'A cheerful assistant who helps manage your town.', TRUE),
    ('Ganondorf', 'The Legend of Zelda', 1998, 'The King of Evil and nemesis of Link.', TRUE);

```
#If you want to clean this data up, you can DROP the table
```bash	

-- Drop the nintendo_characters table if it exists
DROP TABLE IF EXISTS nintendo_characters;
```


