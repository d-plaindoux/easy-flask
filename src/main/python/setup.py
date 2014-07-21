from distutils.core import setup

setup(
    name='fluent-rest',
    version='0.1',
    packages=['fluent_rest'],
    package_dir={'': 'src/main/python'},
    url='https://github.com/d-plaindoux/fluent-rest',
    license='LGPL ',
    author='dplaindoux',
    author_email='d.plaindoux@fungus.fr',
    description='Utilities for REST declaration using decorators'
)
