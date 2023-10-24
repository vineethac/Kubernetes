# prerequisite: pip3 install kubernetes, pip3 install kubeconfig
# this sample code snipet can be used to get basic node details of a given list of clusters/ contexts

from kubernetes import client, config
from kubeconfig import KubeConfig
import argparse
import json


def get_nodes():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    return v1.list_node(_preload_content=False)


def switch_context(cluster_name):
    conf = KubeConfig()
    conf.use_context(f"{cluster_name}")
    conf_doc = conf.view()
    return conf.current_context()


def main():
    """
    This function will use the default kubeconfig file, and prints basic node details of a given context.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--cluster", required=True, help="K8s cluster context name"
    )

    args = parser.parse_args()
    all_clusters = args.cluster
    cluster_list = all_clusters.split(",")

    for cluster_name in cluster_list:
        current_context = switch_context(cluster_name)
        print(f"Current context: {current_context}")

        get_nodes_info = get_nodes()
        get_nodes_info_dict = json.loads(get_nodes_info.data)
        # print(get_nodes_info_dict)
        for each_node in get_nodes_info_dict["items"]:
            if (
                "node-role.kubernetes.io/control-plane"
                in each_node["metadata"]["labels"]
            ):
                role = "Control Plane Node"
            elif "node-role.kubernetes.io/agent" in each_node["metadata"]["labels"]:
                role = "Worker Node"

            print(
                f'{each_node["metadata"]["name"]} - {each_node["status"]["nodeInfo"]["operatingSystem"]} - {role}'
            )

        print("------------------------------------------")


if __name__ == "__main__":
    main()
