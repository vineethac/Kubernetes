# K8s NFR System Design

------------------------------------------------------------------------------------------------------------------

## Availability
### K8s infra
#### HA topology
#### AZs/ Multiple racks and DCs
#### Multiple CP nodes
#### Multiple Worker nodepools
* group nodes with same config
* helps to upgrade per nodepool
* eg: group with GPUs
* System nodepool (coredns, metrics-server, monitoring, logging) + Workload nodepools
* use taints and tolerations for scheduling workload
#### HA of container registry
#### Use multiple K8s clusters to deploy apps
#### K8s storage considerations and CSI

### K8s apps
#### Use Deployments/ STS with multiple replicas
#### Use PDBs, resource requests, QoS, pod topologySpreadConstraints
#### Use ingress and services for loadbalancing
#### Use deployment strategies like rolling, canary, blue/green

------------------------------------------------------------------------------------------------------------------

## Reliability
### K8s infra
#### Have multiple CP and Worker nodes and node pools
#### Use ingress for LB
#### Implement regular K8s cluster etcd backup
#### K8s infra monitoring/ logging to identify issues
#### Use multiple K8s clusters across AZs
#### DR site and strategy
#### Rate limiting using Istio (to avoid overloading traffic)
#### Namespace level ResourceQuotas and LimitRange
#### Perform benchmarking
#### Health check of infra components
#### K8s storage considerations and CSI
### K8s apps
#### Use multiple replicas
#### Use rolling updates to minimize downtime
#### Implement regular app backups (Use Velero)
#### App monitoring/ logging to identify issues
#### Deploy apps across multiple K8s clusters
#### Runs apps in active-active/ active-passive modes
#### Granular traffic control to apps using Istio service mesh virtual services
#### Use Circuit breaker at app level to avoid cascading of failures to other system components
#### Use readiness and liveness probes
#### QoS for pods (Guaranteed/ Burstable/ BestEffort)
#### Perform benchmarking
#### Health check of app

------------------------------------------------------------------------------------------------------------------

## Scalability
### K8s infra
* Cluster auto scaling/ Karpenter
### K8s apps
* HPA/ KEDA

------------------------------------------------------------------------------------------------------------------

## Observability
### K8s infra/ K8s apps
* Metrics (Prometheus stack)
* Logs (Loki stack)
* Traces (Jaeger and Grafana Tempo)
* Alerts (Alert manager)
* Service mesh

------------------------------------------------------------------------------------------------------------------

## Performance
### Latency
### Saturation
### Errors
### Traffic

------------------------------------------------------------------------------------------------------------------

## Security
### RBAC
### Secrets
### Netowork policies
### Audit logs
### Enforce policies/ governance using OPA Gatekeeper
### Service mesh
### Use Vault
### Zero trust between micro services
### PSP
### Vulnerability scanning of container images
------------------------------------------------------------------------------------------------------------------

## Agility
### Deployability (Ease of deploy/ upgrade)
* Use Helm charts
### Portability (Ease of moving across platforms)
* K8s backups
### Maintainability (Ease of test/ modify/ maintain)
* Microservices

------------------------------------------------------------------------------------------------------------------

## Extensibility
### Reusability
### Pluggability (Ease to integrate with other things)