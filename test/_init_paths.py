
"""Set up paths. it is form Fast R-CNN."""

import os.path as osp
import sys

def add_path(path):
    if path not in sys.path:
        sys.path.insert(0, path)

this_dir = osp.dirname(__file__)

core_path = osp.join(this_dir, '..')
add_path(core_path)

