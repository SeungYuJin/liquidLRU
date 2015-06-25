"""
    liquidLRUtest.py by Seung
    -------------------
    Example of how to use liquidLRU
"""
from liquidLRU import Cache

"""
    Cache constraints
    100MB of maximum storage.
    2MB maximum per cache item.
    60 Seconds is the 'default' expiry time.
    30 Seconds is when the cache will purge expired entries.
"""
c = Cache(100, 2, 60, 30)

"""
    Sets key 'hello' with a value of 'world', and inherits the default expiry time.
"""
isSet = c.Set("hello", "world")

"""
    Set() will return true or false. True if the item got added to the cache and False
    if it didn't.

    Let's have a look at cache.ExpireTime. This is the total time for the item to expire.
    (Not the time elapsed)
"""
if isSet:
    print "hello world indeed!"
    print "Expire time for key {hello} is %s" % c.Get("hello").ExpireTime

"""
    You can check if the cache has a key.
"""
if c.HasKey("hello"):
    print "Oh, hello again"

"""
    If you want to Get() a node, but don't want to refresh the expiry timer.
    Also show the value of the node.
"""
print c.Get("hello", silent=True).Value

"""
    Let's try setting an expire time for this object manually instead of using the cache default.
"""
isSet2 = c.Set("test", "123", 10)
print "Expire time for key {test} is %s" % c.Get("test").ExpireTime

"""
    Let's have a look at the size of a cached item, as well as the total size of the cache.
"""
print "Size of key {test} is %s" % c.Get("test").Size
print "Total size of our cache is %s" % c.Size

"""
    Let's see how many items are in the cache, then we'll reset the cache, and check how many items
    it has after.
"""
print "Number of items in the cache: %s" % c.Items()
c.Reset()
print "Number of items in the cache: %s" % c.Items()
