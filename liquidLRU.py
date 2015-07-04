"""
    liquidLRU by Seung
    -------------------
    Just a simple cache.
"""

from threading import Timer
from time import time

"""
    This class is the object we use to store the values
    inside the cache. It contains when the item expires,
    let's us refresh it.
"""
class Node:
    def __init__(self, value, expire):
        self.ExpiresAt = time() + expire
        self.ExpireTime = expire
        self.Value  = value
        self.Size   = len(value)

    def RefreshExpire(self):
        self.ExpiresAt = time() + self.ExpireTime

    def TimeLeft(self):
        return self.ExpiresAt - time()

    def Expired(self):
        if time() > self.ExpiresAt:
            return True
        return False

class Cache:
    """
        maxSize is the max size in megabytes that the cache should store.
        nodeMax is the max size in megabytes that a cache item can be.
        nodeExpire is the number in seconds it takes for a cache item to expire.
        purgeTime is how often the cache should purge expired entries from the cache.
    """
    def __init__(self, maxSize, nodeMax, nodeExpire, purgeTime):
        self.MaxSize = maxSize * (1024*1024)
        self.NodeMax = nodeMax * (1024*1024)
        self.NodeExpire  = nodeExpire
        self.Size = 0
        self.PurgeTime = purgeTime
        self.Cache   = {}

        if self.PurgeTime > 0:
            self.ScanPurge()

    """
        Checks the cache for expired keys, and purges them.
        The timer will call this function for whatever amount of time
        the user set.
    """
    def ScanPurge(self):
        for i in self.Cache.keys():
            if self.Cache[i].Expired():
                self.Remove(i)

        Timer(self.PurgeTime, self.ScanPurge).start()

    """
        Looks for the OLDEST entry in the cache and purges it, regardless
        of whether or not it has time left in the cache.
    """
    def RemoveLowest(self):
        lowest = None

        for i in self.Cache.keys():
            if lowest == None:
                lowest = i
            else:
                if self.Cache[i].TimeLeft < self.Cache[lowest].TimeLeft:
                    lowest = i

        self.Remove(lowest)

    """
        Pretty straightforward. It gets a value from the cache from a key.
        If you pass slient as True, it won't refresh the cache expiry time.
    """
    def Get(self, key, silent=False):
        if self.HasKey(key):
            if not silent:
                self.Cache[key].RefreshExpire()
            return self.Cache[key]
        else:
            return None

    """
        We don't want to call this method directly, instead use Set.
    """
    def _setnode(self, key, value, expireTime):
        while((len(value) + self.Size) > self.MaxSize):
            self.RemoveLowest()

            if len(self.Cache.keys()) == 0:
                break

        self.Cache[key] = Node(value, expireTime)
        self.Size += self.Cache[key].Size

    """
        Sets a value in the cache.
        If key exists with the same value it refreshes it's expire time.
        If key exists and the value is different, it sets the new value.
        If key does not exist, it adds it to the cache.

        Additionally, it will return True is the item is added, and False
        if it is not. Also if you so choose, you can override the default
        time for each cache item to expire.
    """
    def Set(self, key, value, expireTime=None):
        if expireTime is None:
            expireTime = self.NodeExpire

        """
            Using len(value) should be good enough for MOST things. It's going to
            throw an error if you feed it integers or something though.

            The reason we're not using sys.sizeof() is because python tends to add
            a lot of overhead to objects, so it wouldn't be as accurate.
        """
        try:
            nodeSize = len(value)
        except:
            return False

        """
            Honestly setting max node size to 0 is dumb but we'll add it as an option,
            because I'm sure SOMEONE out there wants it, even if it is trivial to implement.
        """
        if nodeSize <= self.NodeMax or self.NodeMax == 0:
            if not self.HasKey(key):
                self._setnode(key, value, expireTime)
            else:
                if value != self.Cache[key].Value:
                    self.Remove(key)
                    self._setnode(key, value, expireTime)
                else:
                    self.Cache[key].RefreshExpire()
            return True
        return False

    """
        Returns if a key is in the cache or not.
    """
    def HasKey(self, key):
        if key in self.Cache.keys():
            return True
        return False

    """
        Removes the key from the cache and updates the cache size.
    """
    def Remove(self, key):
        if self.HasKey(key):
            self.Size -= self.Cache[key].Size
            del self.Cache[key]

    """
        How many items are currently sitting in the cache.
    """
    def Items(self):
        return len(self.Cache.keys())

    """
        Purges all keys from the cache.
    """
    def Reset(self):
        for i in self.Cache.keys():
            self.Remove(i)
