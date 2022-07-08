#######################test code only#######################
import rosnode
import rospy
import rosgraph


def test_rosnode():
    try:
        print("master is online", rosgraph.is_master_online())
        print("core is dead", rospy.core.is_shutdown())
    except:
        print('test: error!')
    
    # master = rosgraph.Master('/rosnode')
    # print('master={}'.format(master))
    # try:
    #     print(rosnode.rosnode_ping_all())
    # except:
    #     pass

    try:
        rosnode.rosnode_listnodes()
    except:
        print('test: error!')


    ############################################################

import sys
import traceback

try:
    1/0
except Exception as e:
    print('str(Exception):\t', str(Exception))
    print('str(e):\t\t', str(e))
    print('repr(e):\t', repr(e))
    # Get information about the exception that is currently being handled  
    exc_type, exc_value, exc_traceback = sys.exc_info() 
    print('e.message:\t', exc_value)
    print("Note, object e and exc of Class %s is %s the same." % 
              (type(exc_value), ('not', '')[exc_value is e]))
    print('########################################################')
    print('traceback.print_exc(): ', traceback.print_exc())
    print('########################################################')

    print('traceback.format_exc():\n%s' % traceback.format_exc())
    print('########################################################')
