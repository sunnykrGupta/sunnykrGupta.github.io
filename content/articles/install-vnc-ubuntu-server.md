Title: Installation of VNC server on Ubuntu
Date: 2017-09-04 22:51:50
Category: Blog
Tags: vnc, vncserver, ubuntu, desktop installation
Author: Sunny Kr Gupta
Status: published


This blog is intended for people who wanted to install GUI or desktop environment on linux [servers](https://en.wikipedia.org/wiki/Server_(computing)) running on [cloud](https://en.wikipedia.org/wiki/Cloud_computing) and connect.

We are going to use VNC (Virtual Network Computing) protocol for accessing our remote desktop server.


#### What is VNC ?

[Virtual network computing](https://en.wikipedia.org/wiki/Virtual_Network_Computing), or VNC, is a graphical desktop sharing system that allows you to control one computer remotely from another. A VNC server transfers keyboard and mouse events, and displays the remote host’s screen via a network connection, which allows you to operate a full [desktop environment](https://en.wikipedia.org/wiki/Desktop_environment).

Basically ubuntu server and ubuntu cloud editions does not contains GUI, which needs to be installed before installing VNC server. Please note that server and cloud editions are carefully designed to utilize less hardware resources ( minimal environment ), installing GUI might leads to high hardware utilization.



#### Why I needed desktop environment in remote server ?
Just to explain a use case, let me tell me you how I ended up using VNC in first place. I was working on a problem which relates with cloud latency testing. My Friend, [Neeraj](https://www.linkedin.com/in/neekneeraj/) *(whose work revolves around core JS research & development)* developed a javascript code that makes an cross origin [HTTP API]((https://en.wikipedia.org/wiki/Web_API)) call to a [loadbalancer](https://en.wikipedia.org/wiki/Cloud_load_balancing) near to the geographical location of browser and response will be delivered from loadbalancer in geographic proximity. To test this setup, executing JS code and to use [developer console](https://developer.mozilla.org/en/docs/Tools/Browser_Console) to see what's happening under the network layer, we were in need of a browser engine in different geographical location. I could have used some online paid or free service to get browser rented, services like [browserstack](https://www.browserstack.com/) or other alternatives but that has free minutes based trial restrictions.

-------------------


### Install a Desktop and VNC Server on Ubtunu 14.04

#### Step 1 - Install Ubuntu desktop

Start installing below *gnome packages* which helps VNC to load properly . These packages are required for all editions including *ubuntu desktop* .

```sh
$ sudo apt-get install --no-install-recommends ubuntu-desktop gnome-panel gnome-settings-daemon metacity nautilus gnome-terminal gnome-core
```

#### Step 2 - Install vnc4server package.

```sh
$ sudo apt-get install vnc4server
```


#### Step 3 - Make configuration changes in vncserver

Open ```/usr/bin/vncserver``` file and edit as follows . Before editing, make a backup copy.

```sh
$ sudo cp /usr/bin/vncserver /usr/bin/vncserver.bkp

$ sudo vim /usr/bin/vncserver

#Find this line "# exec /etc/X11/xinit/xinitrcnn".
#and add these lines like below

    "# exec /etc/X11/xinit/xinitrcnn".
       "gnome-panel &n".
       "gnome-settings-daemon &n".
       "metacity &n".
       "nautilus &n".
       "gnome-terminal &n".

```

#### Step 4 - Start your vncserver

Now type the command ```vncserver``` to start VNC session. you will be prompted for creating new vnc password.

```sh
$ vncserver
You will require a password to access your desktops through VNC Clients.
Password:******
Verify:******

xauth: file /root/.Xauthority does not exist
New 'ubuntu-desktop:1 (root)' desktop is ubuntu-desktop:1

Starting applications specified in /root/.vnc/xstartup
Log file is /root/.vnc/ubuntu-desktop:1.log
```

#### Step 5 - To check VNC server has started, follow

```sh
$ netstat -tulpn

Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:6001            0.0.0.0:*               LISTEN      28372/Xvnc4
tcp6       0      0 :::5901                 :::*                    LISTEN      28372/Xvnc4
```

> VNC server is running and listening on **5901 port**. Make sure your firewall allows **inbound** TCP connection to this port.


#### Step 6 - Configure your Firewall

If **firewall** is active, you need to open ports for inbound communication. If no firewall is enabled, you can skip this section.

```sh
#allow SSH
$ sudo ufw allow OpenSSH

#allowing single port 5901 port
$ sudo ufw allow 5901/tcp

#To allow series of port 5901 - 5910, follow
$ sudo ufw allow 5901:5910/tcp

#To check firewall rules
$ sudo  ufw status verbose

Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), disabled (routed)
New profiles: skip

To                         Action      From
--                         ------      ----
22/tcp (OpenSSH)           ALLOW IN    Anywhere
5901:5910/tcp              ALLOW IN    Anywhere
22/tcp (OpenSSH (v6))      ALLOW IN    Anywhere (v6)
5901:5910/tcp (v6)         ALLOW IN    Anywhere (v6)WW
```

> **[Good reads on configuring UFW firewall](https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-with-ufw-on-ubuntu-14-04)**


#### Step 7 - Connect to VNC Server

> Use any remote desktop connect client that allow VNC protocol. Use *[IP address](https://en.wikipedia.org/wiki/IP_address)* of server along with port where VNC server is listening.

<div style="text-align: right"><sub>Connect -Remote Desktop Viewer</sub></div>
![VNC Connect](/images/vnc/vnc-connect.png "VNC Connect")

> Once connected to your VNC server, you will see screen of remote server where you installed desktop GUI.

<div style="text-align: right"><sub>Launch Firefox from Terminal</sub></div>
![Launch Firefox](/images/vnc/vnc-launch-firefox.png "Launch Firefox")

> Browser screen running on remote server.

<div style="text-align: right"><sub>Google UK</sub></div>
![Google UK](/images/vnc/vnc-google-uk.png "Google UK")


That’s it, your VNC server is working.

> Here I created my linux server in london, UK. I opened firefox through terminal to reach out to URL *google.com*. It opened google.co.uk domain based on regional search engine. You can do lot of other stuffs on VNC protocol to get things done from remote location.

------------


##### Medium Blog : [medium.com/@sunnykrgupta/installation-of-vnc-server-on-ubuntu-1cf035370bd3](https://medium.com/@sunnykrgupta/installation-of-vnc-server-on-ubuntu-1cf035370bd3)


