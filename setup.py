#!/usr/bin/env python

from distutils.core import setup

setup(
    name = "iwb_ros",
    version="0.0.0",
    author="Blackbird",
    author_email="jicong.ao@tum.de",
    description="IWB python package for milling machine simulation",
    license="MIT",
    packages=['iwb_ros'],
    package_data={'iwb_ros': ['script/*.sh']},
    classifiers=["Python 3.10", "Gitlab Project", "Ubuntu"],

)