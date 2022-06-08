from setuptools import setup

package_name = 'robot_driver_pkg'

data_files= []
# Default files that need to be added for the package to work
data_files.append(('share/ament_index/resource_index/packages', ['resource/'+package_name]))
data_files.append(('share/'+package_name, ['package.xml']))
# Additional files added
data_files.append(('share/'+package_name+'/launch', ['launch/robot_launch.py']))
data_files.append(('share/'+package_name+'/worlds', ['worlds/arena_4.wbt']))
data_files.append(('share/'+package_name+'/resource', ['resource/robot.urdf']))

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=data_files,
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ilmusu',
    maintainer_email='mattia.musumeci@yahoo.it',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'robot_driver = robot_driver_pkg.robot_driver:main',
            'obstacle_avoider = robot_driver_pkg.obstacle_avoider:main'
        ],
    },
)
