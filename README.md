## liquidLRU
A simple LRU cache I wrote for a personal image hosting site.

##Usage
I'll keep this short because I included a test file, so you can get an idea of the functionality from that instead.

```python
from liquidLRU import Cache

"""
    Cache constraints
    100MB of maximum storage.
    2MB maximum per cache item.
    60 Seconds is the 'default' expiry time.
    30 Seconds is when the cache will purge expired entries.
"""
c = Cache(100, 2, 60, 30)

print c.Set("hello", "world")
print c.Get("hello")
```
