from geometry_msgs.msg import PoseArray, Pose
from scipy.spatial.transform import Rotation as R


class StagePublisher:
    def __init__(self, pub) -> None:
        self.pub = pub

    def publish(self, waypoints: dict, timestamp) -> None:
        msg = PoseArray()
        msg.header.stamp = timestamp

        for rot_mat in waypoints.values():
            r = R.from_matrix(rot_mat[0:3, 0:3])
            q = r.as_quat()

            pos = rot_mat[-1, 0:3]

            pose = Pose()
            pose.orientation.w = q[0]
            pose.orientation.x = q[1]
            pose.orientation.y = q[2]
            pose.orientation.z = q[3]
            pose.position.x = pos[0]
            pose.position.y = pos[1]
            pose.position.z = pos[2]
            msg.poses.append(pose)

        self.pub.publish(msg)
