from setuptools import find_packages, setup

setup(
    name='blog',
    version='0.9.5',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask', 'flask_admin',
        'flask_login', 'flask_sqlalchemy',
        'flask_misaka',
    ],
)