from notebook import notebookapp
import urllib
import json
import os
import ipykernel
import random
import numpy as np
import torch
import pickle

from jupyter_server import serverapp
from jupyter_server.utils import url_path_join
from pathlib import Path
import re
import requests

def to_pickle(filename, obj):
    with open(filename, mode='wb') as f:
        pickle.dump(obj, f)
        
def unpickle(filename):
    with open(filename, mode='rb') as fo:
        p = pickle.load(fo)
    return p 




def get_notebook_path():
    kernelIdRegex = re.compile(r"(?<=kernel-)[\w\d\-]+(?=\.json)")
    kernelId = kernelIdRegex.search(get_ipython().config["IPKernelApp"]["connection_file"])[0]
    
    for jupServ in serverapp.list_running_servers():
        for session in requests.get(url_path_join(jupServ["url"], "api/sessions"), params={"token": jupServ["token"]}).json():
            if kernelId == session["kernel"]["id"]:
                return str((Path(jupServ["root_dir"]) / session["notebook"]['path'])).replace('\\', '/')