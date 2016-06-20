from setuptools import setup
from setuptools import find_packages

def readme():
    with open('README.rst') as file:
        return file.read()

setup(
    name='consistent-memcached',
    version='0.1.0',
    description='Consistent Hashing and Automatic Failover for Memcached',
    long_description=readme(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Distributed Computing',
    ],
    keywords='consistent hashing memcached automatic failover',
    url='https://github.com/ashishbaghudana/consistent-memcached',
    author='Ashish Baghudana',
    author_email='ashish@baghudana.com',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'hash_ring>=1.0',
        'python-memcached>=1.57',
    ],
)
