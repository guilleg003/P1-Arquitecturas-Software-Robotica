from setuptools import find_packages, setup

package_name = 'p1_contador'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='guille',
    maintainer_email='guille@example.com',
    description='Practica P1: publicador /saludo y nodo contador con servicio, parametro y QoS.',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'publicador_saludo = p1_contador.publicador_saludo:main',
            'contador_nodo = p1_contador.contador_nodo:main',
        ],
    },
)
