#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import atan2, sqrt, pi
from functools import partial
from random import uniform
from turtle_hunter_interfaces.msg import Turtle, TurtleArray
from turtle_hunter_interfaces.srv import CatchTurtle
from rcl_interfaces.msg import SetParametersResult
from rclpy.parameter import Parameter


class TurtleController(Node):
    def __init__(self):
        super().__init__("turtle_controller")

        # self.target_x = 2.0
        # self.target_y = 8.0

        self.declare_parameter("catch_closest_turtle_first", True)

        self.catch_closest_turtle_first_ = self.get_parameter(
            "catch_closest_turtle_first"
        ).value

        self.turtle_to_catch_: Turtle = None
        self.pose_: Pose = None

        self.main_pose_sub_ = self.create_subscription(
            Pose, "/turtle1/pose", self.main_pose_callback, 10
        )
        self.spawned_turtles_sub_ = self.create_subscription(
            TurtleArray, "spawned_turtles", self.spawned_turtles_callback, 10
        )

        self.cmd_vel_pub_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)

        self.catch_turtle_client_ = self.create_client(CatchTurtle, "catch_turtle")

        self.control_loop_timer_ = self.create_timer(0.01, self.control_loop)

        self.add_on_set_parameters_callback(self.parameter_callback)

        self.get_logger().info("turtle_controller node running")

    def main_pose_callback(self, pose: Pose):
        self.pose_ = pose
        self.get_logger().info(f"{self.pose_}")

    def spawned_turtles_callback(self, msg: TurtleArray):
        if len(msg.turtles) > 0:
            if self.catch_closest_turtle_first_ == True:
                closest_turtle = None
                closest_turtle_distance = None

                for turtle in msg.turtles:
                    dist_x = turtle.x - self.pose_.x
                    dist_y = turtle.y - self.pose_.y
                    distance = sqrt(dist_x**2 + dist_y**2)

                    if closest_turtle == None or distance < closest_turtle_distance:
                        closest_turtle = turtle
                        closest_turtle_distance = distance

                self.turtle_to_catch_ = closest_turtle

            else:
                self.turtle_to_catch_ = msg.turtles[0]

    def control_loop(self):
        if self.pose_ == None or self.turtle_to_catch_ == None:
            return

        # self.target_x = uniform(0.5, 10.5)
        # self.target_y = uniform(0.5, 10.5)

        dist_x = self.turtle_to_catch_.x - self.pose_.x
        dist_y = self.turtle_to_catch_.y - self.pose_.y
        distance = sqrt(dist_x**2 + dist_y**2)

        cmd = Twist()

        if distance > 0.5:
            cmd.linear.x = 2 * distance

            goal_theta = atan2(dist_y, dist_x)
            diff = goal_theta - self.pose_.theta

            if diff > pi:
                diff -= 2 * pi
            elif diff < -pi:
                diff += 2 * pi

            cmd.angular.z = 6 * diff
        else:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0

            self.call_catch_turtle_service(self.turtle_to_catch_.name)
            self.turtle_to_catch_ = None

        self.cmd_vel_pub_.publish(cmd)

    def call_catch_turtle_service(self, turtle_name):
        while not self.catch_turtle_client_.wait_for_service(1.0):
            self.get_logger().warn("Waiting for /catch_turtle service to be ready...")

        request = CatchTurtle.Request()
        request.name = turtle_name

        future = self.catch_turtle_client_.call_async(request)
        future.add_done_callback(
            partial(self.callback_call_catch_turtle_service, turtle_name=turtle_name)
        )

    def callback_call_catch_turtle_service(self, future, turtle_name):
        response: CatchTurtle.Response = future.result()
        if not response.success:
            self.get_logger().error(f"Turtle {turtle_name} could not be removed")

    def parameter_callback(self, params: list[Parameter]):
        for param in params:
            if param.name == "catch_closest_turtle_first":
                if hasattr(self, "catch_closest_turtle_first_"):
                    self.catch_closest_turtle_first_ = param.value

        return SetParametersResult(successful=True)


def main(args=None):
    rclpy.init(args=args)
    node = TurtleController()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
