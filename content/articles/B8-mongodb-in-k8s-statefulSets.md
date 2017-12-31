Title: Sharded Mongodb in Kubernetes StatefulSets on GKE
Date: 2017-12-31 20:23:31
Category: Blog
Tags: Kubernetes,Mongodb,StatefulSets
Author: Sunny Kr Gupta
Status: draft


This blog is going to demonstrate the setup of Sharded MongoDB Cluster on Google Kubernetes Engine. We will use kubernetes StatefulSets feature to deploy mongodb containers.

![MongoDB in K8s](/images/kubes/k8s-mongodb.png)

We need to cover some concepts before we move on to demonstration.


### [StatefulSets](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset)

A StatefulSets is like a Deployment which manages Pods and provides guarantees about the ordering and uniqueness of these Pods.
It maintains a sticky identity for each of their Pods. It helps in deployment of application that needs persistency, unique network identifiers (DNS, Hostnames etc) and are meants for stateful applications. If a pod get terminated or deleted, a volume data will remain intact if managed by persistentvolumes.  

### [StorageClass](https://kubernetes.io/docs/concepts/storage/storage-classes/#gce)

StorageClass helps in administration of different storage facilitated by Kubernetes. Each StorageClass has different provisioner (GCEPersistentDisk, AWSElasticBlockStore, AzureDisk etc) that determines what volume plugin is used for provisioning storage.

### [PersistentVolume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)

A PersistentVolume (PV) is a piece of storage in the cluster that has been provisioned by an administrator. PVs are resources available to be used by any Pods. Any Pods can come claim these volumes by mean of PersistentVolumeClaims (PVC) and released eventually when claim is deleted.

### [Headless Services](https://kubernetes.io/docs/concepts/services-networking/service/#headless-services)

Headless Services are used to configure DNS of pods having same selectors defined by services. It is not being used for load-balancing. Each headless services configured with label selectors helps in defining unique network identifiers for pods running in statefulset.

<br>

----------------------------------

<br>

Lets begins the demonstration. Please switch to your terminal and follow the instructions.  

### 1. Prerequisites

Ensure the following dependencies are already fulfilled on your host Linux system:

1. GCP’s cloud client command line tool [gcloud](https://cloud.google.com/sdk/docs/quickstarts)
2. gcloud authentication to a project to manage container engine.
3. Install the Kubernetes command tool (“kubectl”),
4. Configure kubernetes authentication credentials.

<br>

----------

<br>

### 2. Create namespace, storageclass, Google compute Disk and persistentvolumes.

Our Mongodb Setup will be as follows :

* 1x Config Server  (k8s deployment type: "StatefulSet")
* 2x Shards with each Shard being a Replica Set containing 1x replicas (k8s deployment type: "StatefulSet")
* 2x Mongos Routers (k8s deployment type: "Deployment")

We will create a kubernetes namespace and will deploy all our above resources in our defined namespaces. We will define disk that will be used by our statefulset containers. Disk will be mounted on pods running our mongodb server by means of APIs defined in StorageClass and PersistentVolume.

---------

#### 2.1 Create Namespace

Create a file as `namespace.yaml` and replace `NAMESPACE_ID` with your handle name or any other name. I will create a namespace with `daemonsl`.

```
#namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: NAMESPACE_ID
```

```
#To apply resources to kubernetes, run
kubectl apply -f namespace.yaml

#To verify namespaces
kubectl get ns
```

------------

#### 2.2 Create StorageClass

Create a file as `gce-ssd-storageclass.yaml`. We are defining our storageclass name as **`fast`** and using GCE persistent disk as our provisioner with `type: pd-ssd` to allow SSD disk type allocation to requester (ie, statefulset container here).

```
#gce-ssd-storageclass.yaml
kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
  name: fast
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-ssd
```

```
#To apply resources to kubernetes, run
kubectl apply -f gce-ssd-storageclass.yaml

#To verify storageclass
kubectl get sc
```

--------

#### 2.3 Create GCE SSD Disks

We will create some disk to be used by mongodb statefulset container. We are ordering two `10GB` disk and one `5GB` disk of type `SSD`.

```
#For MainDB servers
gcloud compute disks create --size 10GB --type pd-ssd pd-ssd-disk-k8s-mongodb-daemonsl-10g-1
gcloud compute disks create --size 10GB --type pd-ssd pd-ssd-disk-k8s-mongodb-daemonsl-10g-2

#For Config servers
gcloud compute disks create --size 5GB --type pd-ssd pd-ssd-disk-k8s-mongodb-daemonsl-5g-1
```

--------

#### 2.4 Create PersistentVolume

Create a file as `ext4-gce-ssd-persistentvolume.yaml`. We are defining our PersistentVolume storage capacity `10GB` to be bounded by `maindb` pod and `5GB` to be bounded by `configdb` pod.

```
#ext4-gce-ssd-persistentvolume.yaml
apiVersion: "v1"
kind: "PersistentVolume"
metadata:
  name: data-volume-k8s-mongodb-daemonsl-SIZEg-INSTANCE
spec:
  capacity:
      storage: SIZEGi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: fast
  gcePersistentDisk:
    fsType: ext4
    pdName: pd-ssd-disk-k8s-mongodb-daemonsl-SIZEg-INSTANCE
```

Use above template, modify and apply in following order :

```
#Replace 'SIZE' with 10 and 'INSTANCE' with 1,
# Ex: data-volume-k8s-mongodb-daemonsl-10g-1, storage: 10Gi,
kubectl apply -f ext4-gce-ssd-persistentvolume.yaml

#Replace 'SIZE' with 10 and 'INSTANCE' with 2
kubectl apply -f ext4-gce-ssd-persistentvolume.yaml

#Replace 'SIZE' with 5 and 'INSTANCE' with 1
kubectl apply -f ext4-gce-ssd-persistentvolume.yaml


#To verify PersistentVolume creation,
kubectl get pv
```


Now we have **storageclass, namespace, disks** and **persistentvolume** ready as resources for statefulset container.

<br>

----------------

<br>

### 3. StatefulSet containers and Mongos Deployment.

#### 3.1 Statefulset ConfigDB

Create a file as `mongodb-configdb-service-stateful.yaml` and copy the following template. Replace `NAMESPACE_ID` with `daemonsl`, or whatever name you have defined and `DB_DISK` with `5Gi`.

We have created a headless service with clusterIP `None` with selector as `role: mongodb-configdb` listening to port `27019`. We have defined our statefulset definition with mongodb arguments and volumeClaimTemplates. Here, `VolumeClaimTemplates` is requesting storageclass `fast` with `storage capacity 5GB`. This volumeClaimTemplates register this requests to storageclass and storageclass fulfill this requests by  `PersistentVolume (PV)` and register claim in `PersistentVolumeClaims (PVC)`.


```
#mongodb-configdb-service-stateful.yaml
apiVersion: v1
kind: Service
metadata:
  name: mongodb-configdb-headless-service
  namespace: NAMESPACE_ID
  labels:
    name: mongodb-configdb
spec:
  ports:
  - port: 27019
    targetPort: 27019
  clusterIP: None
  selector:
    role: mongodb-configdb
---
apiVersion: apps/v1beta2  #change this version based on master version
kind: StatefulSet
metadata:
  name: mongodb-configdb
  namespace: NAMESPACE_ID
spec:
  selector:
    matchLabels:
      role: mongodb-configdb # has to match .spec.template.metadata.labels
  serviceName: mongodb-configdb-headless-service
  replicas: 1
  template:
    metadata:
      labels:
        role: mongodb-configdb
        tier: configdb
    spec:
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: tier
                  operator: In
                  values:
                  - configdb
              topologyKey: kubernetes.io/hostname
      terminationGracePeriodSeconds: 10
      containers:
        - name: mongodb-configdb-container
          image: mongo
          command:
            - "mongod"
            - "--port"
            - "27019"
            - "--dbpath"
            - "/mongo-disk"
            - "--bind_ip"
            - "0.0.0.0"
            - "--configsvr"
          resources:
            requests:
              cpu: 50m
              memory: 100Mi
          ports:
            - containerPort: 27019
          volumeMounts:
            - name: mongodb-configdb-persistent-storage-claim
              mountPath: /mongo-disk
  volumeClaimTemplates:
  - metadata:
      name: mongodb-configdb-persistent-storage-claim
      annotations:
        volume.beta.kubernetes.io/storage-class: "fast"
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: DB_DISK
```

```
kubectl apply -f mongodb-configdb-service-stateful.yaml
```

-------------

#### 3.2 Statefulset mainDB

Create a file as `mongodb-maindb-service-stateful.yaml` and copy the following template. Replace `NAMESPACE_ID` with `daemonsl`, or whatever name you have defined, `DB_DISK` with `10Gi` and `shardX` & `ShardX` to `1` and then `2` and apply template two times to create two different statefulsets configuration. After deploying in kubernetes, we will have two statefulsets running with name as `mongodb-shard1` and `mongodb-shard2`

Here again, We have created headless service and `VolumeClaimTemplates` which is requesting storageclass `fast` with storage capacity 10GB.

```
#mongodb-maindb-service-stateful.yaml
apiVersion: v1
kind: Service
metadata:
  name: mongodb-shardX-headless-service
  namespace: NAMESPACE_ID
  labels:
    name: mongodb-shardX
spec:
  ports:
  - port: 27017
    targetPort: 27017
  clusterIP: None
  selector:
    role: mongodb-shardX
---
apiVersion: apps/v1beta2
kind: StatefulSet
metadata:
  name: mongodb-shardX
  namespace: NAMESPACE_ID
spec:
  selector:
    matchLabels:
      role: mongodb-shardX # has to match .spec.template.metadata.labels
  serviceName: mongodb-shardX-headless-service
  replicas: 1
  template:
    metadata:
      labels:
        role: mongodb-shardX
        tier: maindb
        replicaset: ShardX
    spec:
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: replicaset
                  operator: In
                  values:
                  - ShardX
              topologyKey: kubernetes.io/hostname
      terminationGracePeriodSeconds: 10
      containers:
        - name: mongodb-shardX-container
          image: mongo
          command:
            - "mongod"
            - "--port"
            - "27017"
            - "--bind_ip"
            - "0.0.0.0"
            - "--replSet"
            - "ShardX"
            - "--dbpath"
            - "/mongo-disk"
          resources:
            requests:
              cpu: 50m
              memory: 100Mi
          ports:
            - containerPort: 27017
          volumeMounts:
            - name: mongo-shardX-persistent-storage-claim
              mountPath: /mongo-disk
  volumeClaimTemplates:
  - metadata:
      name: mongo-shardX-persistent-storage-claim
      annotations:
        volume.beta.kubernetes.io/storage-class: "fast"
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: DB_DISK
```

```
#replace 'shardX' & 'ShardX' with shard1 & Shard1. Mind case sensitivity.
kubectl apply -f mongodb-maindb-service-stateful.yaml

#replace 'shardX' & 'ShardX' with shard2 & Shard2. Mind case sensitivity.
kubectl apply -f mongodb-maindb-service-stateful.yaml

#run command to see Pods & Services spinning up
kubectl get svc,po --namespace=daemonsl
```

Till here, we have accomplished statefulsets container running along with headless services and mounted a SSD volume that fulfills Pods requirement.

```
kubectl get persistentvolumes

# Get persistent volume claims
kubectl get persistentvolumeclaims --namespace=daemonsl
```

-----------

#### 3.3 Mongos Deployment

We have configdb and maindb pods up and running. We will spin up mongos server to establish a sharding cluster. Replace `NAMESPACE_ID` with `daemonsl`, or whatever name you have defined.

We have configured config server information in mongos using `--configdb` flag with unique network identifiers of configdb pod. DNS of statefulset pods goes by convention `<POD_NAME>.<SERVICE_NAME>.<NAMESPACE>.svc.<CLUSTER_DOMAIN>`.

**Reference : ** [https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/#stable-network-id](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/#stable-network-id)


```
apiVersion: apps/v1beta1
kind: Deployment
metadata:
  name: mongos
  namespace: NAMESPACE_ID
spec:
  replicas: 2
  template:
    metadata:
      labels:
        role: mongos
        tier: routers
    spec:
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: tier
                  operator: In
                  values:
                  - routers
              topologyKey: kubernetes.io/hostname
      terminationGracePeriodSeconds: 10
      containers:
        - name: mongos-container
          image: mongo
          command:
            - "mongos"
            - "--port"
            - "27017"
            - "--bind_ip"
            - "0.0.0.0"
            - "--configdb"
            - "mongodb-configdb-0.mongodb-configdb-headless-service.daemonsl.svc.cluster.local:27019"
          resources:
            requests:
              cpu: 50m
              memory: 100Mi
          ports:
            - containerPort: 27017
```

```
kubectl apply -f mongodb-mongos-deployment-service.yaml
```

<br>

------------------

<br>

### 4 Configure Sharding

Now, we have `mongos, configdb` and `maindb` up and running. We need to create Replicaset in MainDB servers that we are intending to make shard. We will run `rs.initiate()` command to make `PRIMARY` replica. Since we are going with one replica member in each shard. We will run initiate command in each of the `maindb` pod.

    echo "Replicaset Init mongodb-shard1-0 "
    kubectl exec --namespace=daemonsl mongodb-shard1-0 -c mongodb-shard1-container -- mongo --port 27017 --eval "rs.initiate({_id: \"Shard1\", version: 1, members: [ {_id: 0, host: \"mongodb-shard1-0.mongodb-shard1-headless-service.daemonsl.svc.cluster.local:27017\"} ] });"


    echo "Replicaset Init mongodb-shard2-0 "  
    kubectl exec --namespace=daemonsl mongodb-shard2-0 -c mongodb-shard2-container -- mongo --port 27017 --eval "rs.initiate({_id: \"Shard2\", version: 1, members: [ {_id: 0, host: \"mongodb-shard2-0.mongodb-shard2-headless-service.daemonsl.svc.cluster.local:27017\"} ] });"


Above lines, will make both pods PRIMARY of their respective replicaset. You can even go into container to verify replicaset status by running `rs.status()` command.

We are proceeding now to add shards to mongos server. We will run below command in any of the mongos pod. Mongos server are stateless application, they save the configuration in configdb server which we have made stateful application by declaring them under statefulset container.

```

echo "Adding Shard 1 : Shard1 "
kubectl exec --namespace=daemonsl $(kubectl get pod -l "tier=routers" -o jsonpath='{.items[0].metadata.name}' --namespace=daemonsl ) -c mongos-container -- mongo --port 27017 --eval "sh.addShard(\"Shard1/mongodb-shard1-0.mongodb-shard1-headless-service.daemonsl.svc.cluster.local:27017\");"

echo "Adding Shard 2 : Shard2 "
kubectl exec --namespace=daemonsl $(kubectl get pod -l "tier=routers" -o jsonpath='{.items[0].metadata.name}' --namespace=daemonsl ) -c mongos-container -- mongo --port 27017 --eval "sh.addShard(\"Shard2/mongodb-shard2-0.mongodb-shard2-headless-service.daemonsl.svc.cluster.local:27017\");"
```

Now, we can get into one of the mongos container to verify the sharding status of cluster. All the above steps can be automated to make any number of shards within your cluster and thus concepts are very trivial to support stateful application powered by GKE.

-----------

#### Test Sharding

To test that the sharded cluster is working properly, connect to the container running the first "mongos" router, then use the Mongo Shell to authenticate, enable sharding on a specific database & collection, add some test data to this collection and then view the status of the Sharded cluster and collection:

    $ kubectl exec -it $(kubectl get pod -l "tier=routers" -o jsonpath='{.items[0].metadata.name}') -c mongos-container bash
    $ mongo
    > sh.enableSharding("<Database_name>");
    > sh.status();
    > use admin
    > db.admin.runCommand("getShardMap")

-----------

#### Tearing & Cleaning Down the Kubernetes Environment

**Important:** This step is required to ensure you aren't continuously charged by Google Cloud for an environment you no longer need.

Run the following script to undeploy the MongoDB Services & StatefulSets/Deployments plus related Kubernetes resources, followed by the removal of the GCE disks. This script is available in repository.

    $ sh teardown.sh   #To delete all resources provisioned above

-----------

### Factors Addressed in this Demonstration

* Deployment of a MongoDB on the Google Kubernetes Engine
* Use of Kubernetes StatefulSets and PersistentVolumeClaims to ensure data is not lost when containers are recycled
* Proper configuration of a MongoDB Sharded Cluster for Scalability with each Shard being a Replica Set for full resiliency
* Controlling Anti-Affinity for Mongod Replicas to avoid a Single Point of Failure

-----------

#### Must read below resources in order :

- [https://kubernetes.io/docs/concepts/workloads/controllers/statefulset](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset)
- [https://kubernetes.io/docs/concepts/services-networking/service/#headless-services](https://kubernetes.io/docs/concepts/services-networking/service/#headless-services)
- [https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/#stable-network-id](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/#stable-network-id)
- [https://kubernetes.io/docs/concepts/storage/storage-classes/#gce](https://kubernetes.io/docs/concepts/storage/storage-classes/#gce)
- [https://kubernetes.io/docs/concepts/storage/persistent-volumes/](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- [http://blog.kubernetes.io/2017/03/dynamic-provisioning-and-storage-classes-kubernetes.html](http://blog.kubernetes.io/2017/03/dynamic-provisioning-and-storage-classes-kubernetes.html)
- [http://blog.kubernetes.io/2017/03/advanced-scheduling-in-kubernetes.html](http://blog.kubernetes.io/2017/03/advanced-scheduling-in-kubernetes.html)

<br>

**Credit :** This blog is based on workdone by [Paul Done](https://twitter.com/TheDonester)

-------------
