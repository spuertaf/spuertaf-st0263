# Deploying WordPress and MySQL on Kubernetes

## Course Details


| Information  |                   |
|--------------|      :-----:      |
| Name    | Sebastian Guerra - Juan David Prieto - Juan David Echeverri - Santiago Puerta |
| Email   | jsguerrah@eafit.edu.co - jdprietom@eafit.edu.co - jdecheverv@eafit.edu.co - spuertaf@eafit.edu.co |
| Teacher | Edwin Montoya          |
| Course  | ST0263                 |

## Description

This README provides a step-by-step guide to set up and deploy WordPress and MySQL on a Kubernetes cluster using microk8s on Google Cloud Platform (GCP).

The information and parameters of the project criteria are in the teacher's domain. In view of this situation, it remains to say that in this project all the considerations required by the teacher are partially fulfilled.

## Prerequisites

Before you begin, ensure you have `kubectl` installed and configured to point to your Kubernetes cluster. Additionally, you should have access to a GCP account and have received an invitation to join the GCP cloud.

## Installing microk8s

Install microk8s by running the following commands:

```bash
sudo snap install microk8s --classic --channel=1.28
sudo usermod -a -G microk8s $USER
sudo chown -f -R $USER ~/.kube
```

Then, restart microk8s with:

```bash
newgrp microk8s
```

## Adding Nodes to the Cluster

Add nodes to the cluster with the following commands:

```bash
microk8s add-node
microk8s kubectl get nodes
```

Verify the cluster's status with these commands:

```bash
microk8s kubectl get deployments
microk8s kubectl get nodes
microk8s kubectl get pv
microk8s kubectl get pvc
microk8s kubectl get services
```

## Configuring MySQL in Kubernetes

### Step 1: Create a Secret for MySQL

Generate the base64-encoded password and create a secret with it:

```bash
echo -n 'mysql1234' | base64
```

Create the `mysql-secret.yaml` file with the following content:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: wp-db-secrets
type: Opaque
data:
  MYSQL_ROOT_PASSWORD: bXlzcWwxMjM0
```

Apply the secret:

```bash
microk8s kubectl apply -f mysql-secret.yaml
```

### Step 2: Configure PV and PVC for MySQL

Create the `mysql-volume.yaml` file with the following content:

```yaml
kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
  name: local-storage
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: mysql-pv
spec:
  storageClassName: local-storage
  claimRef:
    name: mysql-volume
    namespace: default
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  local:
    path: /mnt
  nodeAffinity:
    required:
      nodeSelectorTerms:
        - matchExpressions:
            - key: kubernetes.io/hostname
              operator: In
              values:
                - slave-cluster-1
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-volume
  namespace: default
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
  storageClassName: local-storage
```

Apply the storage configuration:

```bash
microk8s kubectl apply -f mysql-volume.yaml
```

### Step 3: Create a Deployment for MySQL

Create the `mysql.yaml` file with the following content:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql
  labels:
    app: mysql
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
        - name: database
          image: mysql:5.7
          args:
            - "--ignore-db-dir=lost+found"
          envFrom:
            - secretRef:
                name: wp-db-secrets
          ports:
            - containerPort: 3306
          volumeMounts:
            - name: mysql-data
              mountPath: /var/lib/mysql
      volumes:
        - name: mysql-data
          persistentVolumeClaim:
            claimName: mysql-volume
```

Apply the MySQL deployment:

```bash
microk8s kubectl apply -f mysql.yaml
```

### Step 4: Create a Service for MySQL

Create the `mysql-service.yaml` file with the following content:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mysql-service
spec:
  ports:
    - port: 3306
      protocol: TCP
  selector:
    app: mysql
```

Apply the MySQL service:

```bash
microk8s kubectl apply -f mysql-service.yaml
```

## Configuring WordPress in Kubernetes

### Step 5: Configure PV and PVC for WordPress

Create the `wp-volume.yaml` file with the following content:

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: wordpress-pv
spec:
  storageClassName: local-storage
  claimRef:
    name: wordpress-volume
    namespace: default
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  local:
    path: /
  nodeAffinity:
    required:
      nodeSelectorTerms:
        - matchExpressions:
            - key: kubernetes.io/hostname
              operator: In
              values:
                - slave-cluster-1
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: wordpress-volume
  namespace: default
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: local-storage
```

Apply the storage configuration for WordPress:

```bash
microk8s kubectl apply -f wp-volume.yaml
```

### Step 6: Create a Deployment for WordPress

Create the `wp.yaml` file with the following content:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: wordpress
spec:
  replicas: 1
  selector:
    matchLabels:
      app: wordpress
  template:
    metadata:
      labels:
        app: wordpress
    spec:
      containers:
        - name: wordpress
          image: wordpress:5.8.3-php7.4-apache
          ports:
            - containerPort: 80
              name: wordpress
          volumeMounts:
            - name: wordpress-data
              mountPath: /var/www
          env:
            - name: WORDPRESS_DB_HOST
              value: mysql-service.default.svc.cluster.local
            - name: WORDPRESS_DB

_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: wp-db-secrets
                  key: MYSQL_ROOT_PASSWORD
            - name: WORDPRESS_DB_USER
              value: root
            - name: WORDPRESS_DB_NAME
              value: wordpress
      volumes:
        - name: wordpress-data
          persistentVolumeClaim:
            claimName: wordpress-volume
```

Apply the WordPress deployment:

```bash
microk8s kubectl apply -f wp.yaml
```

### Step 7: Create a Service for WordPress

Create the `wp-service.yaml` file with the following content:

```yaml
kind: Service
apiVersion: v1
metadata:
  name: wordpress-service
spec:
  type: LoadBalancer
  externalIPs:
    - 34.133.11.102
  selector:
    app: wordpress
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 80
```

Apply the WordPress service:

```bash
microk8s kubectl apply -f wp-service.yaml
```

You should now have MySQL and WordPress deployed on your Kubernetes cluster. Obtain the external IP address to access WordPress by running:

```bash
microk8s kubectl get svc wordpress-service
```

Access that IP address in your browser to configure WordPress. Ensure that your Kubernetes cluster has internet access for the LoadBalancer service to work correctly.
