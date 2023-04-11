from setuptools import find_packages, setup

version='0.1.0'

setup(
    name='certbot-installer-copy',
    version=version,
    maintainer='Jack Wearden',
    maintainer_email='jack@jackwearden.co.uk',
    description='Simple file copy installer for certbot',
    keywords='letsencrypt certbot installer',
    url='https://github.com/NotBobTheBuilder/certbot-installer-copy',
    license='Apache License 2.0',
    python_requires='>=3.6',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'acme',
        'certbot',
        'setuptools',
    ],
    extras_require={
        'test': [ 'pytest' ],
    },
    entry_points={
        'certbot.plugins': [
            'copy-installer = copy_installer:CopyInstaller',
        ],
    },
)
