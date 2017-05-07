Title: Kubernetes at Shieldsquare
Date: 2017-05-02 00:10:10
Category: kubernetes, docker, gce, gcr, container
Tags: kubernetes, docker, gce, gcr, container
Author: Sunny Kr Gupta
Status: draft

> Couple of months ago, we were struggling with scalability of system and were in pursuit of finding right orchestration tools which can help in scaling system quickly.

Then, we started exploring popular project managed by Google for orchestration management, **[Kubernetes](https://kubernetes.io/)** for DevOps. Starting with two weeks of learning curves, we get our working staging system in **_kubes_** <sub>(kubernetes in short)</sub> and did small working setup to visualize the power of this orchestration framework.

At **Shieldsquare** our pain point was scaling different version of modules on the fly and managing blue-green deployment. In our tradional model of scaling, we keep on adding server dependent on type of code we wanted to run on server (VMs) and it puts us in difficult situation when it comes to handling more traffic, we need to prepare servers to run different modules. At Shieldsquare, one advantage is we runs on purely decoupled services, each application service do transformation on data and transformed data is consumed by next service layer. We took advantage and started looking for technology that fits our requirement. We were in pursuit of moving our server management in _auto-pilot_ mode.

-------------------

#### Microservices

Microservice architectures have been trending because its architectural style aims to tackle the problems of managing modern application by decoupling software solutions into smaller functional services that are expected to fail.

This help in quick recovery from failure on smaller functional units in contrast to making recovery from big monolithic software systems. Microservices helps in making your release cycle faster even because you will be focusing on smaller changes in single app instead of pushing code changes in bigger software systems that has multiple dependencies.

----------------

#### Containers


Microservice architectures got a big tide in 2013 when Docker inc. released Docker technology. **Docker container** gave perfect replacement to virtual machines and drove software packaging methods in more developer friendly way. Docker container are comparatively smaller than virtual machines (VMs). Its shares underlying host OS resources, we can spin up hundreds of these small units in order of milliseconds. Their smaller size helps in faster packaging, testing and even deployments because of its portable nature.

Docker’s container-based platform allows for highly portable workloads. Docker containers can run on a developer’s local laptop, on physical or virtual machines in a data center, on cloud providers, or in a mixture of environments.

----------------

#### Launching on Kubernetes

We started with ```Google Container Engine (GCE)``` to get things working quickly. We started with a cluster of ```10 Nodes```, each Node with configuration ```4 vCore and 15 GB``` in **default pool** to run stateless Java components <sub>( Here at [Shieldsquare](https://www.shieldsquare.com/) core processing relies on code written in Java)</sub>.

When working with Kubernetes, we must become familiar with working concepts of ```Docker``` and ```Kubernetes```.

----------------

#### Understanding Docker

* [Understanding containerization concept](https://www.redhat.com/en/containers)
    - Container provides operating system-level virtualization through a virtual environment that has its own process and network space, instead of creating a full-fledged [virtual machine](https://en.wikipedia.org/wiki/Virtual_machine). This enables the kernel of an operating system to allow the existence of multiple isolated user-space instances, instead of just one.

* [Writing good Dockerfile for modules](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/).
    - Dockerfile is set of instruction used by Docker to build an image. Containers are created using docker images, which can be built either by executing commands manually or automatically through Dockerfile. Docker achieves this by creating safe, **LXC** (i.e. Linux Containers) based environments for applications called “docker containers”.


- [Running a single process inside a Docker container](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/#each-container-should-have-only-one-concern).
    * “one process per container” is frequently a good rule of thumb, it is not a hard and fast rule. Use your best judgment to keep containers as clean and modular as possible - Docker

- Understanding remote Docker container registry for storing/pushing our locally built docker images, here we have used Google container registry (GCR) for docker image management.
    * [Pushing and Pulling Images to GCR](https://cloud.google.com/container-registry/docs/pushing-and-pulling)
    * [Push images to Docker Cloud](https://docs.docker.com/docker-cloud/builds/push-images/)

----------------

#### Understanding Kubernetes

The Kubernetes documentation is great place to start.

 - Learning basics of kubernetes & [working flow training](https://kubernetes.io/docs/tutorials/kubernetes-basics/).
    * Kubernetes is an open-source platform for automating deployment, scaling, and operations of application containers across clusters of hosts, providing container-centric infrastructure - Kubernetes.io

> Defining correct Node resources in kubernetes cluster.

Each container has its own requirements of resources (ie, CPU or RAM, disk, network etc), there comes [requests & limits in kubes](https://kubernetes.io/docs/tasks/configure-pod-container/assign-cpu-ram-container/). This helps alot in keeping your nodes healthy. Many times due to bad limits or not defining limits on resources, your pods could go crazy at utilization, eat any resources which lead to node starvation and node goes in ```[Not Ready]``` state due to resource exhaustion. We had this multiple times at early stage and now we had fine tuned each pods resources based on its hunger behaviour.


Depends on container type <sub>(which you are running inside a pod)</sub>, you can define different Node pools. Suppose you have modules named ```Core-X, Core-Y and Core-Z``` , all of them needs ```2 Core, 2 GB``` each to run, then you can have **Standard Node Pool** to run them. In this case, i will allocate below config for my Node pool.

 - Name : Standard Pool
 - Pool Size : 2
 - Node Config: 4 Core, 4 GB
 - Node Pool Size : 8 Core, 8 GB
 - ```Utilization``` : 6 Core, 6 GB (75 % used Core & RAM)

Now, lets say i have high memory eater modules. let call them ```Mem-X, Mem-Y and Mem-Z``` , all of them needs ```0.5 Core, 4 GB``` each to run, then you need **High memory Node Pool** to run them. In this case, i will allocate now below config for my Node pool.

- Name : HighMem Pool
- Pool Size : 2
- Node Config : 1 Core, 8 GB
- Node Pool : 2 Core, 16 GB
- ```Utilization``` : 1.5 Core, 12 GB (75 % used Core & RAM)


> So, based on your [Node pool type](https://cloud.google.com/container-engine/docs/node-pools), you can deploy your pods in different Node pools by using ```nodeSelector``` directives in configuration.

```
-------------- Node selector example

apiVersion: v1
kind: Pod
metadata:
  name: nginx
  labels:
    env: test
spec:
  containers:
  - name: nginx-v1
    image: nginx
  nodeSelector:
    #give label assigned to your node pool
    cloud.google.com/gke-nodepool: high-mem-pool

```

----------------

#### Blue-green deployments in Shieldsquare

A blue-green deployment works by starting a cluster of replicas running the new version while all the old replicas are still serving all the live requests. When the new version of replicas is completely functioning, we switch the flip by decreasing the number of replicas of older version. A benefit of this approach, there is always only one version of application running, Its helps in reducing deployments complexity of handling multiple concurrent versions. If in any case, released version doesnt work out well in production, kubernetes maintains history of version rolled out, we can do rollback of deployments easily.

----------------

#### How we monitor Kubernetes

We have our custom monitoring monitoring setup to keep an eye on Nodes. We run a [heapster](https://github.com/kubernetes/heapster) responsible for compute resource usage analysis and monitoring of container clusters, hooked with [influxdb](https://github.com/influxdata/influxdb) that consumes reporting done by heapster and we visualize graphs in [grafana](https://grafana.com/).

<div style="text-align: right"><sub>Monitoring at Shieldsquare</sub></div>
![Grafana monitoring](/images/kubes/grafana.png "Grafana monitoring")


> Um! What about logs?

Right, logs are very important. We have ELK (Elasticsearch, Logstash, Kibana) to consume logs reported by containers running in cluster. Containers is running with [log4j](https://logging.apache.org/log4j) (log4j is a reliable, fast and flexible logging framework (APIs) written in Java,) configured to push logs through logstash to Elasticsearch.

```
#log4j configuration for application
log4j.rootLogger=ERROR, server

#We will use socket appender
log4j.appender.server=org.apache.log4j.net.SocketAppender

#Port where socket server will be listening for the log events
log4j.appender.server.Port=6083

#Host name or IP address of socket server
log4j.appender.server.RemoteHost=app-logstash.server.net

#Define any connection delay before attempting to reconnect
log4j.appender.server.ReconnectionDelay=10000
```

----------------

#### Data stores and Kubernetes

Kubernetes is more about running stateless containers. At shieldsquare, we mostly use kubernetes to run tools that don't need persistency ie, caching, temporary data. Its not meant for stateful components like, MySQL or MongoDB or any other engine that extensively work with data at rest. So, we are not running our production data stores inside Kubernetes. However, Kubernetes have support for stateful containers management too but still at mature stage. The important learning is that you don’t have to run everything in Kubernetes and orchestrate only applications which are stateless.

----------------

#### Cost Impact

With Kubernetes cluster, we brought down cost by 40% on Google Cloud Platform. We have managed to run tightly coupled containers inside a different node pools. We have plenty of services, some are core intensive and couple of them are memory hungry, we let kubernetes manage and fit the containers in right place without us worrying about how to maximize the utilization.


--------------


**Note :** Some configuration in GCE should be taken care, like ```autoupgrade kubernetes version```. If you are running RabbitMQ, Redis or any other message queue as service that needs uptime, better you turn off autoupgrade because kubernetes new version release comes, all node will be scheduled for maintenance, however it rolles updates one by one but could affect your production system. Else, if you are fully stateless, you can keep default or skip this warning!.

```
----Autoupgrade off

# https://cloud.google.com/container-engine/docs/node-auto-upgrade

gcloud beta container node-pools update <NODEPOOL> --cluster <CLUSTER> --zone <ZONE> --no-enable-autoupgrade

```

Pretty much all above understanding are based on what we learned in last four months of kubernetes running in production. Container management is easy to adapt and lot of new observation is yet to be discovered as we go along the way.

Looking at our deployments today, Kubernetes is absolutely fantastic. We currently managed to put the system in place to process ``5 Billion APIs``` call per month and are pushing more to handle.


------------

> Conclusion : ```Kubernetes``` lifted alot of ``` server management``` and helped in faster depployments & scaling system. Adaptability is much quicker, most of security and other concerns is being managed by Google. Kubernetes aims to offer a better orchestration management system on top of clustered infrastrcuture. Development on Kubernetes has been happening at storm-speed, and the [community of Kubernauts](https://kubernetes.io/community/) has grown bigger.
