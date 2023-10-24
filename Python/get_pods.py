from kubernetes import client, config
import argparse


def load_kubeconfig(context_name):
    config.load_kube_config(context=f"{context_name}")
    v1 = client.CoreV1Api()
    return v1


def get_all_pods(v1):
    print("Listing all pods:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print(i.metadata.namespace, i.metadata.name, i.status.phase)


def get_namespaced_pods(v1, ns):
    print(f"Listing all pods under namespace {ns}:")
    ret = v1.list_namespaced_pod(f"{ns}")
    for i in ret.items:
        print(i.metadata.namespace, i.metadata.name, i.status.phase)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--context", required=True, help="K8s context")
    parser.add_argument("-n", "--namespace", required=False, help="K8s namespace")
    args = parser.parse_args()

    context = args.context
    v1 = load_kubeconfig(context)

    if not args.namespace:
        get_all_pods(v1)
    else:
        get_namespaced_pods(v1, args.namespace)


if __name__ == "__main__":
    main()
