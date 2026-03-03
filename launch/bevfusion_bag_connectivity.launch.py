from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import AnyLaunchDescriptionSource
from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory
import os


def include_launch(package_name: str, relative_launch_path: str):
    pkg_share = get_package_share_directory(package_name)
    launch_path = os.path.join(pkg_share, relative_launch_path)
    return IncludeLaunchDescription(AnyLaunchDescriptionSource(launch_path))


def generate_launch_description():
    # autoware_bevfusion bevfusion.launch.xml
    bevfusion_launch = include_launch(
        "autoware_bevfusion",
        os.path.join("launch", "bevfusion.launch.xml"),
    )

    # relay /points -> /sensing/points (relay1)
    relay1 = Node(
        package="topic_tools",
        executable="relay",
        name="relay1",
        output="screen",
        arguments=["/points", "/sensing/points"],
    )

    # ouster_point_type_adapter ouster_point_type_adapter.launch.py
    ouster_adapter_launch = include_launch(
        "ouster_point_type_adapter",
        os.path.join("launch", "ouster_point_type_adapter.launch.py"),
    )

    # relay /sensing/points_adapter_output -> /points_raw (relay2)
    relay2 = Node(
        package="topic_tools",
        executable="relay",
        name="relay2",
        output="screen",
        arguments=["/sensing/points_adapter_output", "/points_raw"],
    )

    # autoware_pointcloud_preprocessor preprocessor.launch.xml
    preprocessor_launch = include_launch(
        "autoware_pointcloud_preprocessor",
        os.path.join("launch", "preprocessor.launch.xml"),
    )

    # relay /points_raw/cropbox/filtered -> /sensing/lidar/concatenated/pointcloud (relay3)
    relay3 = Node(
        package="topic_tools",
        executable="relay",
        name="relay3",
        output="screen",
        arguments=["/points_raw/cropbox/filtered", "/sensing/lidar/concatenated/pointcloud"],
    )

    # Static TF: base_link -> os_sensor
    static_tf_base_to_os = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="static_tf_base_to_os_sensor",
        output="screen",
        arguments=["0.67", "0.0", "2.1844", "0", "0", "0", "base_link", "os_sensor"],
    )

    # Static TF: map -> base_link
    static_tf_map_to_base = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="static_tf_map_to_base_link",
        output="screen",
        arguments=["0", "0", "0", "0", "0", "0", "map", "base_link"],
    )

    return LaunchDescription([
        bevfusion_launch,
        relay1,
        ouster_adapter_launch,
        relay2,
        preprocessor_launch,
        relay3,
        static_tf_base_to_os,
        static_tf_map_to_base,
    ])