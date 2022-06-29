from setuptools import setup

package_name = 'robot_ui'
_maintainer = ['matteomaragliano', 'ilmusu', 'danipari']
_maintainer_email = ['4636216@studenti.unige.it','4670261@studenti.unige.it','4670964@studenti.unige.it']

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer=_maintainer,
    maintainer_email=_maintainer_email,
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
