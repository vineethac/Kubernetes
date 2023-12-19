from kubernetes import client, config
import argparse


def load_kubeconfig(kubeconfig_file, context_name):
    try:
        config.load_kube_config(
            config_file=f"{kubeconfig_file}", context=f"{context_name}"
        )
    except config.ConfigException as err:
        print(err)
        raise Exception("Could not configure kubernetes python client!")
    v1 = client.CoreV1Api()
    return v1


def create_ns(v1, ns_name):
    print("Creating namespace")
    namespace = client.V1Namespace(metadata={"name": ns_name})
    ret = v1.create_namespace(namespace)
    print(ret)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--context", required=True, help="K8s context")
    parser.add_argument("-f", "--file", required=False, help="Kubeconfig file")
    args = parser.parse_args()

    if not args.file:
        kubeconfig_file = "~/.kube/config"
    else:
        kubeconfig_file = args.file

    context = args.context

    v1 = load_kubeconfig(kubeconfig_file, context)

    ns_name = input("Enter namespace name: ")
    create_ns(v1, ns_name)


if __name__ == "__main__":
    main()
