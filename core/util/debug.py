import globals

def dprint(*a, **k):
    if globals.DEBUG:
        print(*a, **k)