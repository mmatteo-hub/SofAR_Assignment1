from setuptools import setup

package_name = 'my_commander'
_maintainers = ['matteomaragliano', 'ilmusu', 'danipari']
_maintainers_email = ['4636216@studenti.unige.it','4670261@studenti.unige.it','4670964@studenti.unige.it']

data_files = []
data_files.append(('share/ament_index/resource_index/packages', ['resource/' + package_name]))
data_files.append(('share/' + package_name, ['package.xml']))

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=data_files,
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer=_maintainers,
    maintainer_email=_maintainers_email,
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
