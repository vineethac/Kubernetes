# prerequisite: pip3 install kubernetes

from kubernetes import client, config


def main():
    """
    This function will use the default kubeconfig file, list the contexts, and active context.
    """

    contexts, active_context = config.list_kube_config_contexts()
    if not contexts:
        print("Cannot find any context in kube-config file.")
        return

    contexts = [context["name"] for context in contexts]
    active_index = contexts.index(active_context["name"])
    active_context = active_context["name"]

    print(f"List of contexts: {contexts}")
    print(f"Active context index is: {active_index}")
    print(f"Actice context name is: {active_context}")


if __name__ == "__main__":
    main()
