from simulator import Simulator
from parse_stage import StageParser
from scipy.spatial.transform import Rotation as R


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser("USD Loader")
    parser.add_argument("--usd_path", type=str, help="Path to usd file", required=True)
    parser.add_argument("--headless", default=False, action="store_true", help="Run stage headless")

    args, unknown = parser.parse_known_args()
    simulator = Simulator(args.headless)
    if simulator.load_stage(args.usd_path):
        print("Loading stage...")
        while simulator.kit.is_loading():
            simulator.kit.update(1.0 / 60.0)
        print("Loading complete!")

        # parse and analyze prior information from stage
        stage_parser = StageParser(simulator.get_stage())
        waypoints = stage_parser.traverse()

        # publish prior stage information
        from geometry_msgs.msg import Pose, PoseArray
        import rospy
        rospy.init_node("cad2cav_simulator", anonymous=True, log_level=rospy.INFO)
        publisher = rospy.Publisher("/simulator/stage", PoseArray, queue_size=10)

        # start simulation
        simulator.start()
        while simulator.kit.app.is_running():
            msg = PoseArray()
            msg.header.stamp = rospy.Time.now()

            for rot_mat_list in waypoints.values():
                for rot_mat in rot_mat_list:
                    r = R.from_matrix(rot_mat[0:3, 0:3])
                    q = r.as_quat()

                    pos = rot_mat[0:3, -1]

                    pose = Pose()
                    pose.orientation.w = q[0]
                    pose.orientation.x = q[1]
                    pose.orientation.y = q[2]
                    pose.orientation.z = q[3]
                    pose.position.x = pos[0]
                    pose.position.y = pos[1]
                    pose.position.z = pos[2]
                    msg.poses.append(pose)

            publisher.publish(msg)

            simulator.kit.update()
        simulator.stop()

        rospy.signal_shutdown("cad2cav_simulator complete")
