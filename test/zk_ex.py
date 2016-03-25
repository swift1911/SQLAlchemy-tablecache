from kazoo.client import KazooClient
from kazoo.client import KazooState
from kazoo.exceptions import NoNodeError

zk = KazooClient(hosts='192.168.112.2:2181')


@zk.add_listener
def my_listener(state):
    if state == KazooState.LOST:
        print('lost')
    elif state == KazooState.SUSPENDED:
        print('suspend')
    else:
        print ('connect/reconnect')


zk.start()
prefix = '/'
#zk.add_auth('admin', 'test')


def get_node_by_path(prefix, node):
    try:
        global visited
        child = zk.get_children(prefix)
        if child:
            print prefix
            print child
        for c in child:
            if c not in visited:
                visited.append(prefix)
                #data, stat = zk.get(prefix)
                #print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))
                get_node_by_path(prefix + '/' + c, c)
    except NoNodeError:
        prefix = reduce(lambda x: '/' + x, map(lambda x: x, prefix.split('/')[0:len(prefix.split('/')) - 1]))
        print prefix
        return prefix
    except:
        pass


if zk.exists(prefix):
    visited = []
    try:
        get_node_by_path(prefix, [])
    except NoNodeError:
        pass
