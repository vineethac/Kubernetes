## Overview
This is a sample Python based web application using FastAPI. Prometheus Python client is used to expose an endpoint for metrics.

## Docker image
* Pull image: `docker pull vineethac/fastapi-app-with-metrics:latest`

## Deploy on Kubernetes
To deploy this as a pod on K8s:  
```
❯ k run fastapi1 --image=vineethac/fastapi-app-with-metrics
pod/fastapi1 created
❯ k get po fastapi1
NAME       READY   STATUS    RESTARTS   AGE
fastapi1   1/1     Running   0          11s
```
## Verify
```
❯ k exec -it fastapi1 -- bash
root@fastapi1:/fastapi-app# ls
__pycache__  main.py  requirements.txt
root@fastapi1:/fastapi-app# pwd
/fastapi-app
root@fastapi1:/fastapi-app# curl 0.0.0.0:5000/
{"message":"welcome to using FastAPI"}root@fastapi1:/fastapi-app# curl 0.0.0.0:5000/testpage
{"message":"this is a test page"}root@fastapi1:/fastapi-app# curl 0.0.0.0:5000/date
{"date":"2023-11-19T17:23:11.770983"}root@fastapi1:/fastapi-app#
root@fastapi1:/fastapi-app# curl 0.0.0.0:5000/date
{"date":"2023-11-19T17:23:14.225068"}root@fastapi1:/fastapi-app# date
Sun Nov 19 17:23:15 UTC 2023
root@fastapi1:/fastapi-app# curl 0.0.0.0:5000/metrics
# HELP welcome_count_total count of welcome api
# TYPE welcome_count_total counter
welcome_count_total 1.0
# HELP welcome_count_created count of welcome api
# TYPE welcome_count_created gauge
welcome_count_created 1.7004144957410429e+09
# HELP testpage_count_total count of testpage api
# TYPE testpage_count_total counter
testpage_count_total 1.0
# HELP testpage_count_created count of testpage api
# TYPE testpage_count_created gauge
testpage_count_created 1.700414495741074e+09
# HELP date_count_total count of date api
# TYPE date_count_total counter
date_count_total 2.0
# HELP date_count_created count of date api
# TYPE date_count_created gauge
date_count_created 1.7004144957410867e+09
root@fastapi1:/fastapi-app#
```

You can use a K8s service to expose this app. Or you can just port forward the application from your localhost.

## API docs
* Interactive API docs can be found at `/docs`.
```
http://127.0.0.1:5000/docs
```
* Alternative API docs are available at `/redoc`.
```
http://127.0.0.1:5000/redoc
```

## Application metrics
* You can find application metrics at: `http://127.0.0.1:5000/metrics`.
* Sample metrics are as follows:  
```
# HELP welcome_count_total count of welcome api
# TYPE welcome_count_total counter
welcome_count_total 3.0
# HELP welcome_count_created count of welcome api
# TYPE welcome_count_created gauge
welcome_count_created 1.700400707814614e+09
# HELP testpage_count_total count of testpage api
# TYPE testpage_count_total counter
testpage_count_total 1.0
# HELP testpage_count_created count of testpage api
# TYPE testpage_count_created gauge
testpage_count_created 1.70040070781464e+09
# HELP date_count_total count of date api
# TYPE date_count_total counter
date_count_total 2.0
# HELP date_count_created count of date api
# TYPE date_count_created gauge
date_count_created 1.700400707814652e+09
```

## Capture and visualize metrics
You can use Prometheus to store these metrics and Grafana to visualize the data stored in Prometheus.

