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

