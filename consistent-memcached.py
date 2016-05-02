from consistent_hash import ConsistentHash
from memcache import Client
import socket
import time



class ConsistentMemcachedClient(Client):
    """
    Consistent Memcached Client attempts to create a scalable Memcached
    cluster that uses Consistent Hashing (using the ketama algorithm).
    In any distributed caching setup, adding or deleting servers disrupts
    the entire hashing and results in significant redistribution of keys.
    A consistent hashing function will significantly decrease the chances
    of a key being hashed to a different slot.
    
    A good explanation for the algorithm is found here:
    http://michaelnielsen.org/blog/consistent-hashing/
    """

    # The timeout period before marking a server as a dead
    _RETRY_GAP = 0.1

    def __init__(self, *args, **kwargs):
        """ 
        A memcache subclass. It currently allows you to add or delete a new 
        host at run time. It also checks if a memcache server is down and 
        automatically readjusts if a memcached server is not reachable.
        """
        super(ConsistentMemcachedClient, self).__init__(*args, **kwargs)
        self.hash_manager = ConsistentHash(self.servers)
        
    def _reconfigure_hashing(self):
        """
        If a server can be reached add it to the list of available servers.
        If a server cannot be reached, delete it from the list of available
        servers.
        """
        for server in self.servers:
            if self._is_server_alive(server, sleep=False):
                self._add_alive_server(server)
        for server in self.hash_manager.nodes:
            if not self._is_server_alive(server, sleep=False):
                self._remove_dead_server(server)            
    
    def _add_alive_server(self, server):
        """
        Add a server to the hash manager
        """
        if server not in self.hash_manager.nodes:
            self.hash_manager.add_nodes([server])
    
    def _is_server_alive(self, server, sleep=True):
        """
        Check is server is alive Client._SERVER_RETRIES times
        """
        for i in range(Client._SERVER_RETRIES):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                if not sock.connect_ex(server.address):
                    return True
                if sleep:
                    time.sleep(Client._RETRY_GAP)
            finally:
                sock.close()
        return False
        
    def _remove_dead_server(self, server):
        """
        Reconfigure hashing by removing the server that is not responding
        """
        try:
            self.hash_manager.nodes.remove(server)
            self.hash_manager = ConsistentHash(self.hash_manager.nodes)
        except ValueError:
            raise ValueError('no data store is functioning, cannot process request')
        
    def _get_server(self, key):
        """ 
        Returns the most likely server to hold the key
        """
        self._reconfigure_hashing()
        
        server = self.hash_manager.get_node(key)
        
        if not self.buckets:
            return None, None
        
        for i in range(Client._SERVER_RETRIES):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                if server and server.connect() and not sock.connect_ex(server.address):
                    return server, key
                time.sleep(Client._RETRY_GAP)
            finally:
                sock.close()
        return None, None

