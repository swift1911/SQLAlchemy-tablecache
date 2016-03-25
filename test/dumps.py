import sys, traceback, Ice

status = 0
ic = None
try:
    ic = Ice.initialize(sys.argv)
except:
    traceback.print_exc()
    status = 1

if ic:
    try:
        ic.destroy()
    except:
        traceback.print_exc()
        status = 1

sys.exit(status)
