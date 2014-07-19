from distutils.core import setup

setup(
    name='easy-flask',
    version='0.1',
    packages=['easy_flask'],
    package_dir={'': 'src/main/python'},
    url='https://github.com/d-plaindoux/easy-flask',
    license='LGPL ',
    author='dplaindoux',
    author_email='d.plaindoux@fungus.fr',
    description='Utilities for REST declaration using annotations'
)
