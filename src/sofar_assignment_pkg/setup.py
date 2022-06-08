from setuptools import setup

package_name = 'sofar_assignment_pkg'

data_files= []
# Default files that need to be added for the package to work
data_files.append(('share/ament_index/resource_index/packages', ['resource/'+package_name]))
data_files.append(('share/'+package_name+'/launch', ['launch/simulation.py']))
data_files.append(('share/'+package_name+'/launch', ['launch/robots_controller.py']))
data_files.append(('share/'+package_name+'/worlds', ['worlds/arena_4.wbt']))
data_files.append(('share/'+package_name+'/resource', ['resource/robot.urdf']))
data_files.append(('share/'+package_name, ['package.xml']))

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=data_files,
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='matteomaragliano',
    maintainer_email='S4636216@studenti.unige.it',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'collision_avoidance = sofar_assignment_pkg.collision_avoidance:main',
        ],
    },
)
