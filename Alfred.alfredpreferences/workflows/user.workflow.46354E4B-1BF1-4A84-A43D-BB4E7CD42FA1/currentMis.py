import sys

from utils import get_args, wf


def main(workflow):
    query, mis, cache_seconds = get_args()
    sys.stdout.write(mis)


if __name__ == "__main__":
    sys.exit(wf().run(main))
