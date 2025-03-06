#!/usr/bin/python
# encoding: utf-8
import sys

from utils import wf

def main(workflow):
    wf().clear_cache()
    wf().add_item('clear cache success!', valid=False)
    wf().send_feedback()


if __name__ == '__main__':
    sys.exit(wf().run(main))
