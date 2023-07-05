# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

setup(
    name='p_gpio',
    version='v1.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['test_pwr = panthyr_gpio.test_pwr:power_up'],
    },
)
