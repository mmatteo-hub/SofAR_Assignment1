import os
from setuptools import find_packages
from setuptools import setup

setup(
    name='webots_ros2_driver_webots',
    version='1.2.2',
    packages=find_packages(
        include=('webots_ros2_driver_webots', 'webots_ros2_driver_webots.*')),
)
