# the base class for robot modeling, including all the basic attributes and functionalities.

# Nur Entwurf


# ROS_WORKSPACE = '~/sa_ws'
# PYTHON_PKG_DIR = '~/my_pkg'
# SCRIPT_DIR = iwb_ros.__path__[0] + '/script'
# print("SCRIPT_DIR = ", SCRIPT_DIR)
# SCRIPT_LIST = {"ros_setup": './ros_setup.sh',
#                 "visualization": './robot_visualization_launch.sh',
#                 "fake_controller":'./fake_controller.sh',
#                 "ros_shutdown": './ros_shutdown.sh',
#                 "roscore_launch": './roscore_launch.sh',
#                 "motion_visualization": './moveit_script.sh',
#                 "motion_planner": './moveit_planner.sh'
#                 }
# PROCESS_HANDLE = {"visualization": '',
#                 "fake_controller": '',
#                 }
# USE_SCRIPT = {"fake_controller": False,
#                 "motion_controller": True,}

# # for those nodes who may not launch from launch file, a register must be done in main thread
# ROS_NODE_NAME ={"fake_controller": 'iwb_fake_controller',
#                 }


# class IWB_Robot_Base():
#     # flags

#     # get functions
#     # set functions


#     pass



from attr import has
from colorama import Fore
import sys
import traceback

# print Exception info in terminal
def exception_track(e):
    print(Fore.RED)
    print('##################### Exception #########################')
    print('Name:\t\t', repr(e))

    if hasattr(e, "operation"):
        print('Operation:\t', e.operation)    
    print('Description:\t', str(e))
    # print('Location:\t', e.location)    
    # Get information about the exception that is currently being handled  
    exc_type, exc_value, exc_traceback = sys.exc_info() 
    # print('details:\t', exc_type)
    # print('e.message:\t', exc_value)
    # print("Note, object e and exc of Class %s is %s the same." % 
    #           (type(exc_value), ('not', '')[exc_value is e]))
    # print('traceback.print_exc(): ', traceback.print_exc())
    print('Exception Traceback:\n%s' % traceback.format_exc())
    if not hasattr(e, "suggestion"):
        pass
    else:
        print(e.suggestion)
    # print('Exception Traceback:\n%s' % traceback.print_tb(exc_traceback))
    print('########################################################')
    print(Fore.RESET)

class Error(Exception):
    # basic class for exceptions in the package
    pass

class RosOfflineError(Error):
    # Exception raised when call ROS with Ros master offline
    description = ""
    # message = ""
    module_name = ""
    location = ""
    suggestion = ""

    def __init__(self, module_name, function_name):
        self.description = "ROS master is offline"
        self.module_name = module_name
        self.suggestion = "ROS was called when offline. Please launch ROS first!"
        # self.message = "in module " + module_name
        # self.location = "iwb_ros."+ module_name + "." + function_name
    def __str__(self):
        return self.description

class RobotNotFound(Error):
    # Exception raised when call ROS with Ros master offline
    description = ""
    # message = ""
    module_name = ""
    location = ""
    suggestion = ""

    def __init__(self, module_name, function_name):
        self.description = "IWB_Robot object was not found"
        self.module_name = module_name
        self.suggestion = "IWB_Robot object was not found. Please create a object first!"
        # self.message = "in module " + module_name
        # self.location = "iwb_ros."+ module_name + "." + function_name
    def __str__(self):
        return self.description

class NodeNotOnline(Error):
    # Exception raised when call ROS with Ros master offline
    description = ""
    # message = ""
    operation = ""
    location = ""
    suggestion = ""
    nodename = ""

    def __init__(self, module_name, operation, nodename = None):
        self.description = "Cannot kill a node"
        self.operation = operation
        self.nodename = nodename
        self.suggestion = "Cannot kill node: " + nodename +", maybe it's not alive."
        # self.message = "in module " + module_name
        # self.location = "iwb_ros."+ module_name + "." + function_name
    def __str__(self):
        return self.description

class ScriptPermissionDenied(Error):
    # Exception raised when call ROS with Ros master offline
    description = ""
    # message = ""
    module_name = ""
    location = ""
    suggestion = ""

    def __init__(self, module_name, function_name):
        self.description = "Script system permission denied"
        self.module_name = module_name
        self.suggestion = "Script was not excutable in system. Please run systempermission.sh again!"
        # self.message = "in module " + module_name
        # self.location = "iwb_ros."+ module_name + "." + function_name
    def __str__(self):
        return self.description



def main():
    try:
        raise RosOfflineError("test_module", "test_function")

    except RosOfflineError as e:
        exception_track(e)

if __name__ == "__main__":
    main()
