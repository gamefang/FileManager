#2018/4/15
#put '@timeit' above function to use it.

import time

def timeit(func):
    def wrapper(*args,**kw):
        start = time.clock()
        ret=func(*args,**kw)
        end = time.clock()
        print( '%s used: %s ms.' % (func.__name__,(end - start)*1000) )
        return ret
    return wrapper
