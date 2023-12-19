## Overview
In this exercise we will use Argo CD to deploy the apps we worked on in the [K8s mini project](https://github.com/vineethac/Kubernetes/tree/main/mini-project).

## Access to a K8s cluster
You should have access to a Kubernetes cluster. In my case, the kubeconfig file is `gc.kubeconfig`.

## Deploy Argo CD on the K8s cluster
Now lets deploy Argo CD to the K8s cluster.
```
❯ KUBECONFIG=gc.kubeconfig kubectl create namespace argocd
❯ KUBECONFIG=gc.kubeconfig kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```
Reference: https://vineethac.blogspot.com/2022/06/gitops-using-argo-cd-part1.html

## Deploy different components of our project to the K8s cluster using Argo CD application resource
All the Argo CD app manifests are present in the `apps-manifest` directory. We can now deploy them.

### Ingress controller
```
❯ KUBECONFIG=gc.kubeconfig kubectl create -f apps-manifest/ingress-controller.yaml
```

### Prometheus stack
```
❯ KUBECONFIG=gc.kubeconfig kubectl create -f apps-manifest/prometheus-stack.yaml
```

### FastAPI web app
```
❯ KUBECONFIG=gc.kubeconfig kubectl create -f apps-manifest/fastapi-webapp.yaml
```

### FastAPI service monitor
```
❯ KUBECONFIG=gc.kubeconfig kubectl create -f apps-manifest/fastapi-service-monitor.yaml
```

### Loki stack
```
❯ KUBECONFIG=gc.kubeconfig kubectl create -f apps-manifest/loki-stack.yaml
```

## Verify

