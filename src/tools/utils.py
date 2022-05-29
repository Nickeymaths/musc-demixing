import os
import sys

USER_DATA_DIR = "/media/vinh/3f144d46-6de0-49c5-aedb-ede7be595d7c/user_data"

def resource_path(relative=''):
    root = getattr(sys, '_MEIPASS', os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
    return os.path.join(root, 'data', relative)
