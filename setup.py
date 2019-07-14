from setuptools import setup, find_packages

setup(
    name='pybugscan',
    version='0.0.1',
    description='Scans the AST for bugs',
    packages=find_packages(exclude=["test"])
)