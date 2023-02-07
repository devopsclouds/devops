kubernetes

kubernetes is opn source container architecture engine manage containers for high avaiblity.
cluster management
scheduling
service discovery monitoring

secrets management


kubernetes is also called as k8s
k8s architecture

1.worker nodes are nothing but virtual machines or physcial servers running within in a data centre . All these nodes join together

to form a cluster.
2.pod is scheduling unit in kubernetes . each pod consists of one or more containers , most cases only one container. container are
run run time enviornment for run time appilication . containers are designed to run microservices application are not monolithic application

3.master is resposible for manging the entire cluster.it monitors the health check of the nodes.when the work node fails it moves work node to failure node.
and keep to  another healthy node

k8s master components
API Server: Api server is the entire gatekeeper of cluster. 
API : all the objects perform in the API like pod craetion, service and any operation , API using kubectl command or UI
then Api interacts with api server. api server should do the validates the objects.

shecudelar . shecudlig in the pods acrosss multipe nodes   kubernetes deponds upon the constraints like memory etc
suppose if the application requires x constarints the scheduler will look the appromaite work node for that application

controller manager
they are four
1.node point controller
2.repplication controller
3.end point controller

these controller are responsible for health check of entire cluster
it ensures the nodes are up and running
it ensure the correct number of pods are running as mention in the spec file

etcd is central data base store current state of the cluster at any point of time. it is  key value distributed data base the data will stored related to cluster
worker node components
kubelet : kubelet is the primary node agent in every worker node inside the cluster. bascially it look the pod spec and submitted to api server in master
ensure that pod to be running and healthy.if the kubelet notices any issues in the pod in the worker node . then it will restart the pods in same worker node
if the problem within in the worker node itself then the matser detects the failure node and launches the pod in another worker node.
if all depends on pod is replication controller or repplication set

kube proxy . It is responsible for mantaining the entire network configuration and it also exposes the service to outside the world


Every node is unique is ip adddress . in the kubernetes when we deployed the pod in the cluster we get pod ip address

pod: pod contain one or more container most cases one container 
if  the pod has one or more containers how we can communicate . as we know each pod has unique ipaddess , same cname communicate ipdress through different port number containers
how the two pods can communicate by using pod network.
u r defining manifest file and submitted to api serverin kubernetes master and scheduler schelude the pods in the appromirimate worker node once it is scheduled then 
go to pending state during the pending state it downlod the container of required images ,once it is done then it goes to running state

in the mainfest yaml file they are 4 attributes
apiversion: v1 [ apiversion is the version of pod]
kind: pod    [ what kind of object]
metadata:    [ they are two fields name and label] 
  name:  ngnix-pod [ name of the pod]
  labels:      [ label is the tag to pod , u can filter by using label supoose if u have no of pods are running in the cluster u can filter like ngnix
     app: ngnix
     tier: dev
spec:
  containers:
  - name: ngnix-container
    image: ngnix

apiversion: v1 
kind: pod    
metadata:   
  name:  ngnix-pod 
  labels:     
     app: ngnix
     tier: dev
spec:
  containers:
  - name: ngnix-container
    image: ngnix

important commands
kubectl create -f yaml file
kubectl delete -f yaml file
kubectl get pods 
kubectl get pods -o wide
kubectl describe pod podname

Repplication controller:
Ensure that specified pods are running at any time
1.If they are excess pods, they get killed and vice-versa
2.New pods are launched when they get killed,deleted or terminated
Replication controller and pods are associated with labels
creating a replication controller with a count of 1 esure that pod is always avaibile
The main adavantage is high avaibility and load balancincng
load is equal balance among all the pods inside the cluster . the no of requests is passes the same.
if the node1 memory is full , assuming that 3 pods are running node1 and remaining 1 pod isrunning at another worker node if rc count as 4 
suppose if the rc count as 1 , assumming that pod dies or crashes then the pod will recreate within ths same node . it it 1 means pod should be running at any time
the issue within the node itstelf , then the pod will recreate an another helthy work node

apiVersion: v1
kind: ReplicationController
metadata:
 name: httpd-rc
spec:
 replicas: 3
 selector:
    app: httpd
 template:
    metadata:
      name:  httpd-pod
      labels:
        app: httpd
        tier: dev
    spec:
      containers:
      - name: httpd-container
        image: httpd
        imagePullPolicy: Always
        ports:
        - containerPort: 80

here the object is relication controller and how we need to spec the replicas and pod template . replication controller know this pod by using selector and label

ReplicationController is equaity based selector
ReplicationSet is set based selector

Replicaset
apiVersion: v1
kind: ReplicaSet
metadata:
 name: httpd-rc
spec:
 replicas: 3
 selector:
   matchLabels:
    app: httpd
   matchExpression:
      - {key: tier,operator: In, values: [frontend]}
 template:
    metadata:
      name:  httpd-pod
      labels:
        app: httpd
        tier: frontend
    spec:
      containers:
      - name: httpd-container
        image: httpd
        imagePullPolicy: Always
        ports:
        - containerPort: 80



important commands
kubectl exec -it httpd-pod -- /bin/bash
  127  docker images
  128  cd /opt
  129  vi ng.yaml
  130  kubectl delete -f ng.yaml
  131  kubectl create -f ng.yaml
  132  vi ng.yaml
  133  kubectl create -f ng.yaml
  134  kubectl get pods
  135  kubectl get pods -o wide
  136  kubectl delete -f ng.yaml
  137  vi ng.yaml
  138  kubectl create -f ng.yaml
  139  kubectl get pods -o wide
  140  cat ng.yaml
  141  kubectl get -l pods
  142  kubectl get pods -l
  143  kubectl get pods app=httpd
  144  kubectl get po -l  app=httpd
  145  kubectl describe rc httpd-rc
  146  kubectl get po -l app=httpd
  147  kubectl describe rc httpd-rc
  148  kubectl get pods -o wide
  149  kubectl get nodes
  150  kubectl scale rc httpd-rc --replicas=5
  151  kubectl get rc
  152  kubectl get pods

Replicaset or controller does not there updgrade or roll back


deployment will have some additional features
Multiple replicas : replicat set to in pod for high availibility and load balancing
if u does not specifiy in replica set in manifest file then deplyment controller will set the replica count as 1 . advantage is it ensure that 1 pod will be running at any time
Upgrade: In the upgarde we have some deployment types
1.Recreate: suppose u upgrade the v1 to v2 . it will turn off of v1 then start the v2 during the swith from v1 to v2 there is a downtime
2.Rollingupdate:Rolling update is the default strategy in kubernetes but upgarding is slow. suppose v1 have 10 instances with load balancing it upgarding one after another . when 1 st instance  ugarding to v2 then the switch off i st instance  and then v2 accepts the 1 st instance . similary soo on
3. canary: canary deployment u cannot upgare v1 all into v2.suppose there are 10 instances are running in the cluster first u upgrade 2 instances to v2 and its tested once the ready 2 instances in v2 then switch off 2 instances in v1 and remaining 8 instances will do upgarde automatically.
4. Blue/Green: the advatage of this roll out and roll back
ROllback: if u done mistake while upgrading new version u can roll out to previous version.
Pause/resume: u can pause is in inprogress and whenever want u can resume

apiVersion: apps/v1
kind: Deployment
metadata:
 name: httpd-deploy
 labels:
   app: httpd
spec:
 replicas: 2
 selector:
   matchLabels:
    app: httpd
 template:
    metadata:
      name:  httpd-pod
      labels:
        app: httpd
        tier: dev
    spec:
      containers:
      - name: httpd-container
        image: httpd
        imagePullPolicy: Always
        ports:
        - containerPort: 80


1.Rolling update: If u have set replicas has 4 , then 4 pods are running .when u update the from one version to another version , it not migrate  all the pods to  another version at a time , It will take one pod is terminated and start again then update the pod to another version. the process is continue to another pod and so on





apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    run: nginx
  name: nginx-deploy
spec:
  replicas: 4
  selector:
    matchLabels:
      run: nginx
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 0
      maxUnavailable: 1
  minReadySeconds: 5
  revisionHistoryLimit: 10
  template:
    metadata:
      labels:
        run: nginx
    spec:
      containers:
      - image: nginx:1.13
        name: nginx
  


Maxunavailable - 1  -- if u set is 1 only one pod is terminating at a time and it container again updated to new version
maxSurge : the maximum number of pods that can be created over the desired number of pods.


Updating the version to another version
Kubectl set image deploy nginx-deploy nginx=nginx:1.12-----Updating the version to another version

Or

Kubectl edit deploy nginx-deploy -o yaml




Kubectl rollout status deploy nginx-deploy ------- to check the rollout status of deployments
Kubectl rollout history deploy nginx-deploy   --------- to find out the revision of previous deployments and current deployments
-
Kubectl rollout history deplorevisiy nginx-deploy --revision=2   -----------to specific revision history


Kubectl rollout undo deploy nginx-deploy  --------- to undo the changes of previous deployment


kubectl rollout undo deploy nginx-deploy --to-revision=revision number ------to undo the changes of specific deployment



kubectl annotate deploy nginx-deploy Kubernetes.io/change-cause="updated version"

Or

Edit the line in yaml file in the metadata spec

annotations:
      kubernetes.io/change-cause: "updated to latest version"




2.Rollcreate. when u are updating the new version to another version , if u have 4 pods that 4 pods will terminate and start again in parallel. This type of deployment whenever any  urgenency need but in the production u will face issue becoz the down time will be happened



cat rollcreate.yaml 
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    run: nginx
  name: nginx-deploy
spec:
  replicas: 4
  selector:
    matchLabels:
      run: nginx
  strategy:
    type: Recreate
  minReadySeconds: 5
  revisionHistoryLimit: 10
  template:
    metadata:
      labels:
        run: nginx
    spec:
      containers:
      - image: nginx:1.13
        name: nginx

Blue green
Blue-green deployment is a technique that reduces downtime and risk by running two identical production environments called Blue and Green.

At any time, only one of the environments is live, with the live environment serving all production traffic. For this example, Blue is currently live and Green is idle.

As you prepare a new version of your software, deployment and the final stage of testing takes place in the environment that is not live: in this example, Green. Once you have deployed and fully tested the software in Green, you switch the router so all incoming requests now go to Green instead of Blue. Green is now live, and Blue is idle.

This technique can eliminate downtime due to app deployment. In addition, blue-green deployment reduces risk: if something unexpected happens with your new version on Green, you can immediately roll back to the last version by switching back to Blue.


switch the traffic using the load balancer
for 2 deployments using the same load balancer service but differnet selectors with lables to be used


Blue/Green deployments are very powerful when it comes to easy rollbacks, but they are not the only approach for updating your Kubernetes application.

canary deployment

Another deployment strategy is using Canaries (a.k.a. incremental rollouts). With canaries, the new version of the application is gradually deployed to the Kubernetes cluster while getting a very small amount of live traffic (i.e. a subset of live users are connecting to the new version while the rest are still using the previous version).


The small subset of live traffic to the new version acts as an early warning for potential problems that might be present in the new code. As our confidence increases, more canaries are created and more users are now connecting to the updated version. In the end, all live traffic goes to canaries, and thus the canary version becomes the new “production version”.


The big advantage of using canaries is that deployment issues can be detected very early while they still affect only a small subset of all application users. If something goes wrong with a canary, the production version is still present and all traffic can simply be reverted to it.

While a canary is active, you can use it for additional verification (for example running smoke tests) to further increase your confidence on the stability of each new version.

kubectl scale deploy deploy-1 --replicas=5
kubectl scale deploy deploy-2 --replicas=1





Namespace
In Kubernetes, namespaces provides a mechanism for isolating groups of resources within a single cluster. Names of resources need to be unique within a namespace, but not across namespaces. Namespace-based scoping is applicable only for namespace objects (e.g. Deployments, Services, etc) and not for cluster-wide objects (e.g. StorageClass, Nodes, PersistentVolumes, etc).

Suppose u have creating more resources in the single cluster from different teams or different environments like dev sit etc . Then u can create namespaces for different env or teams

Note : when u deploy the resource with namespace and u cannot deploy the same resource with that same namespace

Kubectl get ns

kubectl get ns       
NAME                   STATUS   AGE
default                Active   26d
kube-node-lease        Active   26d
kube-public            Active   26d
kube-system            Active   26d
kubernetes-dashboard   Active   26d


Default - when u create resources it will be under in the default namespace
 
kubectl get po -n kube-system
NAME                               READY   STATUS    RESTARTS        AGE
coredns-78fcd69978-pwhct           1/1     Running   6 (3h23m ago)   26d
etcd-minikube                      1/1     Running   6 (3h23m ago)   26d
kindnet-4cgzq                      1/1     Running   9 (3h22m ago)   26d
kindnet-fqs52                      1/1     Running   2 (3h22m ago)   10d
kindnet-q7lxj                      1/1     Running   9 (3h22m ago)   26d
kindnet-qzbqz                      1/1     Running   8 (3h23m ago)   26d
kube-apiserver-minikube            1/1     Running   7 (3h23m ago)   26d
kube-controller-manager-minikube   1/1     Running   6 (3h23m ago)   26d
kube-proxy-75x7x                   1/1     Running   6 (3h22m ago)   26d
kube-proxy-8sx9f                   1/1     Running   6 (3h23m ago)   26d
kube-proxy-q9mqm                   1/1     Running   2 (3h22m ago)   10d
kube-proxy-rn6jb                   1/1     Running   6 (3h22m ago)   26d
kube-scheduler-minikube            1/1     Running   6 (3h23m ago)   26d
metrics-server-5d56ccdd76-ltdzt    1/1     Running   3 (3h23m ago)   10d
storage-provisioner                1/1     Running   19 (131m ago)   26d


kube-system ---when u install Kubernetes by Kubernetes components will be created it will be under in the kube-system namespace
Create the namespace ---- kubectl create namespace dev
Or
apiVersion: v1
kind: Namespace
metadata:
    name: dev

Suppose u need to create the resource with dev namespace
Kubectl create -f yaml file -n dev
Or
Edit the resource yaml file under the metadata
Namespace: dev


Context : A kubernetes context is just a set of access parameters that contains a Kubernetes cluster, a user, and a namespace. kubernetes Context is essentially the configuration that you use to access a particular cluster & namespace with a user account.




Kubectl config view - to find out cluster info , contexts info . In the contexts we have namespace and user

kubectl config get-contexts    ---- to find all the contextrs
CURRENT   NAME       CLUSTER    AUTHINFO   NAMESPACE
          dev        minikube   minikube   dev
*         minikube   minikube   minikube   default
          test       minikube   minikube   test

kubectl config current-context.      ---- to find the current context
minikube
kubectl config get-clusters           ----- to find the clusters
NAME
minikube
kubectl config get-users           --- to find the users 
NAME
minikube


To switch to different namespace by using context , then u don't need to given -n namespace 

kubectl config set-context dev --cluster=minikube --user=minikube --namespace=dev.  - to create the context with specific namespace

Switch to context -- kubectl config use-context dev

Then the default namespace is dev . When u create resource by default it will goes to dev namespace




How to schedule pod in the specific node. ---- if u apply the label in the specific node and then specify that label in the pod spec of yaml file

Kubectl label node nodename  ram= slow 
apiVersion: apps/v1
kind: Deployment
metadata:
  name: httpd-deploy
  labels:
    app: httpd-deploy
spec:
  replicas: 1
  selector:
    matchLabels:
      app: httpd
  template:
    metadata:
      name: httpd-pod
      labels:
        app: httpd
        tier: dev
    spec:
      nodeSelector:
        ram: slow
      containers:
        
        - image: sushanth53/ngnix_server
          imagePullPolicy: Always
          name: nginx-container
          ports:
          - containerPort: 80


How to schedule the pod on node using admission control plugin through namespace
First u have add plugin PodNodeSelector in enable admission plugin on the api server
Then add the label to node 
Kubectl label node nodename "env="develop"
Create the namespace : kubectl create ns dev
Edit the namespace dev and add annotation add label whatever u add the label to node in the previous , then belongs to that label to schedule the specific node
Add this line 
Annotations:
     Scheduler.alpha.kubernetes.io/node-selector: "env=Develop"


SET LIMIT NUMBER OF PODS

mark nodes is unscheduled or disabled
kubcectl cordon nodename

mark node is scheduled or enabled
kubectl uncordon nodename

set limit of pod : 
by default of pods in node is 110
kubectl describe node nodename | grep pods

set the specific limit
go to node

cd /var/lib/kubelet
open config.yaml
edit maxPods: 10
systemctl start kubelet


RESOURCES QUOTA AND LIMITS

When several users or teams share a cluster with a fixed number of nodes, there is a concern that one team could use more than its fair share of resources.

Resource quotas are a tool for administrators to address this concern.

A resource quota, defined by a ResourceQuota object, provides constraints that limit aggregate resource consumption per namespace. It can limit the quantity of objects that can be created in a namespace by type, as well as the total amount of compute resources that may be consumed by resources in that namespace.

Resource quotas work like this:

Different teams work in different namespaces. This can be enforced with RBAC.

The administrator creates one ResourceQuota for each namespace.

Users create resources (pods, services, etc.) in the namespace, and the quota system tracks usage to ensure it does not exceed hard resource limits defined in a ResourceQuota.

If creating or updating a resource violates a quota constraint, the request will fail with HTTP status code 403 FORBIDDEN with a message explaining the constraint that would have been violated.

If quota is enabled in a namespace for compute resources like cpu and memory, users must specify requests or limits for those values; otherwise, the quota system may reject pod creation. Hint: Use the LimitRanger admission controller to force defaults for pods that make no compute resource requirements.

See the walkthrough for an example of how to avoid this problem.

The name of a ResourceQuota object must be a valid DNS subdomain name.

Examples of policies that could be created using namespaces and quotas are:

In a cluster with a capacity of 32 GiB RAM, and 16 cores, let team A use 20 GiB and 10 cores, let B use 10GiB and 4 cores, and hold 2GiB and 2 cores in reserve for future allocation.
Limit the "testing" namespace to using 1 core and 1GiB RAM. Let the "production" namespace use any amount.
In the case where the total capacity of the cluster is less than the sum of the quotas of the namespaces, there may be contention for resources. This is handled on a first-come-first-served basis.

Neither contention nor changes to quota will affect already created resources.

Enabling Resource Quota
Resource Quota support is enabled by default for many Kubernetes distributions. It is enabled when the API server --enable-admission-plugins= flag has ResourceQuota as one of its arguments.

A resource quota is enforced in a particular namespace when there is a ResourceQuota in that namespace.

Compute Resource Quota
You can limit the total sum of compute resources that can be requested in a given namespace.

The following resource types are supported:

Resource Name	Description
limits.cpu	Across all pods in a non-terminal state, the sum of CPU limits cannot exceed this value.
limits.memory	Across all pods in a non-terminal state, the sum of memory limits cannot exceed this value.
requests.cpu	Across all pods in a non-terminal state, the sum of CPU requests cannot exceed this value.
requests.memory	Across all pods in a non-terminal state, the sum of memory requests cannot exceed this value.
hugepages-<size>	Across all pods in a non-terminal state, the number of huge page requests of the specified size cannot exceed this value.
cpu	Same as requests.cpu
memory	Same as requests.memory


important commands
kubectl create -g ng1.yaml
  160  kubectl create -f ng1.yaml
  161  kubectl get po -l app=httpd
  162  kubectl get deployment -l app=httpd
  163  kubectl get rc  -l app=httpd
  164  kubectl get
  165  kubectl get rc
  166  kubectl get rs
  167  kubectl get rs -l app=httpd
  168  kubectl decribe deploy httpd-deploy
  169  kubectl describe deploy httpd-delpoy
  170  kubectl decribe deploy httpd-deploy
  171  kubectl describe deploy httpd-deploy
  172  kubectl set image deploy httpd-deploy httpd-container=httpd:2.4.43
  173  kubectl decribe deploy httpd-deploy
  174  kubectl describe deploy httpd-deploy
  175  cat ng1.yaml
  176  kubectl edit deploy httpd-deploy
  177  kubectl rollout status deploy/httpd-deploy
  178  cat ng1.yaml
  179  kubectl rollout history deploy/httpd-deploy
  180  kubectl rollout undo  deploy/httpd-deploy
  181  kubectl describe deploy httpd-deploy
kubectl scale deploy httpd-deploy --replicas=5



The type property in the Service's spec determines how the service is exposed to the network. It changes where a Service is able to be accessed from. The possible types are ClusterIP, NodePort, and LoadBalancer

ClusterIP ñ The default value. The service is only accessible from within the Kubernetes cluster ñ you canít make requests to your Pods from outside the cluster!
NodePort ñ This makes the service accessible on a static port on each Node in the cluster. This means that the service can handle requests that originate from outside the cluster.
LoadBalancer ñ The service becomes accessible externally through a cloud provider's load balancer functionality. GCP, AWS, Azure, and OpenStack offer this functionality. The cloud provider will create a load balancer, which then automatically routes requests to your Kubernetes Service

Port exposes the Kubernetes service on the specified port within the cluster. Other pods within the cluster can communicate with this server on the specified port.
TargetPort is the port on which the service will send requests to, that your pod will be listening on. Your application in the container will need to be listening on this port also.
NodePort exposes a service externally to the cluster by means of the target nodes IP address and the NodePort. NodePort is the default setting if the port field is not specified.


clusterIP:
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
  labels:
    app: nginx
spec:
  selector:
      app: nginx
  type: ClusterIP
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80


headless service
When there is no need of load balancing or single-service IP addresses.We create a headless service which is used for creating a service grouping. That does not allocate an IP address or forward traffic.So you can do this by explicitly setting ClusterIP to “None” in the mainfest file, which means no cluster IP is allocated.

For example, if you host MongoDB on a single pod. And you need a service definition on top of it for taking care of the pod restart.And also for acquiring a new IP address. But you don’t want any load balancing or routing. You just need the service to patch the request to the back-end pod. So then you use Headless Service since it does not have an IP.

Kubernetes allows clients to discover pod IPs through DNS lookups. Usually, when you perform a DNS lookup for a service, the DNS server returns a single IP which is the service’s cluster IP. But if you don’t need the cluster IP for your service, you can set ClusterIP to None , then the DNS server will return the individual pod IPs instead of the service IP.Then client can connect to any of them.

apiVersion: v1
kind: Service
metadata:
  name: headless-svc
spec:
  clusterIP: None
  selector:
    app: web
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080

loadbalancer
apiVersion: v1
kind: Service
metadata:
  name: example-service
spec:
  selector:
    app: example
  ports:
    - port: 8765
      targetPort: 9376
  type: LoadBalancer
  
nodeportservice

apiVersion: v1
kind: Service
metadata:
  name: nginx-service
  labels:
    app: nginx
spec:
  selector:
      app: nginx
  type: NodePort
  ports:
    - nodePort: 31000
      port: 80
      targetPort: 80 
      
      
metallb: if u are  using cloud cloud provider will create external load balance  by automataically. if not u need to setup metal lb balancer and install metal load balancer




  volumes
  empty dir: emptyDir are volumes that get created empty when a Pod is created.

While a Pod is running its emptyDir exists. If a container in a Pod crashes the emptyDir content is unaffected. Deleting a Pod deletes all its emptyDirs.

There are several ways a Pod can be deleted. Accidental and deliberate. All result in immediate emptyDir deletion. emptyDir are meant for temporary working disk space.
empty-dir.yaml
apiVersion: v1
kind: Pod
metadata:
        name: emptydir-vol
spec:
        containers:
                - name: emptycontainer
                  image: nginx
                  volumeMounts:
                           - name: empty-vol
                             mountPath: /cache


        volumes:
                - name: empty-vol
                  emptyDir: {}
                  
hostpath

A hostPath volume mounts a file or directory from the file system of the host node to a pod. This topic describes how to mount hostPath volumes to pods.

#hostpath.yaml
apiVersion: v1
kind: Pod
metadata:
        name: hostpath-vol
spec:
        containers:
                - name: emptycontainer
                  image: nginx
                  volumeMounts:
                           - name: host-vol
                             mountPath: /test-path


        volumes:
                - name: host-vol
                  hostPath:
                          path: /test-vol

Kubernetes persistent volume
Kubernetes persistent volumes are administrator provisioned volumes. These are created with a particular filesystem, size, and identifying characteristics such as volume IDs and names.
A Kubernetes persistent volume has the following attributes
when admin create a pv , and user claim request a some storage and used it in actual deploy
 

It is provisioned either dynamically or by an administrator
Created with a particular filesystem
Has a particular size
Has identifying characteristics such as volume IDs and a name

  install nfs-server  package in server
  cat /etc/exports 
# /etc/exports: the access control list for filesystems which may be exported
#		to NFS clients.  See exports(5).
#
# Example for NFSv2 and NFSv3:
# /srv/homes       hostname1(rw,sync,no_subtree_check) hostname2(ro,sync,no_subtree_check)
#
# Example for NFSv4:
# /srv/nfs4        gss/krb5i(rw,sync,fsid=0,crossmnt,no_subtree_check)
# /srv/nfs4/homes  gss/krb5i(rw,sync,no_subtree_check)
#
/srv/nfs/kubedata *(rw,sync,no_subtree_check,insecure)
  
  mkdir -p /srv/nfs/kubedata
root@nfs:~# chmod -R 777 /srv/nfs
root@nfs:~# exportfs -avr
exporting *:/srv/nfs/kubedata

  install nfs-clinet package in client
  apt install nfs-client
  

apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-nfs-pv10
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteMany
  nfs:
    server: 
    path: "/src/nfs/kubedata"

persistent volume claim


A persistent volume claim (PVC) is a request for storage, which is met by binding the PVC to a persistent volume (PV). A PVC provides an abstraction layer to the underlying storage. For example, an administrator could create a number of static persistent volumes that can later be bound to one or more persistent volume claims. If none of the static persistent volumes match the user's PVC request, the cluster may attempt to dynamically create a new PV that matches the PVC request.
inated.

A persistent volume claim (PVC) is a request for storage, which is met by binding the PVC to a persistent volume (PV). A PVC provides an abstraction layer to the underlying storage. For example, an administrator could create a number of static persistent volumes that can later be bound to one or more persistent volume claims. If none of the static persistent volumes match the user's PVC request, the cluster may attempt to dynamically create a new PV that matches the PVC request.

apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-nfs-pv10
spec:
  storageClassName: managed-nfs-storage
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 50Mi
and attach this claim to pod spec
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    run: nginx
  name: nginx-deploy
spec:
  replicas: 1
  selector:
    matchLabels:
      run: nginx
  template:
    metadata:
      labels:
        run: nginx
    spec:
      volumes:
      - name: www
        persistentVolumeClaim:
          claimName: pvc-nfs-pv10
      containers:
      - image: nginx
        name: nginx
        volumeMounts:
        - name: www
          mountPath: /usr/share/nginx/html
  
 if pv and pvc are in stuck
  root@hanuman-Latitude-3420:/kube/kubernetes# kubectl patch pv jhooq-pv -p '{"metadata":{"finalizers":null}}'
Error from server (NotFound): persistentvolumes "jhooq-pv" not found
root@hanuman-Latitude-3420:/kube/kubernetes# kubectl patch pv pv-nfs-pv1  -p '{"metadata":{"finalizers":null}}'
persistentvolume/pv-nfs-pv1 patched
root@hanuman-Latitude-3420:/kube/kubernetes# kubectl patch pvc pvc-nfs-pv1  -p '{"metadata":{"finalizers":null}}'

 prestient volume using hostpath.
pv:
apiVersion: v1
kind: PersistentVolume
metadata:
  name: log-volume
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteMany
  storageClassName: manual
  hostPath:
    path: /opt/volume/nginx
 pvc
  apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: log-claim
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 200Mi
  storageClassName: manual
 
  apply the pvc in pod
  ---
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: logger
# pod name
  name: logger
spec:
  containers:
  - image: nginx:alpine
    name: logger
    volumeMounts:
    - name: log
      mountPath: /var/www/nginx
  volumes:
  - name: log
    persistentVolumeClaim:
        claimName: log-claim

 
Dynamic nfs:Dynamic NFS Provisioning: is allows storage volumes to be created on-demand. The dynamic provisioning feature eliminates the need for cluster administrators to code-provision storage. Instead, it automatically provisions storage when it is requested by users.
  git hub nfs external subdir:https://github.com/kubernetes-sigs/nfs-subdir-external-provisioner.git
  if archetypeon delete on true in storage class : when you delete pvc its delete the remote path
  
 network policy
  apiVersion: v1
kind: List
items:
- apiVersion: networking.k8s.io/v1
  kind: NetworkPolicy
  metadata:
    creationTimestamp: "2023-02-07T10:29:32Z"
    generation: 1
    name: np
    namespace: default
    resourceVersion: "1930"
    uid: 717f3df9-eedd-4b8b-b93e-2c1e8ec85f03
  spec:
    podSelector:
      matchLabels:
        run: secure-pod

    policyTypes:
    - Ingress
    ingress:
    - from:
        
        - podSelector:
            matchLabels:
              name: webapp-color
              
      ports:
      - protocol: TCP          
        port: 80

stateful set

StatefulSets
StatefulSet(stable-GA in k8s v1.9) is a Kubernetes resource used to manage stateful applications. It manages the deployment and scaling of a set of Pods, and provides guarantee about the ordering and uniqueness of these Pods.
StatefulSet is also a Controller but unlike Deployments, it doesn’t create ReplicaSet rather itself creates the Pod with a unique naming convention. e.g. If you create a StatefulSet with name counter, it will create a pod with name counter-0, and for multiple replicas of a statefulset, their names will increment like counter-0, counter-1, counter-2, etc
Every replica of a stateful set will have its own state, and each of the pods will be creating its own PVC(Persistent Volume Claim). So a statefulset with 3 replicas will create 3 pods, each having its own Volume, so total 3 PVCs.
For deploying the sample counter app using a statefulset, we will be using the following manifest. you can deploy it by copying the below manifest and saving it in a file e.g. statefulset.yaml, and then applying by

stateful set pv

apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-nfs-pv1
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 200Mi
  accessModes:
    - ReadWriteOnce
  nfs:
    server: 192.168.76.139
    path: "/srv/nfs/kubedata/pv1"
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-nfs-pv2
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 200Mi
  accessModes:
    - ReadWriteOnce
  nfs:
    server: 192.168.76.139
    path: "/srv/nfs/kubedata/pv2"
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-nfs-pv3
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 200Mi
  accessModes:
    - ReadWriteOnce
  nfs:
    server: 192.168.76.139
    path: "/srv/nfs/kubedata/pv3"
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-nfs-pv4
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 200Mi
  accessModes:
    - ReadWriteOnce
  nfs:
    server: 192.168.76.139
    path: "/srv/nfs/kubedata/pv4"
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-nfs-pv5
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 200Mi
  accessModes:
    - ReadWriteOnce
  nfs:
    server: 192.168.76.139
    path: "/srv/nfs/kubedata/pv5"


sts-deploy
apiVersion: v1
kind: Service
metadata:
  name: nginx-headless
  labels:
    run: nginx-sts-demo
spec:
  ports:
  - port: 80
    name: web
  clusterIP: None
  selector:
    run: nginx-sts-demo
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: nginx-sts
spec:
  serviceName: "nginx-headless"
  replicas: 4
  #podManagementPolicy: Parallel
  selector:
    matchLabels:
      run: nginx-sts-demo
  template:
    metadata:
      labels:
        run: nginx-sts-demo
    spec:
      containers:
      - name: nginx
        image: nginx
        volumeMounts:
        - name: www
          mountPath: /var/www/
  volumeClaimTemplates:
  - metadata:
      name: www
    spec:
      storageClassName: manual
      accessModes:
        - ReadWriteOnce
      resources:
        requests:
          storage: 100Mi
          
          
StatefulSets are useful in case of Databases especially when we need Highly Available Databases in production as we create a cluster of Database replicas with one being the primary replica and others being the secondary replicas. The primary will be responsible for read/write operations and secondary for read only operations and they will be syncing data with the primary one.


  
  
  
  ingress:
  helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
 helm repo update
 
 helm install myrelease ingress-nginx/ingress-nginx

An API object that manages external access to the services in a cluster, typically HTTP.

Ingress may provide load balancing, SSL termination and name-based virtual hosting.

Terminology
For clarity, this guide defines the following terms:

Node: A worker machine in Kubernetes, part of a cluster.
Cluster: A set of Nodes that run containerized applications managed by Kubernetes. For this example, and in most common Kubernetes deployments, nodes in the cluster are not part of the public internet.
Edge router: A router that enforces the firewall policy for your cluster. This could be a gateway managed by a cloud provider or a physical piece of hardware.
Cluster network: A set of links, logical or physical, that facilitate communication within a cluster according to the Kubernetes networking model.
Service: A Kubernetes Service that identifies a set of Pods using label selectors. Unless mentioned otherwise, Services are assumed to have virtual IPs only routable within the cluster network.
What is Ingress?
Ingress exposes HTTP and HTTPS routes from outside the cluster to services within the cluster. Traffic routing is controlled by rules defined on the Ingress resource.

Here is a simple example where an Ingress sends all its traffic to one Service:

ingress-diagram
Figure. Ingress

An Ingress may be configured to give Services externally-reachable URLs, load balance traffic, terminate SSL / TLS, and offer name-based virtual hosting. An Ingress controller is responsible for fulfilling the Ingress, usually with a load balancer, though it may also configure your edge router or additional frontends to help handle the traffic.

An Ingress does not expose arbitrary ports or protocols. Exposing services other than HTTP and HTTPS to the internet typically uses a service of type Service.Type=NodePort or Service.Type=LoadBalancer.




ingreess - it will route the traffic and specify the rules. suppose if the request comes from nginx.devops.com and it will route the taffic to this service(that rules we specified in yamls files)


ingress class



ingress default calss
kubectl edit ingressclass ingressclassname 
and add annontations
You can mark a particular IngressClass as default for your cluster. Setting the ingressclass.kubernetes.io/is-default-class: "true"  annotation to true on an IngressClass resource will ensure that new Ingresses without an ingressClassName field specified will be assigned this default IngressClass.





ingress sticky
Sticky sessions or session affinity, is a feature that allows you to keep a session alive for a certain period of time. In a Kubernetes cluster, all the traffic from a client to an application, even if you scale from 1 to 3 or more replicas, will be redirected to the same pod.

ANd add anotation ingress-resource yaml file
    nginx.ingress.kubernetes.io/affinity: "cookie"
    nginx.ingress.kubernetes.io/session-cookie-name: "route"
    nginx.ingress.kubernetes.io/session-cookie-expires: "172800"
    nginx.ingress.kubernetes.io/session-cookie-max-age: "172800"

  job:
  suppose if the pod is deleted it will recreate the again until the job should be execute

if the pod fails the job will run another pod until the  job should be execute

completions(non parrallel) -  if you specify 2 it will execute 2 jobs one after another

parallelism - if you specify 2 it will execute 2 jobs at a same time

backofflimit --  if you specify 3 , the iteration wil occur 4 pod fails then it will stops the job

activedeadlineseconds --- i dont want the job to long runner if you specify the time limit the time limit excedes then it will not run 



cronjob --- it will run the job on the  specific time


successfuljobhistorylimit  ---- if u specify 2 the 2 succesfull jobs will be there

failedjobhistorylimit --- f u specify 2 the 2 failed  jobs will be there



suspend if you specify true the job will be suspend



how to delete jobs automatic
in the job spec ttlsecafterfinishedjobs: 10
aftercjob completion it will wait 10 sec then the job will delete





init container - init container runs before the actual container run . if th init container sucessfull executed then only process with actual container. if the init container fails it will not start actual container , if fails it will restart the init container again

if you have multiple init  container it will start the sequences one init container another


pause container -pause container is the container that hold all the containers of a pod together
pause container is always created before the mai container

pause container is infrastracure container whose sole purpose to all these namespaces

all user defined containers of the pod then use the namespace of the pod infrastracure container

when u stop pause container the kubernetes detects the pod is unhealty and it will recreate again the pod then ipaddress will change

when u stop main container it will not affect to pod but restart increment no ipaddress will change



how the config map applies in a pod
k create cm time-config --from-literal=TIME_FREQ=10 -n dvl1987
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: time-check
  name: time-check
  namespace: dvl1987
spec:
  containers:
  - image: busybox
    name: time-check
    volumeMounts:
      - name: vol
        mountPath: /opt/time
    
    env:
      - name: TIME_FREQ
        valueFrom:
          configMapKeyRef:
            name: time-config
            key: TIME_FREQ
    command: ["/bin/sh", "-c", "while true; do date; sleep $TIME_FREQ;done > /opt/time/time-check.log"]
    resources: {}
  volumes:
    - name: vol
      emptyDir: {}


  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
 
 test 1:
    Create a redis deployment with the following parameters:
Name of the deployment should be redis using the redis:alpine image. It should have exactly 1 replica.
The container should request for .2 CPU. It should use the label app=redis.
It should mount exactly 2 volumes.

a. An Empty directory volume called data at path /redis-master-data.
b. A configmap volume called redis-config at path /redis-master.
c. The container should expose the port 6379.
The configmap has already been created.
