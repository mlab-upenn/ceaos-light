from setuptools import setup

setup(
    name='ceaos_light',
    version='0.0.1',
    packages=['ceaos_light'],
    install_requires=[
        'pigpio',
        'zmq',
    ],
)