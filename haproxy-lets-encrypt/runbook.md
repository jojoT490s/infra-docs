##HAPROXY RUNBOOK

##installation:

```bash
sudo apt update
sudo apt install haproxy -y
```
##Check version :
```bash
haproxy -v
```
##Open the conf file:
```bash
sudo nano /etc/haproxy/haproxy.cfg
```
##At the bottom of the conf file configure backend and frontend  by adding the f>
```bash
frontend web-frontend

        bind *:80

        default_backend web-backend

backend web-backend

        balance roundrobin

        server web1 192.168.84.54:8080 check
```
##You can add more than one server at server

##start/ restart/enable the haproxy:
```bash
sudo systemctl enable haproxy

sudo systemctl start haproxy

sudo systemctl status haproxy
```
##Test the conf file:
```bash
 haproxy -sudo -f /etc/haproxy/haproxy.cfg
```
##restart:

```bash
sudo systemctl restart haproxy
```
##Because they are running on the same server run a temporary python  to act as the backend:
```bash
python3 -m http.server 8080
```
 ## Then run this in another terminal:
```bash
curl http://192.168.84.54:8080  
```
##If you see html its working

##i did not have a domain so i created self assigned certs:
```bash
openssl req -x509 -nodes -days 365 \
newkey rsa:2048 \

keyout privkey.pem \

out fullchain.pem

```

##Combine the certificates:
```bash
cat fullchain.pem privkey.pem > haproxy.pem
```
## Make a haproxy certs file and move the keys there:
```bash
sudo mkdir -p /etc/haproxy/certs

sudo mv haproxy.pem /etc/haproxy/certs/
```
## Give the file permissions:
```bash
sudo chmod 600 /etc/haproxy/certs/haproxy.pem
```

##Edit the haproxy conf file: 
```bash
sudo nano /etc/haproxy/haproxy.cfg
```
##Needed to create DH parameters:
```bash
sudo openssl dhparam -out /etc/haproxy/dhparams.pem 2048
```
##Append the dh parameters to the conf file:
```bash
sudo bash -c 'cat /etc/haproxy/dhparams.pem >> /etc/haproxy/certs/haproxy.pem'
```
##Test to see certs worked:
```bash
sudo haproxy -c -f /etc/haproxy/haproxy.cfg
```
## After using self assigned certs this is what is in my conf file:

```bash
frontend web-frontend

    bind *:80

    bind *:443 ssl crt /etc/haproxy/certs/haproxy.pem


   redirect scheme https if !{ ssl_fc }


    default_backend web-backend


backend web-backend

    balance roundrobin

    server web1 192.168.84.54:8080 check
```
##I added this at the top of my conf file:
```bash
global

    tune.ssl.default-dh-param 2048
```
# #CONFIGURE STATISTICS FOR HAproxy

##In the config file add the following lines:
```bash
listen stats

       bind 192.168.84.54:8404

      mode http

       stats enable

    stats uri /stats

        stats refresh 10s
```
##Add port 8404 in ufw:
```bash
sudo ufw allow 8404
```
##Check for stats in a browser:
```bash
http://192.168.84.54:8404/stats
```
#LETS ENCRYPT WORK FLOW

##Certbot requests a certificate from Let's Encrypt using ACME protocal


##Let's Encrypt sends an HTTP-01 challenge token

 ##HAProxy listens on port 80

 ##Certbot starts a temporary challenge server on port 8888 - this  is after setting the acl variable above and creating a backend that runs on port 8888

##HAProxy ACL detects requests to:

##/.well-known/acme-challenge/

##Let's Encrypt requests the token over the internet

 ##Certbot serves the correct token

#Let's Encrypt verifies domain ownership

##The certificate is issuedHAProxy forwards those requests to the Certbot backend on port 8888

##Certbot stores the certificate files

 ##HAProxy uses the certificates for HTTPS

## Certbot later renews automatically using the same process 



