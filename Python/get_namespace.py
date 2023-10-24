from kubernetes import client, config
import argparse


def load_kubeconfig(context_name):
    config.load_kube_config(context=f"{context_name}")
    v1 = client.CoreV1Api()
    return v1


def get_all_namespace(v1):
    print("Listing namespaces with their creation timestamp, and status:")
    ret = v1.list_namespace()
    for i in ret.items:
        print(i.metadata.name, i.metadata.creation_timestamp, i.status.phase)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--context", required=True, help="K8s context")
    args = parser.parse_args()

    context = args.context
    v1 = load_kubeconfig(context)
    get_all_namespace(v1)


if __name__ == "__main__":
    main()
