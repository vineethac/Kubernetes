## Overview
* Here you have an example Python Flask app and the Dockerfile used to create its container image.
* The purpose of this is to test the Kubernetes readiness and liveness probes.
* This container image is available at: `vineethac/python-flask-healthz`

## Deploy this app in Kubernetes
* You can use the following deployment yaml spec.

```
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: py-healthz-app
  name: py-healthz-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: py-healthz-app
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: py-healthz-app
    spec:
      containers:
      - image: vineethac/python-flask-healthz:latest
        name: python-flask-healthz
        resources: {}
        livenessProbe:
          httpGet:
            path: /healthz/live
            port: 5000
          initialDelaySeconds: 90
          timeoutSeconds: 7
          periodSeconds: 30
          failureThreshold: 5
        readinessProbe:
          httpGet:
            path: /healthz/ready
            port: 5000
          initialDelaySeconds: 5
          timeoutSeconds: 22
          periodSeconds: 60
          failureThreshold: 5
status: {}

```

## Notes
* After deploying the app into a Kubernetes cluster, lets verify the response from the app.  

```
❯ kg po | grep py-healthz-app
py-healthz-app-64fd486999-vnqzn             1/1     Running   0          16m
❯
❯ k exec -it py-healthz-app-64fd486999-vnqzn -- bash
root@py-healthz-app-64fd486999-vnqzn:/#
root@py-healthz-app-64fd486999-vnqzn:/# curl http://127.0.0.1:5000
Hello World!root@py-healthz-app-64fd486999-vnqzn:/#
root@py-healthz-app-64fd486999-vnqzn:/#
root@py-healthz-app-64fd486999-vnqzn:/# curl http://127.0.0.1:5000/healthz/ready
{"status": 200, "title": "OK"}root@py-healthz-app-64fd486999-vnqzn:/#
root@py-healthz-app-64fd486999-vnqzn:/# curl http://127.0.0.1:5000/healthz/live
{"status": 200, "title": "OK"}root@py-healthz-app-64fd486999-vnqzn:/#
root@py-healthz-app-64fd486999-vnqzn:/#
root@py-healthz-app-64fd486999-vnqzn:/#
```

* Lets check application code now. The endpoints `/healthz/ready` and `/healthz/live` internally invokes the following two functions:

```
def verify_readiness():
    time.sleep(20)
    logging.info("Readiness probe OK")

def verify_liveness():
    time.sleep(5)
    logging.info("Liveness probe OK")

```
* You can also notice that when the API `http://127.0.0.1:5000/healthz/ready` is invoked, it takes 20 seconds to return the response and the API `http://127.0.0.1:5000/healthz/live` takes 5 seconds to respond. 

* In the deployment spec, the readinessProbe is set to poll `periodSeconds` the API every 60 seconds, and the `timeoutSeconds` is set to 22, because the response from the API will take around 21 seconds. If you set it to a lower number say 18, you will see readiness warnings in the pod events. Following is a sample Readiness probe failed warning when `timeoutSeconds` was set to 18.

```
❯ kg po py-healthz-app-84cb864db4-jw5mr -w
NAME                              READY   STATUS    RESTARTS   AGE
py-healthz-app-84cb864db4-jw5mr   0/1     Running   0          63s

❯ k get event --field-selector involvedObject.name=py-healthz-app-84cb864db4-jw5mr -w
LAST SEEN   TYPE     REASON      OBJECT                                MESSAGE
53s         Normal   Created     pod/py-healthz-app-84cb864db4-jw5mr   Created container python-flask-healthz
53s         Normal   Started     pod/py-healthz-app-84cb864db4-jw5mr   Started container python-flask-healthz
0s          Warning   Unhealthy   pod/py-healthz-app-84cb864db4-jw5mr   Readiness probe failed: Get "http://192.168.2.215:5000/healthz/ready": context deadline exceeded (Client.Timeout exceeded while awaiting headers)
```

* Similarly, the livenessProbe is set to poll the API every 30 seconds, and the `timeoutSeconds` is set to 7 seconds becuase the response from API will take around 7 seconds. Here if you set it to a lower value, say 4, you will see liveness warnings and the container will restart continously. Following is a sample liveness probe failed warning when `timeoutSeconds` was set to 4. You also notice that after 5 failures, its restarting the container as `failureThreshold` was set to 5.

```
❯ kg po py-healthz-app-75f64bdd48-2pknw -w
NAME                              READY   STATUS    RESTARTS   AGE
py-healthz-app-75f64bdd48-2pknw   0/1     Running   0          18s
py-healthz-app-75f64bdd48-2pknw   1/1     Running   0          80s
py-healthz-app-75f64bdd48-2pknw   0/1     Running   1 (2s ago)   4m36s

❯ k get event --field-selector involvedObject.name=py-healthz-app-75f64bdd48-2pknw -w
LAST SEEN   TYPE     REASON      OBJECT                                MESSAGE
25s         Normal   Created     pod/py-healthz-app-75f64bdd48-2pknw   Created container python-flask-healthz
25s         Normal   Started     pod/py-healthz-app-75f64bdd48-2pknw   Started container python-flask-healthz
0s          Warning   Unhealthy   pod/py-healthz-app-75f64bdd48-2pknw   Liveness probe failed: Get "http://192.168.2.217:5000/healthz/live": context deadline exceeded (Client.Timeout exceeded while awaiting headers)
0s          Warning   Unhealthy   pod/py-healthz-app-75f64bdd48-2pknw   Liveness probe failed: Get "http://192.168.2.217:5000/healthz/live": context deadline exceeded (Client.Timeout exceeded while awaiting headers)
0s          Warning   Unhealthy   pod/py-healthz-app-75f64bdd48-2pknw   Liveness probe failed: Get "http://192.168.2.217:5000/healthz/live": context deadline exceeded (Client.Timeout exceeded while awaiting headers)
0s          Warning   Unhealthy   pod/py-healthz-app-75f64bdd48-2pknw   Liveness probe failed: Get "http://192.168.2.217:5000/healthz/live": context deadline exceeded (Client.Timeout exceeded while awaiting headers)
0s          Warning   Unhealthy   pod/py-healthz-app-75f64bdd48-2pknw   Liveness probe failed: Get "http://192.168.2.217:5000/healthz/live": context deadline exceeded (Client.Timeout exceeded while awaiting headers)
0s          Normal    Killing     pod/py-healthz-app-75f64bdd48-2pknw   Container python-flask-healthz failed liveness probe, will be restarted

```

## Pod logs
* I've now reset the `timeoutSeconds` values of both probes as mentioned in the above yaml spec. Now lets see the pod logs.

```
❯ kg po py-healthz-app-64fd486999-962cq -w
NAME                              READY   STATUS    RESTARTS   AGE
py-healthz-app-64fd486999-962cq   0/1     Running   0          16s
py-healthz-app-64fd486999-962cq   1/1     Running   0          80s

❯ k logs py-healthz-app-64fd486999-962cq -f
 * Serving Flask app 'app'
 * Debug mode: on
[07-Nov-23 10:39:44] INFO: WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.2.223:5000
[07-Nov-23 10:39:44] INFO: Press CTRL+C to quit
[07-Nov-23 10:39:44] INFO:  * Restarting with stat
[07-Nov-23 10:39:45] WARNING:  * Debugger is active!
[07-Nov-23 10:39:45] INFO:  * Debugger PIN: 753-311-820
[07-Nov-23 10:41:02] INFO: Readiness probe OK
[07-Nov-23 10:41:02] INFO: 192.168.2.1 - - [07/Nov/2023 10:41:02] "GET /healthz/ready HTTP/1.1" 200 -
[07-Nov-23 10:41:47] INFO: Liveness probe OK
[07-Nov-23 10:41:47] INFO: 192.168.2.1 - - [07/Nov/2023 10:41:47] "GET /healthz/live HTTP/1.1" 200 -
[07-Nov-23 10:42:02] INFO: Readiness probe OK
[07-Nov-23 10:42:02] INFO: 192.168.2.1 - - [07/Nov/2023 10:42:02] "GET /healthz/ready HTTP/1.1" 200 -
[07-Nov-23 10:42:17] INFO: Liveness probe OK
[07-Nov-23 10:42:17] INFO: 192.168.2.1 - - [07/Nov/2023 10:42:17] "GET /healthz/live HTTP/1.1" 200 -
```

* From the logs you can see that the Readiness probe gets invoked every 60 seconds and the Liveness gets invoked every 30 seconds.

## References
* https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
* https://pypi.org/project/flask-healthz/
* https://github.com/sebinxavi/kubernetes-readiness



