>NOTe: my server running ubuntu 20.04 lts which supports postgres 12 and that is where we will be running this task:

# POSTGRES INSTALLATION
```bash
sudo apt update-

sudo apt upgrade -y
```
#Install required tools:
```bash
sudo apt install wget curl gnupg2 lsb-release software-properties-common -y
```
#install:
```bash
sudo apt install postgresql-12 postgresql-client-12 -y
```
#Start and enable:
```bash
sudo systemctl enable postgresql

sudo systemctl start postgresql

sudo systemctl status postgresql
```

#Switch to postgres:
```bash
sudo -i -u postgres
```
#Create a database+ a dedicated user:
```bash
-CREATE ROLE metricsuser WITH LOGIN PASSWORD 'StrongPassword123!';
```
#Create a database:
```bash
CREATE DATABASE metricsdb OWNER metricsuser;
```
#Grant privileges:
```bash
GRANT ALL PRIVILEGES ON DATABASE metricsdb TO metricsuser;
```
#Check the database:
```bash
\l
```
#Exit user and postgres:
```bash
\q

\exit
```
#ALLOW REMOTE CONECTIONS

#open:
```bash
sudo nano /etc/postgresql/12/main/postgresql.conf
```
#Find the:
```bash
listen_addresses = 'localhost'
```
#Change it to:
```bash
listen_addresses = '*'
```
#Save and exit

#CONFIGURE pg_hba config FOR REMOTE ACCESS
#open:
```bash
sudo nano /etc/postgresql/12/main/pg_hba.conf
```
#Add the following at the bottom:
```bash
host    all             all             192.168.84.0/24          md5
```
#Restart postgres:
```bash
sudo systemctl restart postgresql
```
#Check if its listening :
```bash
sudo ss -tulnp | grep 5432
```
#Add port to firewall:
```bash
sudo ufw allow 5432/tcp
```

#Test remote connection 

#From  your client laptop:

#Install client postgres:

```bash
psql -h 192.168.84.54 -U metricsuser -d metricsdb
```
#connect:
```bash
psql -h 192.168.84.54 -U metricsuser -d metricsdb
```


#TIMESCALEDB

#Add repository:
```bash
echo "deb https://packagecloud.io/timescale/timescaledb/ubuntu/ focal main" | \

sudo tee /etc/apt/sources.list.d/timescaledb.list
```
#Import key:
```bash
wget --quiet -O - https://packagecloud.io/timescale/timescaledb/gpgkey | sudo apt-key add -
```
##update:
```bash
sudo apt update
```
#Install timescale:
```bash
sudo apt install timescaledb-2-postgresql-12 -y
```
#Run tunning for timescale:
```bash
sudo timescaledb-tune
```
#Accept the recommendations


#Restart postgress:
```bash
sudo systemctl restart postgresql
```
#Enable timescale:
```bash
sudo -u postgres psql metricsdb
```
#Enable extension:
```bash
CREATE EXTENSION IF NOT EXISTS timescaledb;
```
#Verify:
```bash
\dx
```
#Insert a test row and check:
```bash
INSERT INTO sensor_data VALUES

(NOW(), 'sensor1', 24.5, 65.2);

SELECT * FROM sensor_data;

Quit :\q
```
#AUTOMATING BACKUP TO LOCAL MACHINE

#Create a backup directory:
```bash
sudo mkdir -p /var/backups/postgresql
```
#Give it permissions:
```bash
sudo chown postgres:postgres /var/backups/postgresql
```
#Create a backup script:
```bash
sudo nano /usr/local/bin/pg_backup.sh
```
#This contains:
```bash
!/bin/bash

DATE=$(date +%F_%H-%M-%S)

pg_dump -U postgres metricsdb > /var/backups/postgresql/metricsdb_$DATE.sql
```
#Make it executable and test:
```bash
sudo chmod +x /usr/local/bin/pg_backup.sh

sudo -u postgres /usr/local/bin/pg_backup.sh

Check for file:ls /var/backups/postgresql

The expected result is:metricsdb_2026-05-25_01-00-00.sql
```
#Automate backups with cron:
```bash
sudo crontab -e
```
#Add the following line
```bash
0 1 * * * /usr/local/bin/pg_backup.sh
```


#SYNCHING BACKUPS

#SSH


#Generate ssh keys:
```bash
ssh-keygen -t ed25519:

```
#NOTE: my laptop did not have an authorised keys file so i had to create One:
```bash
mkdir -p ~/.ssh

chmod 700 ~/.ssh

touch ~/.ssh/authorized_keys

chmod 600 ~/.ssh/authorized_keys
```
#The copy id:
```bash
cat timesc.pub | ssh jojo@100.123.163.71 "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"

```
#RSYNC


#Installing rsync
```bash
sudo apt install rsync -y
```
#Synching backups to  my laptop:
```bash
mkdir -p ~/postgres_backups
```
#From the server run:
```bash
rsync -avz /var/backups/postgresql/ jojo@100.123.16.71:/home/jojo/postgres_backups/
```
#Automate rysnc by opening:sudo crontab -e

#Add:
```bash
30 1 * * * rsync -avz /var/backups/postgresql/ jojo@100.123.163.71:/home/jojo/postgres_backups/
```
 
#REPLICATION


#Configure replication on the server

 #open:
```bash
sudo nano /etc/postgresql/12/main/postgresql.conf
```

#Edit the following:
```bash
wal_level = replica

max_wal_senders = 10

hot_standby = on

```

#Create a replication user:
```bash
sudo -u postgres psql

CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD 'ReplicaPass123!';

Quit:\q
```
# Allow replication connections:
```bash
sudo nano /etc/postgresql/12/main/pg_hba.conf
```
#Add the following line:
```bash
host replication replicator 192.168.84.0/24 md5
```
#Restart postgrss:
```bash
sudo systemctl restart postgresql
```


#ON THE LAPTOP

#Install postgress on the laptop:
```bash
sudo apt install wget gnupg2 lsb-release curl -y
```
#Repo key :
```bash
curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | \

sudo gpg --dearmor -o /usr/share/keyrings/postgresql.gpg

repo:echo "deb [signed-by=/usr/share/keyrings/postgresql.gpg] \

http://apt.postgresql.org/pub/repos/apt \

$(lsb_release -cs)-pgdg main" | \

sudo tee /etc/apt/sources.list.d/pgdg.list
```
#update:
```bash
sudo apt update
```
#install:
```bash

sudo apt install postgresql-12 postgresql-client-12 -y
```
#On  the laptop stop postgress:
```bash
sudo systemctl stop postgresql
```

#Clone primary database:
```bash
sudo -u postgres pg_basebackup \
-h 192.168.84.54 \
-D /var/lib/postgresql/12/main \
-U replicator \
-P \
-R
```
# Start postgress: 
```bash
sudo systemctl start postgresql

sudo systemctl status postgresql
```


#ON THE SERVER

#Verify replication:
```bash
sudo -u postgres psql
```
#Run :
```bash
SELECT * FROM pg_stat_replication;
```
#ON THE LAPTOP:
#open:
```bash
sudo nano /etc/postgresql/12/main/postgresql.conf
```
#Add:
```bash
max_worker_processes = 21

max_locks_per_transaction = 1024

hot_standby = on

sudo pg_ctlcluster 12 main restart


sudo -u postgres psql -c "SELECT * FROM pg_stat_wal_receiver;"
```
#Check replicated database appears:
```bash
sudo -u postgres psql -c "\l"
```






