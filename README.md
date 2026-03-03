ROS 2 Bag Connectivity for BEVFusion Object Detection

A ROS 2 package for running object detection with BEVFusion using raw PointCloud2 data from recorded ROS 2 bag files.
Unlike many datasets that preprocess LiDAR data, this package is tailored for bag files without a LiDAR preprocessing pipeline.

This makes it ideal for working with raw sensor recordings where preprocessing nodes were not used during data capture.

The pipeline input topic: /points 

The input topic name can be configured using the arguments of the relay1 node.

The pipeline output topic: //sensing/lidar/concatenated/pointcloud 

The output topic name can be configured using the arguments of the relay3 node.
