from sqlalchemy import event
import uuid
from redis.client import Redis
import pickle
import itertools


class BaseRedisClient(object):
    def __init__(self, host='127.0.0.1', port=6379, db=0, passwd=None):
        self.redissession = Redis(host, port, db, passwd)

    def set(self, pk, uuid, app_id, o, _):
        try:
            self.redissession.setex('{0}_{1}_{2}'.format(app_id, uuid, pk), pickle.dumps(o))
        except:
            pass

    def get(self, pk, uuid, app_id, _):
        try:
            return pickle.loads(self.redissession.get('{0}_{1}_{2}'.format(app_id, uuid, pk)))
        except:
            pass


class SQLAlchemyHook(BaseRedisClient):
    def __init__(self, session, tables=None):
        self.session = session
        self.tables = tables or set()
        super(SQLAlchemyHook).__init__()
        self._reg_hook()

    def _reg_hook(self):
        event.listen(self.session, 'after_commit', self._session_commit)
        event.listen(self.session, 'before_flush', self._session_update)

    def _session_update(self, session):
        self._session_init(session)
        session.todo_write |= set(session.new)
        session.todo_update |= set(session.dirty)
        session.todo_delete |= set(session.delete)

    def _session_commit(self, session):
        self._session_init(session)
        self._update_pk()

    def _update_pk(self):
        if not hasattr(self.session, 'pending_write'):
            self.session.pending_write = {}
        if not hasattr(self.session, 'pending_update'):
            self.session.pending_update = {}
        if not hasattr(self.session, 'pending_rawdata'):
            self.session.pending_rawdata = {}
        for obj in itertools.chain(self.session.pending_write,
                                   self.session.pending_update):
            key = obj.pk, obj.__tablename__

            self.session.pending_rawdata[key] = obj.__rawdata__, obj.__class__

        for k, v in self.session.pending_rawdata.iteritems():
            self.set(k, self.session.uuid, '', v)

    def _session_init(self, session):
        if hasattr(session, 'uuid'):
            return
        for action in ("add", "update", "delete"):
            attr = "todo_%s" % action
            if not hasattr(session, attr):
                setattr(session, attr, set())
        session.uuid = uuid.uuid4().hex
        return session
