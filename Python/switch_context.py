# prerequisite: pip3 install kubeconfig
# this code snipet can be used to switch to a different context

from kubeconfig import KubeConfig
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--cluster", required=True, help="K8s cluster context name"
    )

    args = parser.parse_args()
    new_context = args.cluster

    conf = KubeConfig()
    # you can specify specific kuebconfig file by conf = KubeConfig('path-to-your-kubeconfig')
    print("Kubeconfig file: ", conf.view())

    # conf_doc = conf.view()
    print("Current context: ", conf.current_context())
    conf.use_context(new_context)

    # conf_doc = conf.view()
    print("Switched to context: ", conf.current_context())


if __name__ == "__main__":
    main()
