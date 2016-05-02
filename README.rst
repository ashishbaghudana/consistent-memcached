consistent-memcached
====================

Consistent Hashing and Automatic Failover for Memcached

Memcached is a caching daemon. This library provides a mechanism to interface with a distributed Memcached daemon using the ``python-memcached`` library. It builds on the library further to allow for consistent hashing of keys in the distributed memcached using the ``ketama`` hash-ring algorithm.

Most distinctively, ``consistent-memcached`` handles automatic failover of memcached servers. The library uses sockets to check the status of memcached servers. If a server is added or deleted, the consistent hashing algorithm is called to redistribute the keys correctly, resulting in zero downtime. Used with repcached, it is possible to replicate this data in a master-master fashion.

Usage
=====

Use the ``consistent-memcached`` library as follows::

    from consistent-memcached import ConsistentMemcachedClient
    
    client = ConsistentMemcachedClient(['127.0.0.1:11211', '127.0.0.1:11212', '127.0.0.1:11213'])
    client.set('key', 'value')
    value = client.get('key')
    
Author and Version
==================

:Authors:
 Ashish Baghudana
:Version: 0.1.0 of 02-May-2016
