from setuptools import setup

setup(
    name='spotify-manager',
    version='1.1.0',
    description='A Python 3 library wrote to simplify the basic usage of Spotipy',
    author="Marc Solé",
    author_email="marcsole@insomniacwolves.com",
    install_requires=[
        'spotipy==2.4.4',
    ],
    license='LICENSE.txt',
    packages=['spotify-account']
)
