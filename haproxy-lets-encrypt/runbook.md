#installation:
sudo apt update
sudo apt install haproxy -y
#Check version :
haproxy -v
#Open the conf file:
sudo nano /etc/haproxy/haproxy.cfg
#At the bottom of the conf file configure backend and frontend  by adding the following lines:
frontend web-frontend 
        bind *:80
        default_backend web-backend
backend web-backend
        balance roundrobin
        server web1 192.168.84.54:80 check

#You can add more than one server at server
#start/ restart/enable the haproxy:
sudo systemctl enable haproxy
sudo systemctl start haproxy
sudo systemctl status haproxy

