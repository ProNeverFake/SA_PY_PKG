import os
import sys

# source from the python script: failed
# alternative: add the source command to the 
# os.system("cd")
# os.system(". /opt/ros/noetic/local_setup.bash")

# TODO: need to set the pypath to enable find_pkg
sys.path.append("/usr/lib/python3/dist-packages")
sys.path.append("/opt/ros/noetic/lib/python3/dist-packages")
sys.path.append("/usr/local/lib/python3.8/dist-packages")

# hardcoding
sys.path.append("/usr/local/lib/python3.8/dist-packages/pykdl_utils")
sys.path.append("")

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
