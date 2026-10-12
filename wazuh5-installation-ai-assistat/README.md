 WAZUH INSTALLATION

We used wazuh documentation  guide  step by step method

### **Generating the SSL certificates**

**Download the `wazuh-certs-tool-5.0.0-beta5.sh` script and the `config.yml` configuration file. This creates the certificates that encrypt communications between the Wazuh central components:**

 ```bash
 curl \-sO [https\://packages-staging.xdrsiem.wazuh.info/pre-release/5.x/installation-assistant/wazuh-certs-tool-5.0.0-beta5.sh](https://packages-staging.xdrsiem.wazuh.info/pre-release/5.x/installation-assistant/wazuh-certs-tool-5.0.0-beta5.sh)**

**curl \-o config.yml https\://packages-staging.xdrsiem.wazuh.info/pre-release/5.x/installation-assistant/config-5.0.0-beta5.yml**
```
1. 

**Edit `./config.yml` and replace the node names and IP values with the corresponding names and IP addresses. You need to do this for all Wazuh manager, Wazuh indexer, and Wazuh dashboard nodes. Add as many node fields as needed:**  
**Open   the yaml**  
 ```bash
 **nano ./config .yml**
```
 **nodes:**  
  **\# Wazuh indexer nodes**  
  **indexer:**  
    **\- name: indexer**  
      **ip: "\<indexer-node-ip\>"**  
    **\#- name: indexer-2**  
    **\#  ip: "\<indexer-node-ip\>"**  
    **\#- name: indexer-3**  
    **\#  ip: "\<indexer-node-ip\>"**

  **\# Wazuh manager nodes**  
  **\# If there is more than one Wazuh manager**  
  **\# node, each one must have a node\_type**  
  **manager:**  
    **\- name: manager**  
      **ip: "\<wazuh-manager-ip\>"**  
    **\#  node\_type: master**  
    **\#- name: manager-2**  
    **\#  ip: "\<wazuh-manager-ip\>"**  
    **\#  node\_type: worker**  
    **\#- name: manager-3**  
    **\#  ip: "\<wazuh-manager-ip\>"**  
    **\#  node\_type: worker**

  **\# Wazuh dashboard nodes**  
  **dashboard:**  
    **\- name: dashboard**  
      **ip: "\<dashboard-node-ip\>"**

**NOTE : don’t change the names.**

2.  **To learn more about how to create and configure the certificates, see the [Certificates deployment](https://documentation.wazuh.com/5.0-beta/user-manual/wazuh-indexer-cluster/cluster-configuration.html#wazuh-indexer-cluster-certificates-deployment) section.**

**Run `./wazuh-certs-tool-5.0.0-beta5.sh` to create the certificates. For a multi-node cluster, these certificates need to be later deployed to all Wazuh instances in your cluster:**
```bash
 **bash ./wazuh-certs-tool-5.0.0-beta5.sh \-A**
```
3. 

**Compress all the necessary files:**
```bash
 **tar \-cvf ./wazuh-certificates.tar \-C ./wazuh-certificates/ .**  
**rm \-rf ./wazuh-certificates**
```
**NOTE : MAKE A  COPY OF THE TAR FILE  YOU WILL NEED THE CERTIFICATES**

4.   
5. **Copy the `wazuh-certificates.tar` file to all the nodes, including the Wazuh indexer, Wazuh manager, and Wazuh dashboard nodes. You can use the `scp` utility or any other secure file transfer method available in your environment.**

## **Wazuh indexer nodes installation**

**Follow these steps to install and configure a single-node or multi-node Wazuh indexer.**

### **Installing package dependencies**

**Run the following command to install the following packages if missing:**

 **APTYumDNF**  
```bash
**apt install debconf adduser procps curl**
```
1. 

### **Adding the Wazuh repository**

**APTYumDNF**  

**Install the following packages if missing:**
```bash
 **apt-get install \-y gnupg apt-transport-https curl**
```
1. 

**Install the GPG key:**
```bash
 **curl \-s https\://packages-staging.xdrsiem.wazuh.info/key/GPG-KEY-WAZUH | gpg \--no-default-keyring \--keyring gnupg-ring:/usr/share/keyrings/wazuh.gpg \--import && chmod 644 /usr/share/keyrings/wazuh.gpg**
```
2. 

**Add the repository:**
```bash
 **echo "deb \[signed-by=/usr/share/keyrings/wazuh.gpg\] https\://packages-staging.xdrsiem.wazuh.info/pre-release/5.x/apt/ unstable main" | tee \-a /etc/apt/sources.list.d/wazuh.list**
```
3. 

**Update the packages information:**
```bash
 **apt-get update**
```
4. 

### **Installing the Wazuh indexer**

**Install the Wazuh indexer package.**

 **APTYumDNF**  
 ```bash
**apt-get \-y install wazuh-indexer**
```
**NOTE: I could not find beta5  so i used the above**

1. 

### **Configuring the Wazuh indexer**

1. **Edit ```bash`/etc/wazuh-indexer/opensearch.yml``` and replace the following values:**

   1. **`network.host`: Sets the address of this node for both HTTP and transport traffic. The node will bind to this address and will also use it as its publish address. Accepts an IP address or a hostname.**

       **Use the same node address set in `config.yml` to create the SSL certificates.**

   2. **`node.name`: Name of the Wazuh indexer node as defined in the `config.yml` file. For example, `indexer`.**

**`cluster.initial_cluster_manager_nodes`: List of the names of the master-eligible nodes. Use names defined in the `config.yml` file, for example, `indexer`. Uncomment the `node-2` and `node-3` lines, change the names, or add more lines, according to your `config.yml` definitions.**

 **cluster.initial\_cluster\_manager\_nodes:**  
**\- "indexer"**  
**\#- "node-2"**  
**\#- "node-3"**

3. 

**`discovery.seed_hosts:` List of the addresses of the master-eligible nodes. Each element can be either an IP address or a hostname. You may leave this setting commented if you are configuring the Wazuh indexer as a single-node. For multi-node configurations, uncomment this setting and set the addresses of each master-eligible node.**

 **discovery.seed\_hosts:**  
  **\# \- "node-1-ip"**  
  **\# \- "node-2-ip"**  
  **\# \- "node-3-ip"**

4. 

**`plugins.security.nodes_dn`: List of the Distinguished Names of the certificates of every Wazuh indexer cluster node. Uncomment the lines for `node-2` and `node-3` and change the common names (CN) and values according to your settings and your `config.yml` definitions.**

 **plugins.security.nodes\_dn:**  
**\- "CN=indexer,OU=Wazuh,O=Wazuh,L=California,C=US"**  
**\#- "CN=node-2,OU=Wazuh,O=Wazuh,L=California,C=US"**  
**\#- "CN=node-3,OU=Wazuh,O=Wazuh,L=California,C=US"**

**![][image1]**

### **Deploying certificates**

**Note**

**Make sure that a copy of `wazuh-certificates.tar`, created in the previous stage of the installation process, is placed in your working directory.**

**Run the following commands, replacing `<INDEXER_NODE_NAME>` with the name of the Wazuh indexer node you are configuring as defined in `config.yml`. In our case, the node name is `indexer`. This is to deploy the SSL certificates to encrypt communication between the Wazuh central components:**
```bash
 **NODE\_NAME=\<INDEXER\_NODE\_NAME\>**  
 **mkdir \-p /etc/wazuh-indexer/certs**  
**tar \-xf ./wazuh-certificates.tar \-C /etc/wazuh-indexer/certs/ ./\$NODE\_NAME.pem ./\$NODE\_NAME-key.pem ./admin.pem ./admin-key.pem ./root-ca.pem**  
**mv \-n /etc/wazuh-indexer/certs/\$NODE\_NAME.pem /etc/wazuh-indexer/certs/indexer.pem**  
**mv \-n /etc/wazuh-indexer/certs/\$NODE\_NAME-key.pem /etc/wazuh-indexer/certs/indexer-key.pem**  
**chmod 500 /etc/wazuh-indexer/certs**  
**chmod 400 /etc/wazuh-indexer/certs/\***  
**chown \-R wazuh-indexer:wazuh-indexer /etc/wazuh-indexer/certs**
```
1. 

**Recommended action: If no other Wazuh components will be installed on this node, run the following command to remove the `wazuh-certificates.tar` file.**

 **rm \-f ./wazuh-certificates.tar**

2. 

### **Starting the service**

**Enable and start the Wazuh indexer service.**
```bash
 **SystemdSysV Init**  
**systemctl daemon-reload**  
**systemctl enable wazuh-indexer**  
**systemctl start wazuh-indexer**
```
> 1. 

**Repeat this stage of the installation process for every Wazuh indexer node in your multi-node cluster. Then proceed with initializing your single-node or multi-node cluster in the next stage.**

## **Cluster initialization**

**The final stage of installing the Wazuh indexer single-node or multi-node cluster consists of running the security admin script.**

**Run the Wazuh indexer `indexer-security-init.sh` script on any Wazuh indexer node to load the new certificates information and start the single-node or multi-node cluster.**
```bash
 **/usr/share/wazuh-indexer/bin/indexer-security-init.sh**
```
1.  **Note**

    **You only have to initialize the cluster once, there is no need to run this command on every node.**

### **Testing the cluster installation**

**Run the following commands to confirm that the installation is successful. Replace `<WAZUH_INDEXER_IP_ADDRESS>` with the IP address of the Wazuh indexer and enter admin as the password when prompted:**
```bash
 **curl \-k \-u admin https\://\<WAZUH\_INDEXER\_IP\_ADDRESS\>:9200**
```
 **Output**  
**{**  
  **"name" : "indexer",**  
  **"cluster\_name" : "wazuh-cluster",**  
  **"cluster\_uuid" : "2iYNKDCzR1ShJvSN-2vfOQ",**  
  **"version" : {**  
    **"distribution" : "opensearch",**  
    **"number" : "3.6.0",**  
    **"build\_type" : "deb",**  
    **"build\_hash" : "5917bc144ef6b8971cb17e53e475e306954c8fc9",**  
    **"build\_date" : "2026-07-29T01:44:46.892912988Z",**  
    **"build\_snapshot" : false,**  
    **"lucene\_version" : "10.4.0",**  
    **"minimum\_wire\_compatibility\_version" : "2.19.0",**  
    **"minimum\_index\_compatibility\_version" : "2.0.0"**  
  **},**  
  **"tagline" : "The OpenSearch Project: https\://opensearch.org/"**  
**}**

1. 

**Run the following command to check if the cluster is working correctly. Replace `<WAZUH_INDEXER_IP_ADDRESS>` with the IP address of the Wazuh indexer and enter admin as the password when prompted:**
```bash
 **curl \-k \-u admin https\://\<WAZUH\_INDEXER\_IP\_ADDRESS\>:9200/\_cat/nodes?v**  
```
 **The command produces output similar to the following:**


 **Output**  
**ip              heap.percent ram.percent cpu load\_1m load\_5m load\_15m node.role node.roles                               cluster\_manager name**  
**192.168.107.240           19          94   4    0.22    0.21     0.20 dimr      data,ingest,master,remote\_cluster\_client \*               node-1**

2. 

## **Memory locking**

**When the system is swapping memory, the Wazuh indexer may not work as expected. Therefore, it is important for the health of the Wazuh indexer node that none of the Java Virtual Machine (JVM) is ever swapped out to disk. To prevent any Wazuh indexer memory from being swapped out, configure the Wazuh indexer to lock the process address space into RAM as follows.**

**Note**

**You require root user privileges to run the commands described below.**

**Ensure the following line is present in the `/etc/wazuh-indexer/opensearch.yml` configuration file on the Wazuh indexer to enable memory locking and add it if missing:**

 **bootstrap.memory\_lock: true**

1.   
2. **Modify the limit of system resources. Configuring system settings depends on the operating system of the Wazuh indexer installation.**

    **SystemdSysV init**

**Create a new directory for the file that specifies the system limits:**
```bash
 **mkdir \-p /etc/systemd/system/wazuh-indexer.service.d/**
```
* 

**Run the following command to create the `wazuh-indexer.conf` file in the newly created directory with the new system limit added:**
```bash
 **cat \> /etc/systemd/system/wazuh-indexer.service.d/wazuh-indexer.conf \<\< EOF**  
**\[Service\]**  
**LimitMEMLOCK=infinity**  
**EOF**
```
* 

**Edit the `/etc/wazuh-indexer/jvm.options` file and change the JVM flags. Set a Wazuh indexer heap size value to limit memory usage. JVM heap limits prevent the `OutOfMemory` exception if the Wazuh indexer tries to allocate more memory than is available due to the configuration in the previous step. The recommended value is half of the system RAM. For example, set the size as follows for a system with 8 GB of RAM.**

 **\-Xms4g**  
**\-Xmx4g**

3.  **Where the total heap space:**

   * **`-Xms4g` \- initial size is set to 4Gb of RAM.**  
   * **`-Xmx4g` \- maximum size is to 4Gb of RAM.**  
4. **Note**

    **To prevent performance degradation due to JVM heap resizing at runtime, the minimum (Xms) and maximum (Xmx) size values must be the same.**

   **![][image2]**

**Restart the Wazuh indexer service:**
```bash
 **systemctl daemon-reload**  
**systemctl restart wazuh-indexer**
```
5. 

**Verify that the setting was changed successfully, by running the following command to check that `mlockall` value is set to true:**
```bash
 **curl \-k \-u \<INDEXER\_USERNAME\>:\<INDEXER\_PASSWORD\> "https\://\<INDEXER\_IP\_ADDRESS\>:9200/\_nodes?filter\_path=\*\*.mlockall\&pretty"**
```
 **Output**  
**{**  
  **"nodes" : {**  
    **"sRuGbIQRRfC54wzwIHjJWQ" : {**  
      **"process" : {**  
        **"mlockall" : true**  
      **}**  
    **}**  
  **}**  
**}**

**![][image3]**

**Repeat this stage of the installation process on every Wazuh indexer node in your multi node cluster. This ensures that memory locking is correctly configured across all Wazuh indexer nodes.**

## **Disable Wazuh updates**

**We recommend disabling the Wazuh package repositories after installing all components on this server to prevent accidental upgrades.**

**Execute the following command only after completing all installations:**

**APTYumDNF**  
```bash
**sed \-i "s/^deb /\#deb /" /etc/apt/sources.list.d/wazuh.list**  
**apt update**
```
## **Next steps**

**The Wazuh indexer is now successfully installed on your single-node or multi-node cluster, and you can proceed with installing the Wazuh manager. To perform this action, see the [Installing the Wazuh manager step-by-step](https://documentation.wazuh.com/5.0-beta/installation-guide/wazuh-manager/step-by-step.html) section.**

**To uninstall the Wazuh indexer, see [Uninstalling the Wazuh indexer](https://documentation.wazuh.com/5.0-beta/installation-guide/uninstalling-wazuh/central-components.html#uninstall-indexer).**


# WAZUH MANAGER INSTALLATION

**ges to run all the commands described below.**

## **Wazuh manager node installation**

**Follow these steps to install a single-node or multi-node cluster Wazuh manager.**

### **Adding the Wazuh repository**

**Note**

**If you are installing the Wazuh manager on the same host as the Wazuh indexer, you may skip these steps only if the Wazuh repository is already configured and enabled.**

**APTYumDNF**  

**Install the following packages if missing:**
```bash
 **apt-get install \-y gnupg apt-transport-https curl**
```
1. 

**Install the GPG key:**
```bash
 **curl \-s https\://packages-staging.xdrsiem.wazuh.info/key/GPG-KEY-WAZUH | gpg \--no-default-keyring \--keyring gnupg-ring:/usr/share/keyrings/wazuh.gpg \--import && chmod 644 /usr/share/keyrings/wazuh.gpg**
```
2. 

**Add the repository:**
```bash
 **echo "deb \[signed-by=/usr/share/keyrings/wazuh.gpg\] https\://packages-staging.xdrsiem.wazuh.info/pre-release/5.x/apt/ unstable main" | tee \-a /etc/apt/sources.list.d/wazuh.list**
```
3. 

**Update the packages information:**
```bash
 **apt-get update**
```
4. 

### **Installing the Wazuh manager**

**Install the Wazuh manager package.**

 **APTYumDNF**  
 ```bash
**apt-get \-y install wazuh-manager**
```
**I could not find 5 beta so i used the above**

1. 

### **Deploying certificates**

**Note**

**Make sure that a copy of the `wazuh-certificates.tar` file, created during the initial configuration step, is placed in your working directory.**

**Replace `<MANAGER_NODE_NAME>` with your Wazuh manager node certificate name, the same used in `config.yml` when creating the certificates. In our case, the node name is, `manager`. Then move the certificates to their corresponding location:**
```bash
 **NODE\_NAME=manager**  
 **mkdir /var/wazuh-manager/etc/certs**  
**tar \-xf wazuh-certificates.tar \-C /var/wazuh-manager/etc/certs/ ./\$NODE\_NAME.pem ./\$NODE\_NAME-key.pem ./root-ca.pem**  
**mv /var/wazuh-manager/etc/certs/\$NODE\_NAME.pem /var/wazuh-manager/etc/certs/indexer-connector.pem**  
**mv /var/wazuh-manager/etc/certs/\$NODE\_NAME-key.pem /var/wazuh-manager/etc/certs/indexer-connector-key.pem**  
**chown root:wazuh-manager \\**  
    **/var/wazuh-manager/etc/certs/root-ca.pem \\**  
    **/var/wazuh-manager/etc/certs/indexer-connector.pem \\**  
    **/var/wazuh-manager/etc/certs/indexer-connector-key.pem**  
**chmod 640 \\**  
    **/var/wazuh-manager/etc/certs/root-ca.pem \\**  
    **/var/wazuh-manager/etc/certs/indexer-connector.pem \\**  
    **/var/wazuh-manager/etc/certs/indexer-connector-key.pem**
```
1. 

### **Configuring the Wazuh indexer connection**

**Save the Wazuh indexer username and password into the Wazuh manager keystore using the wazuh-manager-keystore tool. Replace `<WAZUH_INDEXER_USERNAME>` and `<WAZUH_INDEXER_PASSWORD>` with the Wazuh indexer username and password:**
```bash
 **echo '\<WAZUH\_INDEXER\_USERNAME\>' | /var/wazuh-manager/bin/wazuh-manager-keystore \-f indexer \-k username**  
**echo '\<WAZUH\_INDEXER\_PASSWORD\>' | /var/wazuh-manager/bin/wazuh-manager-keystore \-f indexer \-k password**
```
1. **NOTE THE DEFAULT USERNAME AND PASSWORD FOR SAVING TO THE KEYSTORE**

    **The default Wazuh indexer connector credentials are `wazuh-manager`:`wazuh-manager`.**

**Edit `/var/wazuh-manager/etc/wazuh-manager.conf` file to configure the indexer connection.**

 **By default, the indexer settings have one host configured. It's set to `127.0.0.1` as highlighted below.**

 **\<indexer\>**  
  **\<hosts\>**  
    **\<host\>https\://127.0.0.1:9200\</host\>**  
  **\</hosts\>**  
  **\<ssl\>**  
    **\<certificate\_authorities\>**  
      **\<ca\>/var/wazuh-manager/etc/certs/root-ca.pem\</ca\>**  
    **\</certificate\_authorities\>**  
    **\<certificate\>/var/wazuh-manager/etc/certs/indexer-connector.pem\</certificate\>**  
    **\<key\>/var/wazuh-manager/etc/certs/indexer-connector-key.pem\</key\>**  
  **\</ssl\>**  
**\</indexer\>**

**![][image4]**

* **Replace `127.0.0.1` with your Wazuh indexer node IP address or hostname. You can find this value in the Wazuh indexer config file `/etc/wazuh-indexer/opensearch.yml`**  
  * **Ensure the Wazuh manager certificate and key name match the certificate files in `/var/wazuh-manager/etc/certs`.**

**If you are running a Wazuh indexer cluster infrastructure, add a `<host>` entry for each one of your Wazuh indexer nodes. For example, in a two-node configuration:**

 **\<hosts\>**  
  **\<host\>https\://10.0.0.1:9200\</host\>**  
  **\<host\>https\://10.0.0.2:9200\</host\>**  
**\</hosts\>**

2.  **The Wazuh manager prioritizes reporting to the first Wazuh indexer node in the list. It switches to the next node in case it is not available.**

### **Starting the Wazuh manager**

**Enable and start the Wazuh manager service.**

 **SystemdSysV Init**  
 ```bash
**systemctl daemon-reload**  
**systemctl enable wazuh-manager**  
**systemctl start wazuh-manager**
```
1. 

**Run the following command to verify the Wazuh manager status:**

 **SystemdSysV init**  
 ```bash
**systemctl status wazuh-manager**
```
2. 

**Your Wazuh manager node is now successfully installed. Repeat this stage of the installation process for every Wazuh manager node in your Wazuh cluster, then proceed with configuring the Wazuh cluster. If you want a Wazuh manager single-node cluster, everything is set and you can proceed directly with [Installing the Wazuh dashboard step by step](https://documentation.wazuh.com/5.0-beta/installation-guide/wazuh-dashboard/step-by-step.html).**

## **Cluster configuration for multi-node deployment**

**After completing the installation of the Wazuh manager on every node, you need to configure one server node only as the master and the rest as workers.**

### **Configuring the Wazuh manager master node**

**Edit the following settings in the `/var/wazuh-manager/etc/wazuh-manager.conf` file and configure the necessary parameters:**
```bash
 **\<cluster\>**  
  **\<name\>wazuh\</name\>**  
  **\<node\_name\>master-node\</node\_name\>**  
  **\<node\_type\>master\</node\_type\>**  
  **\<key\>c98b62a9b6169ac5f67dae55ae4a9088\</key\>**  
  **\<port\>1516\</port\>**  
  **\<bind\_addr\>0.0.0.0\</bind\_addr\>**  
  **\<nodes\>**  
    **\<node\>\<WAZUH\_MASTER\_ADDRESS\>\</node\>**  
  **\</nodes\>**  
  **\<hidden\>no\</hidden\>**  
**\</cluster\>**
```
**![][image5]**

1.
**Restart the Wazuh manager.**

 **SystemdSysV Init**  
 ```bash
**systemctl restart wazuh-manager**
```
2. 

**Restart the Wazuh manager.**

 **SystemdSysV Init**  
 ```bash
**systemctl restart wazuh-manager**
```
1. 

> **Repeat these configuration steps for every Wazuh manager worker node in your cluster.**

### **Testing Wazuh manager cluster**

**Run the following command to verify that the Wazuh cluster is enabled and all the nodes are connected:**
```bash
**/var/wazuh-manager/bin/cluster\_control \-l**
```
**An example output of the command looks as follows:**

**Output**  
**NAME         TYPE    VERSION  ADDRESS**  
**master-node  master  5.0.0    10.0.0.3**  
**worker-node1 worker  5.0.0    10.0.0.4**  
**worker-node2 worker  5.0.0    10.0.0.5**

**![][image6]**

**Note that the IP addresses `10.0.0.3`, `10.0.0.4`, and `10.0.0.5` are used as examples.**

## **Disable Wazuh updates**

**We recommend disabling the Wazuh package repositories after installing all components on this server to prevent accidental upgrades.**

**Execute the following command only after completing all installations:**

**APTYumDNF**  
```bash
**sed \-i "s/^deb /\#deb /" /etc/apt/sources.list.d/wazuh.list**  
**apt update**
```


**WAZUH \- DASHBOARD INSTALATION**

**Install and configure the Wazuh dashboard following step-by-step instructions. The Wazuh dashboard is a web interface for mining and visualizing security data.**

**Note**

**You need root user privileges to run all the commands described below.**

# Wazuh dashboard installation

**Follow these steps to install the Wazuh dashboard.**

### **Installing package dependencies**

**Install the following packages if missing.**

 **APTYumDNF**  
 ```bash
**apt-get install \-y debhelper tar curl libcap2-bin \#debhelper version 9 or later**
```
1. 

### **Adding the Wazuh repository**

**Note**

**If you are installing the Wazuh dashboard on the same host as the Wazuh indexer or the Wazuh manager, you may skip these steps as you may have added the Wazuh repository already.**

**APTYumDNF**  

**Install the following packages if missing:**
```bash
 **apt-get install \-y gnupg apt-transport-https curl**
```
1. 

**Install the GPG key:**
```bash
 **curl \-s https\://packages-staging.xdrsiem.wazuh.info/key/GPG-KEY-WAZUH | gpg \--no-default-keyring \--keyring gnupg-ring:/usr/share/keyrings/wazuh.gpg \--import && chmod 644 /usr/share/keyrings/wazuh.gpg**
```
2. 

**Add the repository:**
```bash
 **echo "deb \[signed-by=/usr/share/keyrings/wazuh.gpg\] https\://packages-staging.xdrsiem.wazuh.info/pre-release/5.x/apt/ unstable main" | tee \-a /etc/apt/sources.list.d/wazuh.list**
```
3. 

**Update the packages information:**
```bash
 **apt-get update**
```
4. 

### **Installing the Wazuh dashboard**

**Install the Wazuh dashboard package.**

 **APTYumDNF**  
 ```bash
**apt-get \-y install wazuh-dashboard**
```
1. 

### **Configuring the Wazuh dashboard**

> 1. **Edit the `/etc/wazuh-dashboard/opensearch_dashboards.yml` file and replace the following values:**

>    1. **`server.host`: This setting specifies the host of the Wazuh dashboard server. To allow remote users to connect, set the value to the IP address or DNS name of the Wazuh dashboard server. The value `0.0.0.0` will accept all the available IP addresses of the host.**

**`opensearch.hosts`: The URLs of the Wazuh indexer instances to use for all your queries. The Wazuh dashboard can be configured to connect to multiple Wazuh indexer nodes in the same cluster. The addresses of the nodes can be separated by commas. For example, `["https://10.0.0.2:9200", "https://10.0.0.3:9200","https://10.0.0.4:9200"]`**

   **server.host: 0.0.0.0**  
   **server.port: 443**  
   **opensearch.hosts: https\://localhost:9200**  
   **opensearch.ssl.verificationMode: certificate**

> 2. 

**`wazuh_core.hosts.url`: This setting specifies the Wazuh manager master node. Replace `<WAZUH_MANAGER_IP_ADDRESS>` with the IP address or hostname of the Wazuh manager master node.**

  **wazuh\_core.hosts:**  
    **default:**  
      **url: https\://\<WAZUH\_MANAGER\_IP\_ADDRESS\>**  
      **port: 55000**  
      **username: wazuh-wui**  
      **password: wazuh-wui**  
      **run\_as: true**

**![][image7]**

### **Deploying certificates**

> **Note**

> **Make sure that a copy of `wazuh-certificates.tar` file, created during the initial configuration step, is placed in your working directory.**

**Replace `<DASHBOARD_NODE_NAME>` with your Wazuh dashboard node name, the same one used in the `config.yml` file to create the certificates. In our case, the node name is, `dashboard`. Then move the certificates to their corresponding location:**
```bash
 **NODE\_NAME= dashbord**  
 **mkdir /etc/wazuh-dashboard/certs**  
**tar \-xf ./wazuh-certificates.tar \-C /etc/wazuh-dashboard/certs/ ./\$NODE\_NAME.pem ./\$NODE\_NAME-key.pem ./root-ca.pem**  
**\[ \! \-e /etc/wazuh-dashboard/certs/dashboard.pem \] && mv \-n /etc/wazuh-dashboard/certs/\$NODE\_NAME.pem /etc/wazuh-dashboard/certs/dashboard.pem**  
**\[ \! \-e /etc/wazuh-dashboard/certs/dashboard-key.pem \] && mv \-n /etc/wazuh-dashboard/certs/\$NODE\_NAME-key.pem /etc/wazuh-dashboard/certs/dashboard-key.pem**  
**chmod 500 /etc/wazuh-dashboard/certs**  
**chmod 400 /etc/wazuh-dashboard/certs/\***  
**chown \-R wazuh-dashboard:wazuh-dashboard /etc/wazuh-dashboard/certs**
```
> 1. 

### **Starting the Wazuh dashboard service**

**Enable and start the Wazuh dashboard service.**

 **SystemdSysV Init**  
**systemctl daemon-reload**  
**systemctl enable wazuh-dashboard**  
**systemctl start wazuh-dashboard**

1.   
2. **After deployment, the web interface may take one to two minutes to become available while the Wazuh services finish initializing. Access the Wazuh web interface with your `admin` user credentials. This is the default administrator account for the Wazuh indexer and it allows you to access the Wazuh dashboard.**

   * **URL: `https://<WAZUH_DASHBOARD_IP_ADDRESS>`**  
   * **Username: `admin`**  
   * **Password: `admin`**  
3. **When you access the Wazuh dashboard for the first time, the browser shows a warning message stating that the certificate was not issued by a trusted authority. An exception can be added in the advanced options of the web browser. For increased security, the `root-ca.pem` file previously generated can be imported to the certificate manager of the browser.**

## **Securing your Wazuh installation**

**You have now installed and configured all the Wazuh central components. We recommend changing the default credentials to protect your infrastructure from possible attacks.**

**Select your deployment type and follow the instructions to change the default passwords for both the Wazuh API and the Wazuh indexer users.**

**All-in-one deploymentDistributed deployment**  
**Changing the password for a Wazuh indexer userChanging the password for a Wazuh manager API user**

**Wazuh indexer users are defined in `/etc/wazuh-indexer/opensearch-security/internal_users.yml`.**

**Download the Wazuh passwords tool:**
```bash
 **wget https\://packages-staging.xdrsiem.wazuh.info/pre-release/5.x/installation-assistant/wazuh-passwords-tool-5.0.0-beta5.sh**
```
1. 

**To change the password for a Wazuh indexer user, run the passwords tool with the `-u` option and indicate the new password with the `-p` option. The password must have a length between 8 and 64 characters and contain at least one upper case letter, one lower case letter, a number, and one of the following symbols: `.*+?-`.**
```bash
 **bash wazuh-passwords-tool-5.0.0-beta5.sh \-u \<USER\> \-p \<PASSWORD\>**
```
 **Where `<USER>` is the name of the user whose password you want to change and `<PASSWORD>` is the new password. If `<PASSWORD>` is not specified, the tool will generate a random password.**

 **For example, to change the password of the `admin` user to `Secr3tP4ssw*rd`, run the following command:**

 **bash wazuh-passwords-tool-5.0.0-beta5.sh \-u admin \-p Secr3tP4ssw\*rd**  
 **Output**

**10/04/2026 13:40:45 INFO: Updating the internal users.**  
**10/04/2026 13:41:04 INFO: A backup of the internal users has been saved in the /etc/wazuh-indexer/internalusers-backup folder.**  
**10/04/2026 13:41:05 INFO: Generating password hash**  
**10/04/2026 13:42:28 WARNING: Password changed. Remember to update the password in the Wazuh dashboard and the Wazuh manager nodes if necessary, and restart the services.**

2. 

## **Disable Wazuh updates**

**We recommend disabling the Wazuh package repositories after installing all components on this server to prevent accidental upgrades.**

**Execute the following command only after completing all installations:**

**APTYumDNF**  
```bash
**sed \-i "s/^deb /\#deb /" /etc/apt/sources.list.d/wazuh.list**  
**apt update**
```


# INSTALL GRAYLOG 

Install gnupg and curl:
```bash
1. **sudo apt-get install gnupg curl**
```
2. **Import the MongoDB public key:**

    **Copy**
   ```bash
    **curl \-fsSL https\://www\.mongodb.org/static/pgp/server-8.0.asc | \\**  
      **sudo gpg \-o /usr/share/keyrings/mongodb-server-8.0.gpg \\**  
      **\--dearmor**
     ```

4. **Create a list file for MongoDB:**

5. 

 **Copy**  
 ```
 **echo "deb \[ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg \] https\://repo.mongodb.org/apt/ubuntu noble/mongodb-org/8.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list**
```
5. **Reload the local package database:**

    **Copy**
   ```bash
    **sudo apt-get update**
    ```
7. **Install the latest stable version of MongoDB:**

    **Copy**
   ```bash
    **sudo apt-get install \-y mongodb-org**
    ```
9. **Hold the currently installed version of the MongoDB package to prevent it from being automatically upgraded to a newer version when updates are installed:**

    **Copy**
   ```
    **sudo apt-mark hold mongodb-org**
    ```
11. **Open the MongoDB configuration file:**

    **Copy**
    ```bash
    **sudo nano /etc/mongod.conf**
    ```
   **![][image8]**  
11. **By default, MongoDB only listens locally.You must modify either the `bindIp` or `bindIpAll` setting in the MongoDB configuration file so that the port binds to an interface address or a host name or listens on all interfaces. See the example configurations below.**

    **To listen on all interfaces:**
```bash
    **Copy**  
  **
    **net:**  
     **port: 27017**  
     **bindIpAll: true**
    ```
    **To bind to a specific interface, like `192.168.50.71`:**

   **Copy**  
    **net:**  
     **port: 27017**  
     **bindIp: 192.168.50.71**

   **To bind to a host name, like `graylog01`:**

   **Copy**  
    **net:**  
     **port: 27017**  
     **bindIp: graylog01**
```
12. **Enable MongoDB and start the service:**

     **Copy**
    ```
     **sudo systemctl daemon-reload**  
    **sudo systemctl enable mongod.service**  
    **sudo systemctl start mongod.service**
    ```

## [**Install Data Node**](https://go2docs.graylog.org/current/downloading_and_installing_graylog/ubuntu_installation.htm#InstallDataNode)**🔗**

**Data Node is a component in Graylog's architecture designed to handle log ingestion, processing, and indexing, managing communication with OpenSearch for storing and querying logs efficiently. As noted in the Core architecture, the Data Node service should be maintained on its own node, separate from Graylog and MongoDB.**

**Warning: The following guide will walk you through installing Graylog for use with Data Node as your search backend. Do not install OpenSearch directly\! For information on deploying Graylog with self-managed OpenSearch, see [Installing Graylog](https://go2docs.graylog.org/current/downloading_and_installing_graylog/installing_graylog.html#Graylog).**

**To install Data Node, we recommend you follow the process below:** 

1. **Install the Data Node package:**

    **Copy**
   ```bash
    **wget https\://packages.graylog2.org/repo/packages/graylog-7.1-repository\_latest.deb**  
   **sudo dpkg \-i graylog-7.1-repository\_latest.deb**  
   **sudo apt-get update**  
   **sudo apt-get install graylog-datanode**
   ```

3. **Ensure that the Linux setting `vm.max_map_count` is set to at least `262144`. To check the current value:**

    **Copy**
   ```bash
    **cat /proc/sys/vm/max\_map\_count**
   ```
   **![][image9]**

    **To increase the value:**

    **Copy**
   ```bash
    **echo 'vm.max\_map\_count=262144' | sudo tee \-a /etc/sysctl.d/99-graylog-datanode.conf**  
   **sudo sysctl \--system**  
   **cat /proc/sys/vm/max\_map\_count**
   ```

5. **Create your `password_secret`. This is a secure, randomly generated string used to encrypt sensitive data within the system:**

    **Copy**
   ```bash
    **openssl rand \-hex 32**
   ```
    **Hint: This command uses OpenSSL, a toolkit for TLS/SSL protocols and cryptography, to generate a secure random password. See [the OpenSSL documentation](https://docs.openssl.org/master/) for more information.**

7. **Open the Data Node configuration file:**

    **Copy**
   ```bash
    **sudo nano /etc/graylog/datanode/datanode.conf**
     ```
9. **Add the `password_secret` value to the Data Node configuration file. Note that you must add this same value to the Graylog server configuration file in a later step since it is crucial that this value be the same for the Graylog node.**

10. **Ensure the heap settings are set to half your system memory, up to a max of 31 GB. To do so, you will need to add the following configuration property to your Data Node configuration file. For example, if you have 16 GB of RAM, you would set it to 8 GB, like in the example below:**

    **Copy**
    ```bash
    **opensearch\_heap \= 8g**

    **Warning: This configuration property is not included in the `datanode.conf` by default\! It must be added to the file manually.**
    ```
12. **Configure the MongoDB connection string in the Data Node configuration file. In the following example command, `graylog01` represents the host name of the MongoDB node:**

    **Copy**
    ```bash
    **mongodb\_uri \= mongodb://graylog01:27017/graylog**
    ```
14. **Enable Data Node and start the service:**

    **Copy**
    ```bash
    **sudo systemctl daemon-reload**  
    **sudo systemctl enable graylog-datanode.service**  
    **sudo systemctl start graylog-datanode**
    ```
    **Parameters to be configured:**

| [name](https://documentation.wazuh.com/5.0-beta/under-construction.html#cluster-name) | It indicates the name of the cluster. |
| :---- | :---- |
| [**node\_name**](https://documentation.wazuh.com/5.0-beta/under-construction.html#cluster-node-name) | **It indicates the name of the current node.** |
| [**node\_type**](https://documentation.wazuh.com/5.0-beta/under-construction.html#cluster-node-type) | **It specifies the role of the node. It has to be set to `master`.** |
| [**key**](https://documentation.wazuh.com/5.0-beta/under-construction.html#cluster-key) | **Key that is used to encrypt communication between cluster nodes. The key must be 32 characters long and same for all of the nodes in the cluster. You can use the following command to generate a random key: `openssl rand -hex 16`.** |
| [**port**](https://documentation.wazuh.com/5.0-beta/under-construction.html#cluster-port) | **It indicates the destination port for cluster communication.** |
| [**bind\_addr**](https://documentation.wazuh.com/5.0-beta/under-construction.html#cluster-bind-addr) | **It is the network IP to which the node is bound to listen for incoming requests (0.0.0.0 for any IP).** |
| [**nodes**](https://documentation.wazuh.com/5.0-beta/under-construction.html#cluster-nodes) | **It is the address of the master node and can be either an IP or a DNS. This parameter must be specified in all nodes, including the master itself.** |
| [**hidden**](https://documentation.wazuh.com/5.0-beta/under-construction.html#cluster-hidden) | **It shows or hides the cluster information in the generated findings.** |
 
   **So configuration of  wazuh- indexer to  graylog config was becoming impossible because at the moment graylog does not support 0pensearch 3.0 and above so i configured it to the datanode: for elastic hosts configuration.**

**![][image10]**

## [**Install Graylog**](https://go2docs.graylog.org/current/downloading_and_installing_graylog/ubuntu_installation.htm#InstallGraylog)**🔗**

**After Data Node installation is complete, you must install the core Graylog service. The Core architecture model is designed so that Graylog and MongoDB are installed on the same node.**

**To install Graylog, we recommend you follow the process below:** 

1. **On your Graylog/MongoDB node, install the Graylog package.**

    [**![Closed][image11]For Graylog Open ▼**](https://go2docs.graylog.org/current/downloading_and_installing_graylog/ubuntu_installation.htm#)  
    ```bash
    sudo apt-get install graylog-server 
    ```
    [**![Closed][image12]For Graylog Enterprise ▼**](https://go2docs.graylog.org/current/downloading_and_installing_graylog/ubuntu_installation.htm#)

    [**![Closed][image13]For Graylog Security ▼**](https://go2docs.graylog.org/current/downloading_and_installing_graylog/ubuntu_installation.htm#)

3. **Use the following command to create your `root_password_sha2`. This is the password for the root administrator account for the Graylog interface. Make sure you record this password as you will need it to log into the Graylog interface after preflight configuration:** 

    **Copy**
   ```bash 
    **echo \-n "Enter Password: " && head \-1 \</dev/stdin | tr \-d '\\n' | sha256sum | cut \-d" " \-f1**
   ```
    **Warning: Do NOT attempt to log into Graylog for the first time using the password you generated in the steps above\! You must complete the preflight login with the credentials found in the log file after first starting the Graylog service. You will be able to login to Graylog with your generated password after the preflight is complete. See [The Web Interface](https://go2docs.graylog.org/current/setting_up_graylog/web_interface.htm#Prefligh) for more information.**

5. **Open the Graylog server configuration file:**

    **Copy**
   ```bash
    **sudo nano /etc/graylog/server/server.conf**
    ```
   ** NOTE I CONFIGURED MY INDEXER TO THE DATANODE BECAUSE OF COMPATIBILITY ISSUES BETWEEN WAZUH5'S OPENSEARCH AND GRAYLOG.
7. **Enter the value you created for the `root_password_sha2` in the previous step into the Graylog configuration file.**

8. **Retrieve the password secret from the Data Node configuration file as indicated [in steps 3-5 of Install Data Node](https://go2docs.graylog.org/current/downloading_and_installing_graylog/ubuntu_installation.htm#3.) and add it to the `password_secret` property in the Graylog configuration file.**

9. **Set the `http_bind_address` value in the Graylog configuration file to the public host name or a public IP address on which the Graylog web and API server will listen for incoming HTTP requests. (This property is commented out by default and listed beneath the `# HTTP settings` section of the configuration file):** 

    **Copy**
   ```bash
    **http\_bind\_address \= 0.0.0.0:9000**
   ```
    **Hint: More information about these settings can be found in [The Web Interface](https://go2docs.graylog.org/current/setting_up_graylog/web_interface.htm).**

11. **Adjust your journal settings. We recommend you configure your journal settings' max age to 72 hours and the size to your expected total log volume over a 72-hour period. So, if your expected daily log volume is 30 GB, your max size should be adjusted to 90 GB, as in the following example:**

    **Copy**  
    **message\_journal\_max\_age \= 72h**  
   **message\_journal\_max\_size \= 90gb**

12. **Open the `graylog-server` file found by default at `/etc/default/`:**

    **Copy**
    ```bash
    **sudo nano /etc/default/graylog-server**
    ```
   **NOTE : So  I  created a  certs directory for our java moved the wazuh root ca into it and created graylog certs also we moved all this into the java keystore file:**  
   **NOTE THE BELOW BUT FOR OUR VERSION OF GRAYLOG:**  
   
```bash
| mkdir /etc/graylog/server/certs |
| :---- |
| **cp \-a /usr/lib/jvm/java-21-openjdk-amd64/lib/security/cacerts /etc/graylog/server/certs/cacerts** |
| **keytool \-importcert \-keystore /etc/graylog/server/certs/cacerts \-storepass changeit \-alias root\_ca \-file /etc/graylog/server/certs/rootCA.crt** |
```
   **![][image14]**

9. **In the `graylog-server` file, adjust your heap settings to half the system memory up to a max of 16 GB for the Graylog service, as recommended in [Additional Configuration](https://go2docs.graylog.org/current/setting_up_graylog/additional_configuration.htm#JVM). It is recommended that you set the minimum and maximum values to be the same, so if you are setting your minimum to 2 GB, like shown in `-Xms2g`, and your maximum to 2 GB, like shown in `-Xmx2g`, the setting may look like:** 

    **Copy**
   ```bash
    **GRAYLOG\_SERVER\_JAVA\_OPTS="-Xms1536g \-Xmx1536g \-server \-XX:+UseG1GC \-XX:-OmitStackTraceInFastThrow"**
   ```
11. **Enable Graylog and start the service:**

     **Copy**
    ```bash
     **sudo systemctl daemon-reload**  
    **sudo systemctl enable graylog-server.service**  
    **sudo systemctl start graylog-server.service**
    ```
    
**NOTE ON THE UI YOU FIRST CREATE AND DEPLOY A CERTS AUTHORITY THIS CAUSED A MISMATCH WITH OUR ALREADY CREATED CERTS SO WE HAD TO TROUBLE SHOOT THAT AND MAKE INDEXER TRUST OUR CERTS**

**ON GRAYLOG WE CREATED INPUTS WHICH IS WHAT GRAYLOG USES TO GET INFO FROM FLUENT BIT** 

**GO TO** 

**SYSTEMS \-INPUTS LAUNCH NEW INPUT:**

**![][image15]**

#INSTALLING FLUENT-BIT

## **Server GPG key**

**Add the Fluent Bit server GPG key to your keyring to ensure you can get the correct signed packages.**

**Follow the official [Debian wiki guidance](https://wiki.debian.org/DebianRepository/UseThirdParty#OpenPGP_Key_distribution).**

**Copy**
```bash
**sudo sh \-c 'curl https\://packages.fluentbit.io/fluentbit.key | gpg \--dearmor \> /usr/share/keyrings/fluentbit-keyring.gpg'**
```
## **Update your sources lists**

**On Ubuntu, you need to add the Fluent Bit APT server entry to your sources lists. Ensure `codename` is set to your specific [Ubuntu release name](https://wiki.ubuntu.com/Releases). For example, `focal` for Ubuntu 20.04.**

**Copy**
```bash

**codename=\$(grep \-oP '(?\<=VERSION\_CODENAME=).\*' /etc/os-release 2\>/dev/null || lsb\_release \-cs 2\>/dev/null)**
```
**Update your source's list:**

**Copy**
```bash
**echo "deb \[signed-by=/usr/share/keyrings/fluentbit-keyring.gpg\] https\://packages.fluentbit.io/ubuntu/\$codename \$codename main" | sudo tee /etc/apt/sources.list.d/fluent-bit.list**
```
### **Update your repositories database**

**Update the `apt` database on your system:**

**Copy**
```bash
**sudo apt-get update**
```
**Fluent Bit recommends upgrading your system to avoid potential issues with expired certificates:**
```bash
**`sudo apt-get upgrade`**
```
**If you receive the error `Certificate verification failed`, check if the package `ca-certificates` is properly installed:**
```bash
**`sudo apt-get install ca-certificates`**
```
## **Install Fluent Bit**

1. **Ensure your [GPG key](https://docs.fluentbit.io/manual/installation/downloads/linux#gpg-key-updates) is up to date.**  
2. **Use the following `apt-get` command to install the latest Fluent Bit:**  
   **Copy**
   ```bash
   **sudo apt-get install fluent-bit**
   ```

4. **Instruct `systemd` to enable the service:**  
   **Copy**
   ```bash
   **sudo systemctl start fluent-bit**
    ```
**If you do a status check, you should see a similar output like this:**

**Copy**
```bash
**\$ systemctl status fluent-bit**
```
**● fluent-bit.service \- Fluent Bit**

   **Loaded: loaded (/lib/systemd/system/fluent-bit.service; disabled; vendor preset: enabled)**

   **Active: active (running) since mié 2016-07-06 16:58:25 CST; 2h 45min ago**

 **Main PID: 6739 (fluent-bit)**

    **Tasks: 1**

   **Memory: 656.0K**

      **CPU: 1.393s**

   **CGroup: /system.slice/fluent-bit.service**

           **└─6739 /opt/fluent-bit/bin/fluent-bit \-c /etc/fluent-bit/fluent-bit.conf**

**...**

**The default configuration of `fluent-bit` is collecting metrics of CPU usage and sending the records to the standard output. You can see the outgoing data in your `/var/log/syslog` file.**


**NOTE THE  WAZUH 5.0 DOES NOT HAVE THE TRADITIONAL `/var/ossec/logs/alerts/alerts.json so we used  /var/wazuh-manager/logs/standard-wazuh-events-v5/*/*/wazuh-standard-wazuh-events-v5-*.json`**

**`So my fluent-bit became:`**

**`![][image16]`**

**`ON GRAYLOG WE ALSO CREATED A STREAM, AN EXTRACTOR ,AND A WAZUH ALERTS INDEX`**

**`![][image17]`**

**`![][image18]`**

**`![][image19]`**

**`ALSO:
```bash
sudo tail -n 80 /var/log/td-agent-bit.log`**
```
**`![][image20]`**




# NVIDIA API PROVIDER`


**`For your Wazuh 5 AI Assistant, NVIDIA is promising because its hosted inference API uses an OpenAI-compatible interface, and NVIDIA documents support for tool calling. 

## **`Step 1 — Get your NVIDIA API key`**

1. **`Open the official NVIDIA GLM-5.3 model page.`**  
2. **`Sign in or create your NVIDIA Developer account.`**  
3. **`Click Generate API Key.`**  
4. **`Follow the prompts to create the key and copy it somewhere secure.`**

**`NVIDIA's model page confirms the exact API model ID is z-ai/glm-5.3, the API endpoint is https://integrate.api.nvidia.com/v1, and a free endpoint is currently available. It also advertises tool calling. (NVIDIA NIM APIs)`**


## **`Step 2 — Add NVIDIA to Wazuh`**


**`Use these values:`**

| `Setting` | `Value` |
| ----- | ----- |
| **`Provider type`** | **`openai_compatible`** |
| **`Base URL`** | **`https://integrate.api.nvidia.com/v1`** |
| **`Model`** | **`z-ai/glm-5.3`** |
| **`API key`** | **`Your NVIDIA API key`** |

**`Save the provider and run its connection test.`**

## **`Step 3 — Test real Wazuh data`**

**`If the connection test succeeds, ask the assistant:`**

> **`Query the Wazuh findings from the last 24 hours. Report the total number of findings and list the top three rules by occurrence, including each rule ID, description, severity, and affected agent. Retrieve the information from Wazuh; do not invent or estimate any values.`**

**`Check that the response contains real findings, rule IDs, and agents. A successful connection test alone is not enough.`**

 

#THE MODEL z-ai/glm-5.3  failed the provider test so we changed it to  z-ai/glm-5.3-flash

# NVIDIA TERMINAL TESTS BEFORE WE CHANGED THE MODEL  THIS CAN BE USED TO TEST **`z-ai/glm-5.3-flash`**



## Run this test on wazuh5

# Test to confirm  **NVIDIA API key, network connection, endpoint, and model are working**. 

**`Log in to the Wazuh server terminal and copy the entire command below. It tests NVIDIA directly, without changing your Wazuh configuration.`**
```bash
**`read -rsp "Paste your NVIDIA API key: " NVIDIA_API_KEY`**

**`echo`**

**`umask 077`**

**`curl -sS \`**

  **`-o /tmp/nvidia-api-test.json \`**

  **`-w 'HTTP status: %{http_code}\n' \`**

  **`https://integrate.api.nvidia.com/v1/chat/completions \`**

  **`-H "Authorization: Bearer ${NVIDIA_API_KEY}" \`**

  **`-H "Content-Type: application/json" \`**

  **`-d '{`**

    **`"model": "z-ai/glm-5.3",`**

    **`"messages": [`**

      **`{`**

        **`"role": "user",`**

        **`"content": "Reply with exactly NVIDIA_OK"`**

      **`}`**

    **`],`**

    **`"max_tokens": 128,`**

    **`"stream": false`**

  **`}'`**

**`unset NVIDIA_API_KEY`**

**`if command -v jq >/dev/null 2>&1; then`**

  **`jq '{`**

    **`error: .error,`**

    **`model: .model,`**

    **`finish_reason: .choices[0].finish_reason,`**

    **`answer: .choices[0].message.content,`**

    **`answer_present: ((.choices[0].message.content // "") != ""),`**

    **`reasoning_present: ((.choices[0].message.reasoning_content // "") != "")`**

  **`}' /tmp/nvidia-api-test.json`**

**`else`**

  **`cat /tmp/nvidia-api-test.json`**

**`fi`**
```
**`Your API key is entered without displaying it, and the command does not print it. The response is saved locally with restricted file permissions.`**

# Next test — Check NVIDIA's tool-calling ability`**
```bash
**`read -rsp "Paste your NVIDIA API key: " NVIDIA_API_KEY`**

**`echo`**

**`curl -sS \`**

  **`-o /tmp/nvidia-tool-test.json \`**

  **`-w 'HTTP status: %{http_code}\n' \`**

  **`https://integrate.api.nvidia.com/v1/chat/completions \`**

  **`-H "Authorization: Bearer ${NVIDIA_API_KEY}" \`**

  **`-H "Content-Type: application/json" \`**

  **`-d '{`**

    **`"model": "z-ai/glm-5.3",`**

    **`"messages": [`**

      **`{`**

        **`"role": "user",`**

        **`"content": "Use the search_wazuh_findings tool to find security findings from the last 24 hours. Do not answer from memory."`**

      **`}`**

    **`],`**

    **`"tools": [`**

      **`{`**

        **`"type": "function",`**

        **`"function": {`**

          **`"name": "search_wazuh_findings",`**

          **`"description": "Search Wazuh security findings using a query.",`**

          **`"parameters": {`**

            **`"type": "object",`**

            **`"properties": {`**

              **`"time_range": {`**

                **`"type": "string",`**

                **`"description": "The time range to search, such as last 24 hours."`**

              **`}`**

            **`},`**

            **`"required": ["time_range"]`**

          **`}`**

        **`}`**

      **`}`**

    **`],`**

    **`"tool_choice": "auto",`**

    **`"max_tokens": 256,`**

    **`"stream": false`**

  **`}'`**

**`unset NVIDIA_API_KEY`**

**`jq '{`**

  **`error: .error,`**

  **`finish_reason: .choices[0].finish_reason,`**

  **`answer: .choices[0].message.content,`**

  **`tool_calls: .choices[0].message.tool_calls,`**

  **`reasoning_present: ((.choices[0].message.reasoning_content // "") != "")`**

**`}' /tmp/nvidia-tool-test.json`**
```

1. **`Text generation: HTTP 200, with the expected answer NVIDIA_OK.`**  
2. **`Tool calling: HTTP 200, with a valid function call and arguments:`**  
   * **`Tool: search_wazuh_findings`**  
   * **`Argument: time_range = "last 24 hours"`**

**`That means the NVIDIA API can generate normal answers and request tools in the expected OpenAI-compatible format.`**


## **`Next: test NVIDIA's streaming response`**

**`Wazuh may process streaming responses differently from the ordinary JSON responses we just tested. NVIDIA supports both formats, so let's check streaming before changing models or adding anything. (NVIDIA Docs)`**

**`Run this on wazuh5:`**
```bash
**`read -rsp "Paste your NVIDIA API key: " NVIDIA_API_KEY`**

**`echo`**

**`curl -sS -N --max-time 90 \`**

  **`https://integrate.api.nvidia.com/v1/chat/completions \`**

  **`-H "Authorization: Bearer ${NVIDIA_API_KEY}" \`**

  **`-H "Content-Type: application/json" \`**

  **`-d '{`**

    **`"model": "z-ai/glm-5.3",`**

    **`"messages": [`**

      **`{`**

        **`"role": "user",`**

        **`"content": "Reply with exactly NVIDIA_STREAM_OK"`**

      **`}`**

    **`],`**

    **`"max_tokens": 256,`**

    **`"stream": true`**

  **`}' | tail -n 12`**

**`unset NVIDIA_API_KEY`**
```bash
