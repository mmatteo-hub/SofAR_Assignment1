from setuptools import setup

package_name = 'assignment_pkg'

data_files=[]
data_files.append(('share/ament_index/resource_index/packages', ['resource/' + package_name]))
data_files.append(('share/' + package_name + '/launch', ['launch/assignment_launch.py']))
data_files.append(('share/' + package_name + '/worlds', ['worlds/factory.wbt']))
data_files.append(('share/' + package_name + '/resource', ['resource/tiago_robot.urdf']))
data_files.append(('share/' + package_name, ['package.xml']))

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=data_files,
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='matteoamaragliano',
    maintainer_email='S4636216@studenti.unige.it',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'controller = assignment_pkg.controller:main',
        ],
    },
)