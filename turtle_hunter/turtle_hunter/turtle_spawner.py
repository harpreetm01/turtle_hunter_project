#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from rcl_interfaces.msg import SetParametersResult
from functools import partial
from math import pi
from random import uniform
from turtlesim.srv import Spawn
from turtle_hunter_interfaces.msg import Turtle, TurtleArray
from turtle_hunter_interfaces.srv import CatchTurtle
from turtlesim.srv import Kill


class TurtleSpawner(Node):
    def __init__(self):
        super().__init__("turtle_spawner")
        self.declare_parameter("spawn_rate", 0.8)
        self.declare_parameter("turtle_name_prefix", "turtle")

        self.spawn_rate = self.get_parameter("spawn_rate").value
        self.turtle_name_prefix_ = self.get_parameter("turtle_name_prefix").value

        self.turtle_counter_ = 2
        self.alive_turtles_ = []

        self.spawn_client_ = self.create_client(Spawn, "/spawn")
        self.kill_client_ = self.create_client(Kill, "/kill")

        self.spawned_turtles_pub_ = self.create_publisher(
            TurtleArray, "spawned_turtles", 10
        )
        self.catch_turtle_service_ = self.create_service(
            CatchTurtle, "catch_turtle", self.catch_turtle_callback
        )

        self.spawn_timer_ = self.create_timer(self.spawn_rate, self.call_spawn_turtle)

        self.add_on_set_parameters_callback(self.update_parameter)

        self.get_logger().info("turtle_spawner node running")

    def call_spawn_turtle(self):
        # x = uniform(0.0, 11.0)
        # y = uniform(0.0, 11.0)
        x = uniform(0.5, 10.5)
        y = uniform(0.5, 10.5)
        theta = uniform(0.0, 2 * pi)
        name = self.turtle_name_prefix_ + str(self.turtle_counter_)
        self.turtle_counter_ += 1
        self.spawn_turtle(x, y, theta, name)

    def spawn_turtle(self, x, y, theta, name):
        while not self.spawn_client_.wait_for_service(1.0):
            self.get_logger().warn("Waiting for /spawn service to be ready...")

        request = Spawn.Request()
        request.x = x
        request.y = y
        request.theta = theta
        request.name = name

        future = self.spawn_client_.call_async(request)
        future.add_done_callback(partial(self.spawn_turtle_callback, request=request))

    def spawn_turtle_callback(self, future, request: Spawn.Request):
        response: Spawn.Response = future.result()

        if response.name != "":
            self.get_logger().info(f"Spawned turtle: {response.name}")

        spawned_turtle = Turtle()
        spawned_turtle.x = request.x
        spawned_turtle.y = request.y
        spawned_turtle.theta = request.theta
        spawned_turtle.name = response.name

        self.alive_turtles_.append(spawned_turtle)
        self.publish_spawned_turtles()

    def publish_spawned_turtles(self):
        msg = TurtleArray()
        msg.turtles = self.alive_turtles_
        self.spawned_turtles_pub_.publish(msg)

    def catch_turtle_callback(
        self, request: CatchTurtle.Request, response: CatchTurtle.Response
    ):
        self.call_kill_service(request.name)
        response.success = True
        return response

    def call_kill_service(self, turtle_name):
        while not self.kill_client_.wait_for_service(1.0):
            self.get_logger().warn("Waiting for /kill service to be ready...")

        request = Kill.Request()
        request.name = turtle_name

        future = self.kill_client_.call_async(request)
        future.add_done_callback(
            partial(self.callback_call_kill_service, turtle_name=turtle_name)
        )

    def callback_call_kill_service(self, future, turtle_name):
        for i, turtle in enumerate(self.alive_turtles_):
            if turtle.name == turtle_name:
                del self.alive_turtles_[i]
                self.publish_spawned_turtles()
                break

    def update_parameter(self, params: list[Parameter]):
        for param in params:
            if param.name == "spawn_rate":
                self.spawn_rate = param.value
                if hasattr(self, "spawn_timer_") and self.spawn_timer_ is not None:
                    self.spawn_timer_.cancel()
                    self.spawn_timer_ = self.create_timer(
                        self.spawn_rate, self.call_spawn_turtle
                    )
            elif param.name == "turtle_name_prefix":
                self.turtle_name_prefix_ = param.value

        return SetParametersResult(successful=True)


def main(args=None):
    rclpy.init(args=args)
    node = TurtleSpawner()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
