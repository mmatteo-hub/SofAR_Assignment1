from setuptools import setup

package_name = 'sofar_assignment'
data_files = []
data_files.append(
    ('share/ament_index/resource_index/packages', ['resource/' + package_name]))
data_files.append(('share/' + package_name + '/launch', ['launch/launch.py']))

#In case of custom resurces append them
data_files.append(('share/' + package_name + '/resource', [
    'resource/tiago1_control.yaml',
    'resource/tiago2_control.yaml',
]))

data_files.append(('share/' + package_name, ['package.xml']))
data_files.append(('share/' + package_name + '/worlds', ['worlds/office.wbt']))

setup(
    name=package_name,
    version='1.2.2',
    packages=[],
    data_files=data_files,
    install_requires=['setuptools', 'launch'],
    zip_safe=True,
    author='Cyberbotics',
    author_email='support@cyberbotics.com',
    maintainer='Cyberbotics',
    maintainer_email='support@cyberbotics.com',
    keywords=['ROS', 'Webots', 'Robot', 'Simulation', 'Examples', 'TIAGo'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description='TIAGo robots ROS2 interface for Webots.',
    license='Apache License, Version 2.0',
    tests_require=['pytest'],
    entry_points={
        'launch.frontend.launch_extension': ['launch_ros = launch_ros']
    }
)
