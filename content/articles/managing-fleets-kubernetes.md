Title: Managing fleet on Kubernetes
Date: 2017-08-13 19:45:00
Category: kubernetes, docker, container
Tags: kubernetes, docker, gce, gcr, container
Author: Sunny Kr Gupta
Status: published

> Couple of months ago, we were tackling challenges with scalability of system and were in pursuit of finding right orchestration tools which can help in scaling system quickly. This draft is outline of things we have tried and learned along the way. A Quick glance of things we came across while building fleet on Kubernetes.

We started exploring popular project managed by Google for orchestration management, **[Kubernetes](https://kubernetes.io/)** for DevOps. Starting with two weeks of learning curves, we get our working staging system in _kubes_ (kubernetes in short) and did small working setup to visualize the power of this orchestration framework.


-------------------

#### Microservices

Microservice architectures have been trending because its architectural style aims to tackle the problems of managing modern application by decoupling software solutions into smaller functional services that are expected to fail.

This help in quick recovery from failure on smaller functional units in contrast to making recovery from big monolithic software systems. Microservices helps in making your release cycle faster even because you will be focusing on smaller changes in single app instead of pushing code changes in bigger software systems that has multiple dependencies.

----------------

#### Containers


Microservice architectures got a big tide in 2013 when Docker inc. released Docker technology. **Docker container** gave perfect alternatives to virtual machines and drove software packaging methods in a more developer friendly way. Docker container are comparatively smaller than virtual machines (VMs). Its shares underlying host OS resources, we can spin up hundreds of these small units in order of milliseconds. Their smaller size helps in faster packaging, testing and even deployments because of its portable nature.

Docker’s container-based platform allows highly portable workloads. Docker containers can run on a developer’s local laptop, on physical or virtual machines in a data center, on cloud providers, or in a mixture of environments.

----------------


We started with ```Google Container Engine (GCE)``` to get things work quickly. We started with a cluster with few ```10's of Nodes```, each Node with configuration ```12 vCore and 30 GB``` in **[default pool](https://cloud.google.com/container-engine/docs/node-pools)** to run stateless components.

Before we go in depth, we have done some research and found out we needed some _gears_ (concepts/tools/theory) before we board into container ship and sail out for cruise.

We are dividing gears that we need to know into two parts, ie, first will be ```Docker``` and second will focused on ```Kubernetes```.

-----------

#### Part - I (Understanding Docker at Dock)
* Stateless and stateful components.
    - In computing, a stateless protocol is a communications protocol in which no information is retained by either sender or receiver. The sender transmits a packet to the receiver and does not expect an acknowledgment of receipt. A UDP connection-oriented session is a stateless connection because neither systems maintains information about the session during its life.
    - In contrast, a protocol that requires keeping of the internal state on the server is known as a stateful protocol. A TCP connection-oriented session is a 'stateful' connection because both systems maintain information about the session itself during its life.

* [Understanding containerization concept](https://www.redhat.com/en/containers)
    - Container provides operating system-level virtualization through a virtual environment that has its own process and network space, instead of creating a full-fledged [virtual machine](https://en.wikipedia.org/wiki/Virtual_machine). This enables the kernel of an operating system to allow the existence of multiple isolated user-space instances, instead of just one.

* [Writing good Dockerfile for modules](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/).
    - Dockerfile is set of instruction used by Docker to build an image. Containers are created using docker images, which can be built either by executing commands manually or automatically through Dockerfile. Docker achieves this by creating safe, **LXC** (i.e. Linux Containers) based environments for applications called “docker containers”.

* Writing optimized Dockerfile, understanding order of commands. Each command that we run in Dockerfile is executed as a layer and subsequent command will be build on top of previous layer. Each layer is managed in cache by Docker tool. Docker manages cache itself to reuse layer of previously build Docker images to save time & disk.


```
I have three file in my directory named 'flask' :
➜  flask

── app.py
── Dockerfile
── requirement.txt
```

```
##### cat app.py

from flask import Flask
#from flask import render_template, request
import json

app = Flask(__name__)

@app.route("/")
def hello():
    return "Welcome to Python Flask!\n"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5009')

```
```
###### cat requirement.txt

Flask==0.10.1
```

```
###### cat Dockerfile

FROM frolvlad/alpine-python2

RUN mkdir /etc/flask

ADD app.py /etc/flask/app.py
ADD requirement.txt /etc/flask/requirement.txt


CMD ["python", "/etc/flask/app.py"]

```

> Lets build our docker image with name **flask-v1**

```
➜  docker build -t flask-v1 .

Sending build context to Docker daemon 4.096 kB

Step 1/5 : FROM frolvlad/alpine-python2
latest: Pulling from frolvlad/alpine-python2
627beaf3eaaf: Pull complete
79d39e719c2e: Pull complete
Digest: sha256:47e3f85dadf401d51c6f74a18d4f693c2157692292e6dae0a078f37499a183ee
Status: Downloaded newer image for frolvlad/alpine-python2:latest
 ---> 603e17608203

Step 2/5 : RUN mkdir /etc/flask
 ---> Running in 0d97b7a8986b
 ---> 9b2a858914e2
Removing intermediate container 0d97b7a8986b

Step 3/5 : ADD app.py /etc/flask/app.py
 ---> 1a4938be7722
Removing intermediate container f4d11b837e26

Step 4/5 : ADD requirement.txt /etc/flask/requirement.txt
 ---> 5d058851dd81
Removing intermediate container 08eef72a4051

Step 5/5 : CMD python /etc/flask/app.py
 ---> Running in 96490917e533
 ---> a081e6cbcf3c
Removing intermediate container 96490917e533

Successfully built a081e6cbcf3c
```

Now, we have made some modification in **app.py**

```
##### cat app.py

from flask import Flask
#from flask import render_template, request
import json

app = Flask(__name__)

@app.route("/")
def hello():
    return "Welcome to Python Flask!\n"

#Added utility
def utility():
    return "something"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5009')
```

> Lets build our docker image with name **flask-v2**

```
➜  docker build -t flask-v2 .

Sending build context to Docker daemon 4.096 kB

Step 1/5 : FROM frolvlad/alpine-python2
 ---> 603e17608203

Step 2/5 : RUN mkdir /etc/flask
 ---> Using cache
 ---> 9b2a858914e2

Step 3/5 : ADD app.py /etc/flask/app.py
 ---> a7565514aab3
Removing intermediate container 360eb266a458

Step 4/5 : ADD requirement.txt /etc/flask/requirement.txt
 ---> 8441bca383f0
Removing intermediate container 15ebbb15d67d

Step 5/5 : CMD python /etc/flask/app.py
 ---> Running in 73e4bbcbe512
 ---> 0f4a5754f0d0
Removing intermediate container 73e4bbcbe512

Successfully built 0f4a5754f0d0
```

You will see only *step-2* was taken from cache, rest of the instructions ran again because change has been detected by Docker on *step-3* command ie, ```ADD app.py``` , so all subsequent commands ran again to build layer on top of previous layer.


Now we have made changes in ```Dockerfile```, some reorder of commands.

```
# cat Dockerfile

FROM frolvlad/alpine-python2

RUN mkdir /etc/flask

# add requirement file first, then commands which contains some changes.
ADD requirement.txt /etc/flask/requirement.txt
ADD app.py /etc/flask/app.py

CMD ["python", "/etc/flask/app.py"]

```

> Lets build our docker image with name **flask-v3** and lets see build console.

```
➜  flask docker build -t flask-v3 .

Sending build context to Docker daemon 4.096 kB

Step 1/5 : FROM frolvlad/alpine-python2
 ---> 603e17608203

Step 2/5 : RUN mkdir /etc/flask
 ---> Using cache
 ---> 9b2a858914e2

Step 3/5 : ADD requirement.txt /etc/flask/requirement.txt
 ---> Using cache
 ---> db8fc95cebff

Step 4/5 : ADD app.py /etc/flask/app.py
 ---> 9fb8351616e1
Removing intermediate container 4e98534d5339

Step 5/5 : CMD python /etc/flask/app.py
 ---> Running in 139f8c4282d8
 ---> e3fae9852d94
Removing intermediate container 139f8c4282d8

Successfully built e3fae9852d94

```

Now, you can see only *step-2,3* was taken from ```cache```, *step-4* command ie, ```ADD app.py``` build new layer because of change detected in ```app.py``` file, and this build saved little bit of our time. This is really important in building big Docker images where we have bigger chain of command to build an app.



- [Running a single process inside a Docker container](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/#each-container-should-have-only-one-concern).
    * “one process per container” is frequently a good rule of thumb, it is not a hard and fast rule. Use your best judgment to keep containers as clean and modular as possible - Docker
- Understanding remote Docker container registry for storing/pushing our locally built docker images, here we have used Google container registry (GCR) for docker image management.
    * [Pushing and Pulling Images to GCR](https://cloud.google.com/container-registry/docs/pushing-and-pulling)
    * [Push images to Docker Cloud](https://docs.docker.com/docker-cloud/builds/push-images/)


---------------

#### Part - II ( Understanding Kubernetes in Ocean )

 - Learning basics of kubernetes & [working flow training](https://kubernetes.io/docs/tutorials/kubernetes-basics/).
    * Kubernetes is an open-source platform for automating deployment, scaling, and operations of application containers across clusters of hosts, providing container-centric infrastructure - Kubernetes.io

 - [What are Pods! How container run inside a pod!](https://kubernetes.io/docs/concepts/workloads/pods/pod/#what-is-a-pod)
    * Pods are the atomic unit on the Kubernetes platform. A Pod is a Kubernetes abstraction that represents a group of one or more application containers (such as Nginx or redis), and some shared resources for those containers.

<div style="text-align: right"><sub>Pod Overview : Images by Kubernetes.io</sub></div>
![Pods overview image](/images/kubes/module_03_pods.svg "Pods Overview")

 - [What are Nodes](https://kubernetes.io/docs/concepts/nodes/node/#what-is-a-node) <sub>(also known as worker or minion, a single machine)</sub>
    * A Pod always runs inside a Node. A Node is a worker machine in Kubernetes and may be either a virtual or a physical machine, depending on the cluster. Node is controlled by Kubernetes Master. Kubernetes manages scheduling of pods in Nodes running in a cluster.

<div style="text-align: right"><sub>Node Overview : Images by Kubernetes.io</sub></div>
![Node overview image](/images/kubes/module_03_nodes.svg "Node Overview")


 - [What are deployments!](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
    * Deployments to create new resources, or replace existing ones by new ones by means of configuration defined. You can think of it as a supervisor of pods management.


```
#### cat sample-deployment.yaml

apiVersion: apps/v1beta1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.7.9
      ports:
      - containerPort: 80
```

 - [What is replication controller and Replica sets!](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/)
    * A ReplicationController and Replica Sets ensures that a specified number of pod “replicas” are running at any one time. In other words, it makes sure that a pod or homogeneous set of pods are always up and available. If there are too many pods, it will kill some. If there are too few, it will start more.
    > In above ```yaml``` file, you can see ```replicas``` keyword, this is being managed by replication utility.

 - [What is Kubernetes master!](https://kubernetes.io/docs/concepts/overview/components/)
    * The controlling services in a Kubernetes cluster are called the master, or control plane, components. For example, master components are responsible for making global decisions about the cluster (e.g., scheduling), and detecting and responding to cluster events (e.g., starting up a new pod when a replication controller’s ‘replicas’ field is unsatisfied). Kubernetes provides a REST API supporting primarily CRUD operations on (mostly) persistent resources, which serve as the hub of its control plane.
    * [Kubernetes Ecosystem consists of mutiple components.](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/architecture.md#architecture)

 - [What are services!](https://kubernetes.io/docs/concepts/services-networking/service/)
    * A Kubernetes Service is an abstraction which defines a logical set of Pods and a policy by which to access them. The set of Pods targeted by a Service is (usually) determined by a Label Selector. Service keep on looking for pods which has specific labels assigned and keep tracks of those pods for request offloading.

<div style="text-align: right"><sub>Service Overview : Images by Kubernetes.io</sub></div>
![Service overview image](/images/kubes/module_04_labels.svg "Service Overview")


```
###### cat sample-services.yaml

kind: Service
apiVersion: v1
metadata:
  name: my-service
spec:
  type: LoadBalancer
  loadBalancerIP: 10.10.10.1
  ports:
    # the port that this service should serve on
  - port: 80
    # port on which it should forward request ie, port pod is listening
    targetPort: 8080
  selector:
    # labels assigned to pods
    app: MyApp

```

 - How to debug or [get cluster info from command-line!](https://kubernetes.io/docs/user-guide/kubectl-cheatsheet/)
    * ```kubectl``` is a command line interface for running commands against Kubernetes clusters.

```
-----General Commands

## To view Nodes in a cluster
$kubectl get nodes

NAME                                          STATUS    AGE
gke-test-cluster-default-pool-2d123aa1-012f   Ready     2d
gke-test-cluster-default-pool-2d123aa1-e23k   Ready     2d


## To view the Deployment we created run:
$    kubectl get deployments

NAME         DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
hello-node   1         1         1            1           3m


## To view the Pod created by the deployment run:
$    kubectl get pods

NAME                         READY     STATUS    RESTARTS   AGE
hello-node-714049816-ztzrb   1/1       Running   0          6m


## To view the Pod created by the deployment run:
$    kubectl get pods

NAME                         READY     STATUS    RESTARTS   AGE
hello-node-714049816-ztzrb   1/1       Running   0          6m

## To view detailed information of the Pod:
$ kubectl get pods -o wide
or
$ kubectl get pods --output=wide

NAME             READY     STATUS    RESTARTS   AGE       IP
dd-agent-0f75g   1/1       Running   0          23d       10.204.5.16


## To view the stdout / stderr from a Pod run:
$    kubectl logs <POD-NAME>

## To view metadata about the cluster run:
$    kubectl cluster-info

```

-------------

#### How do we run containers in GCE ?

We have number of ```deployments``` which manages scaling pods up/down depend on processing we need. Pods run containers inside Node available in a cluster. We need to follow proper versioning of modules to distinguish what is running inside your system and this helps in rollback releases in case of issues in production.

> How about services/APIs we need to expose ?

  - There comes kubes ```services```. We have plenty of APIs we need to expose to outside world. To make it happen, we have couple of kube services exposed using tcp loadbalancer which has been assigned public IP. Internally, these services keeps on doing service discovery using ```label selector``` to find pods and attach it to this service, pods having same label will be targeted by a service. Its same concept of how we manage loadbalancer on cloud, attach VMs to a loadbalancer to offload incoming traffic.

 - Resources running inside Kube ship knows each other very well. Each ```services/pods``` can communicate by names assigned to each. Instead of using IPs (private) assigned to each of them, you can use names given as FQDN and its a good practise to use names instead of IPs because of dynamic nature of network resource allocation and resources get destroyed and created again in a container lifecycle management. Kube-DNS maintains all list of IPs internally assigned and helps finding resources by names.


------------

#### How to decide what resources you should allocate to your [pods resources](https://kubernetes.io/docs/tasks/configure-pod-container/assign-cpu-ram-container/)?

```
Convention
# RAM : Mi = MB, ie, 1024Mi is 1024 MB or 1GB
# CPU : m = milicpu , ie, 100m cpu is 100 milicpu, or say 0.1 CPU

apiVersion: v1
kind: Pod
metadata:
  name: cpu-ram-demo
spec:
  containers:
  - name: cpu-ram-demo-container
    image: gcr.io/google-samples/node-hello:1.0
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
```

Each container has its own requirements of resources (ie, CPU, RAM, disk, network etc), there comes requests & limits in kubes. This helps in keeping your nodes healthy. Many times due to bad limits or not defining limits, your pods can go crazy at utilization, eat any resources and can lead to node starvation and lead to Node becomes unhealthy and goes in ```[Not Ready]``` state due to resource exhaustion. We had this multiple times at early stage and now we had fine tuned each pods resources based on its hunger behaviour.

##### How to define Node resources in kubernetes cluster?

Depends on container type <sub>(which you are running inside a pod)</sub>, you can define different Node pools. Suppose you have modules named ```Core.X, Core.Y and Core.Z``` , all of them needs ```2 core, 2 GB``` each to run, then you can have **Standard Node Pool** to run them. In this case, i will allocate following config for my Node pool.

 - Name : Standard Pool
 - Pool Size : 2
 - Node Config: 4 Core, 4 GB
 - Node Pool Resource : 8 Core, 8 GB
 - ```Utilization``` : 6 Core, 6 GB (75 % used Core & RAM)

Now, lets say i have high memory eater modules. let call them ```Mem.X, Mem.Y and Mem.Z``` , all of them needs ```0.5 core, 4 GB``` each to run, then you need **High memory Node Pool** to run them. In this case, i will allocate different config for my Node pool.

- Name : HighMem Pool
- Pool Size : 2
- Node Config : 1 Core, 8 GB
- Node Pool Resource : 2 Core, 16 GB
- ```Utilization``` : 1.5 Core, 12 GB (75 % used Core & RAM)


> So, based on your [Node pool type](https://cloud.google.com/container-engine/docs/node-pools), you can deploy your pods in different Node pools by using ```nodeSelector``` in kubes.

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

#### How we monitor Kubernetes ?

We can run custom monitoring setup to keep an eye on Nodes. You can run [heapster](https://github.com/kubernetes/heapster), ie. responsible for compute resource usage analysis and monitoring of container clusters, hooked with [influxdb](https://github.com/influxdata/influxdb) that consumes reporting pushed by heapster and can be visualized in [grafana](https://grafana.com/).

<div style="text-align: right"><sub>Monitoring in Grafana</sub></div>
![Grafana monitoring](/images/kubes/grafana.png "Grafana monitoring")


----------------



**Note :** Some configuration in GCE should be taken care, like ```autoupgrade kubernetes version```. If you are running RabbitMQ, Redis or any other message queue as service that needs uptime, better you turn off autoupgrade because kubernetes new version release will schedule all your node for maintenance, however it rolles updates one by one but could affect your production system. Else, if you are fully stateless, you can keep default or skip this warning!

```
----- Autoupgrade off

# https://cloud.google.com/container-engine/docs/node-auto-upgrade

gcloud beta container node-pools update <NODEPOOL> --cluster <CLUSTER> --zone <ZONE> --no-enable-autoupgrade

```


Pretty much all above understanding are based on what i learned in last six months of kubernetes running in production. Container management is easy to adapt and lot of new observation is yet to be discovered as we go along the way.

Looking at deployments today, Kubernetes is absolutely fantastic in Auto-pilot and doing self-healing jobs itself. We are running more than ```1000 pods``` in cluster together and processing ```10's of Billions of API calls per month``` and are pushing more to handle.


------------

> Conclusion : ```Kubernetes``` lifted lot of ``` server management``` and helped in faster depployments & scaling system. Adaptability is much quicker, most of security and other concerns is being managed by Google. Kubernetes aims to offer a better orchestration management system on top of clustered infrastrcuture. Development on Kubernetes has been happening at storm-speed, and the [community of Kubernauts](https://kubernetes.io/community/) has grown bigger.
