Title: Managing fleet on Kubernetes
Date: 2017-05-02 00:10:
Category: kubernetes, docker, gce, gcr, container
Tags: kubernetes, docker, gce, gcr, container
Author: Sunny Kr Gupta

Couple of months ago, we were struggling with scalability of system and were in pursuit of finding right orchestration tools which can help in scaling modules.

Then, we started exploring popular project managed by Google for orchestration management, Kubernetes for DevOps. Starting with two weeks of learning curves, we get our working staging system in kubes (kubernetes in short) and did small working setup to visualize the power of this orchestration framework.

We started with GCE (Google Container Engine) to get things working quickly. We created a cluster of 10 Nodes, each Node with configuration 4 vCore and 15 GB in default pool to run stateless Java components (in Shieldsquare core processing relies on code written in Java).

Before we go in depth, we did some research and found out we needed some gears(concepts/tools/theory) before board into container ship and sail out for cruise. We are dividing gears we need to know into two parts, ie, first will be Docker and second will focus on Kubernetes.

Part - I (Understanding Docker at Dock)
- Stateless and stateful components.
- Understanding containerization concept.
- Writing good Dockerfile for modules.
- Writing Optimized Dockerfile, understanding order of dynamic commands (ie, commands that we will change according to need for making other docker images) and commands that we will keep same in all Docker images. It helps in quick building of next Docker image. Each command that we run in Dockerfile is executed as a layer and subsequent command will be build on top of previous layer. Each layer is managed in cache by Docker tool. Docker manages cache itself to reuse layer of previously build Docker images to save time, network bandwidth & disk.

------------------Ex :


- Running a single process inside a Docker container
- Understanding remote Docker container registry for storing/pushing our locally built docker images, here we have used Google container registry (GCR) for docker image management.



Part - II (Understanding Kubernetes fleet)
- Learning basics of kubernetes & working flow
- What are Pods! How container runs inside a pod.
- What are Nodes (also known as worker or minion, a single machine)
- What are deployments!
- What is replication controller and Replica sets!
- What is Kubernetes master!
- What are services!
- What is label selectors!
- How to debug or get cluster info from command-line!
    ---------kubectl commands


> How do we run containers in GCE ?
We have number of deployments which manages scaling pods up/down depend on processing we need. We need to follow proper versioning of modules to distinguish what is running inside your system and this helps in rollback releases in case of issues in production.
    How about services/APIs we need to expose ?
- There comes kubes services. We have plenty of APIs we need to expose to outside world. To make it happen, we have couple of kube services exposed using tcp loadbalancer which has been assigned public IP. Internally, these services keeps on doing service discovery using label selector to find pods and attached to this service, pods having same label will be targeted by a service. Its same concept of how we manage loadbalancer on cloud, attach VMs to a loadbalancer to offload incoming traffic.

- Resources running inside Kube ship know each other very well. Each services/pods can communicate by names assigned to each. Instead of using IPs (private) assigned to each of them, you can use names as FQDN given and its a good practise to use names instead of IPs because of dynamic allocation of IPs as resources get destroyed and created again. Kube-DNS maintains all list of IPs internally assigned and helps finding resources by names.


> How to decide what resources you should allocate to your kubernetes Cluster or define pools resources?
[http: // Setting pods CPU and Memory limits (M vs Mi)]

Each container has its own requirements of resources (ie, CPU or RAM, disk, network etc), there comes requests & limits in kubes. This helps alot in keeping your nodes healthy. Many times due to bad limits or not defining limits, your pods can go crazy at utilization, eat any resources and can lead to node starvation and lead to Node becomes unhealthy and goes in [Not Ready] state due to resource exhaustion. We had this multiple times at early stage and now we had fine tuned each pods resources based on its hunger behaviour.

    How to define Node resources?
Depends on container type (which you are running inside a pod), you can define different resource pools. Suppose you have modules named Core.X, Core.Y and Core.Z , all of them needs 2 core, 2 GB each to run, then you can have Standard Node Pool to run them. In this case, i will allocate below config for my Node pool.

- Name : Standard Pool
- Pool Size : 2
- Node Config: 4 Core, 4 GB
- Node Pool Size : 8 Core, 8 GB
- Utilization : 6 Core, 6 GB (75 % used Core & RAM)

Now, lets say i have high memory eater modules. let call them Mem.X, Mem.Y and Mem.Z , all of them needs 0.5 core, 4 GB each to run, then you need high memory Node Pool to run them. In this case, i will allocate below config for my Node pool.

- Name : HighMem Pool
- Pool Size : 2
- Node Config : 1 Core, 8 GB
- Node Pool : 2 Core, 16 GB
- Utilization : 1.5 Core, 12 GB (75 % used Core & RAM)


So, based on your Node types, you can deploy your pods in different Node pools by using Node selector in kube.

-------------- Node selector example



Note : Some configuration in GCE should be taken care, like autoupgrade kubernetes version. If you are running redis or any other cache manager that needs uptime, better you turn off autoupgrade because when kubernetes release comes all node will go on scheduled maintenance one by one and that could affect your production system. Else, you are fully stateless, you can keep default.

-------------- Autoupgrade off/on


Pretty much all above theories are based on what we understood in last three months of kubernetes running in production. Container management is easy to adapt and lot of new observation is yet to be discovered as we go along the way. We currently managed to put the system in place to process 10 Billion APIs call per month and are pushing more to handle.

Conclusion : Kubernetes lifted alot of DevOps management and helped in scaling system. Adaptability is much quicker, most of security and other concerns is being managed by Google. Kubernetes aims to offer a better orchestration management system on top of clustered infrastrcuture.
