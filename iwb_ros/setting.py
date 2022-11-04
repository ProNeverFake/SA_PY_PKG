'''
    The module to set up the running environment.
'''

import os
import sys

'''
    Didn't manage to source the ros environment from python script.
    Used the following lines to run from terminal in a subprocess instead.
'''
# os.system("cd")
# os.system(". /opt/ros/noetic/local_setup.bash")


# TODO: need to set the pypath to enable find_pkg

# append necessary directory
sys.path.append("/usr/lib/python3/dist-packages")
sys.path.append("/opt/ros/noetic/lib/python3/dist-packages")
sys.path.append("/usr/local/lib/python3.8/dist-packages")

#a hardcode directory appending for iwbrbdl
sys.path.append("/home/blackbird/iwbrbdl")

# hardcode directory for pykdl_utils (important!!!!!)
sys.path.append("/usr/local/lib/python3.8/dist-packages/pykdl_utils")
sys.path.append("")

'''
    functions for checking
'''
def get_package_path():
    return os.path.dirname(__file__) 

def get_script_dir():
    script_dir = get_package_path() + '/script'
    return script_dir

def bash_strout(print_name):
    if print_name == "script_dir":
        print(get_script_dir())
    if print_name == "package_path":
        print(get_package_path())
