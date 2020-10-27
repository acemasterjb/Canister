import os
from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='blog',
    author='github: acemasterjb',
    author_email='jamil.bousquet@gmail.com',
    url='https://github.com/acemasterjb/Canister',
    version='1.0.1',
    packages=find_packages(),
    include_package_data=True,
    long_desctiption=read('README.md'),
    license='AGPL-3.0',
    zip_safe=False,
    install_requires=[
        'flask>=1.1.2', 'flask_admin>=1.5.6',
        'flask_login>=0.5.0', 'flask_sqlalchemy>=2.4.4',
        'flask_misaka>=1.0.0', 'SQLAlchemy>=1.3.19'
    ],
)
