# RKE2 KUBERNETES CLUSTER
#For this installation i used 2 nodes

# MASTER NODE  INSTALLATION
# update and upgrade
```bash
sudo apt update && sudo apt upgrade -y
```
# change to root
```bash
sudo su
```
# install rke2
```bash
curl -sfL https://get.rke2.io | sh -
```
# enable the service
```bash
systemctl enable rke2-server.service
```
# start service
```bash
sudo systemctl start rke2-server.service
```
# check logs
```bash
journalctl -u rke2-server -f
```
# check files
```bash
ls /etc/rancher/rke2
```
# create a config.yaml file in the same location
```bash
 nano  /etc/rancher/rke2/config.yaml
```
# add this to the file
```bash
write-kubeconfig-mode: "0644"
```
# move kubectl
#Kubectl is installed but in a different directory  so we need to make sure its in the right  place:
# First exit root
```bash 
exit
```
#  Create kube directory to move the file to from /var/lib/rancher/rke2/bin/  and change ownership:
```bash
mkdir -p ~/.kube
sudo cp /etc/rancher/rke2/rke2.yaml ~/.kube/config
sudo chown $(whoami):$(whoami) ~/.kube/config
```
# Export kubectl binary: 
```bash
export PATH=$PATH:/var/lib/rancher/rke2/bin/
```
# check nodes
```bash
kubectl get nodes
```
# check pods
```bash
kubectl get pods -A
```
# Create a token to join other nodes to the cluster:
```bash
sudo cat /var/lib/rancher/rke2/server/node-token
```
# copy config file with kubectl to the worker node
``` bash
sudo cat /var/lib/rancher/rke2/server/node-token
```

# SET UP THE WORKER NODE

# Go  to root user
```bash
sudo su
```
# run installer
```bash
curl -sfL https://get.rke2.io | INSTALL_RKE2_TYPE="agent" sh -
```
# Configure the service:
```bash
mkdir -p /etc/rancher/rke2/

nano /etc/rancher/rke2/config.yaml
```
# add
```bash
server: https://<server>:9345
token: <token from server node>
```
# Start the service
```bash
systemctl start rke2-agent.service
```
# Check logs
``` bash 
journalctl -u rke2-agent -f
```
# move the config file for kubectl and make it permanent
```bash
sudo mkdir -p /etc/rancher/rke2

sudo mv /tmp/rke2.yaml /etc/rancher/rke2/rke2.yaml

mkdir -p ~/.kube

sudo cp /etc/rancher/rke2/rke2.yaml ~/.kube/config

sudo chown $(whoami):$(whoami) ~/.kube/config

echo 'export KUBECONFIG=$HOME/.kube/config' >> ~/.bashrc
source ~/.bashrc

echo 'export PATH=$PATH:/var/lib/rancher/rke2/bin' >> ~/.bashrc
source ~/.bashrc
```
# check nodes
```bash
 kubectl get nodes
```

# ON THE SERVER NODE

# NGINX DEPLOYMENT
# Creating a sample application and deploying it on the cluster:
```bash
kubectl create deployment nginx --image=nginx
```
# Expose it using a node port service  to see it on  the browser:
```bash
kubectl expose deployment nginx --port=80 --type=NodePort
```
# Allow node ports on ufw:
```bash
sudo ufw allow 30000:32767/tcp
```
# Check service
```bash
kubectl get svc
kubectl get all
```
# Open nginx on browser
```bash
http://100.112.210.49:30337/
```

# SETTING NETWORK POLICY

#  Check if CNI supports network policy:
```bash
kubectl get pods -n kube-system
```
# Create a isolated namespace:
``` bash
kubectl create namespace demo
```
# Deploy an exposed nginx:
```bash
kubectl create deployment nginx -n demo --image=nginx
kubectl expose deployment nginx -n demo --port=80 --type=NodePort
```
# Apply a default deny network policy by creating  a config file:
```bash
nano deny-all.yaml
```
# Add the following inside:
```bash
kind: NetworkPolicy
metadata:
  name: deny-all
  namespace: demo
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```
#  Apply the conf: 
```bash
kubectl apply -f deny-all.yaml
```
# Try access the service this should fail
```bash
kubectl get svc -n demo
```
# Try curl from a test pod
```bash
kubectl run test --rm -it --image=busybox -n demo -- sh
```
# Inside add:
```bash
wget -O- http://nginx
```
# To allow nginx create its net policy yaml 
```bash
nano nginx.yaml
```
# Add:
```bash
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-nginx-internal
  namespace: demo
spec:
  podSelector:
    matchLabels:
      app: nginx
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector: {}
    ports:
    - protocol: TCP
      port: 80
```
# apply
```bash
kubectl apply -f nginx.yaml
```
# test
```bash
kubectl run test --rm -it --image=busybox -n demo -- sh
```
# add:
``` bash 
wget -O- http://nginx
```
# Your should get something like pod is running
# Run  checklist:
```bash
kubectl get pods -n demo
kubectl get netpol -n demo
kubectl describe netpol allow-nginx-internal -n demo
```
