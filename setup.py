import os
from setuptools import setup

setup(
    name = "gin_tune",
    version = "0.0.1",
    author = "Sergei Volodin",
    author_email = "etoestja1@gmail.com",
    description = ("Integration between gin-config and ray tune"),
    license = "BSD",
    keywords = "gin gin-config tune ray",
    url = "https://github.com/sergeivolodin/gin_tune",
    packages=['src'],
    package_dir={"": "src"},
    install_requires=['ray[tune]', 'gin-config'],
    classifiers=[
        "License :: OSI Approved :: BSD License",
    ],
)

