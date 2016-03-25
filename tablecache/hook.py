from sqlalchemy import event
import uuid
import pickle
import itertools


class BaseCacheMixin(object):
    def __init__(self, redis_session, EXPIRE_TIME=6000):
        self._redis_session = redis_session if redis_session is None else RuntimeError('No Redis session')
        self.EXPIRE_TIME = EXPIRE_TIME

    def set(self, pk, uuid, app_id, o):
        try:
            self._redis_session.setex('{0}_{1}_{2}'.format(app_id, uuid, pk), pickle.dumps(o), self.EXPIRE_TIME)
        except:
            pass

    def get(self, pk, uuid, app_id):
        try:
            return pickle.loads(self._redis_session.get('{0}_{1}_{2}'.format(app_id, uuid, pk)))
        except:
            pass

    def delete(self, pk, uuid, app_id):
        try:
            return pickle.loads(self._redis_session.delete('{0}_{1}_{2}'.format(app_id, uuid, pk)))
        except:
            pass

    def mset(self, pk, uuid, app_id, omap):
        try:
            self._redis_session.mset('{0}_{1}_{2}'.format(app_id, uuid, pk), omap)
        except:
            pass

    def mget(self, pk, uuid, app_id):
        try:
            return self._redis_session.mget('{0}_{1}_{2}'.format(app_id, uuid, pk))
        except:
            pass

    @property
    def __rawdata__(self):
        return {i.name: getattr(self, i.name)
                for i in self.__table__.columns}

    @property
    def pk(self):
        return getattr(self, self.__mapper__.primary_key[0].name)


class CacheMixin(BaseCacheMixin):
    _expire_time = 6000
    _app_id = ''
    _session = None
    _tables = None
    _redis_session = None

    def __init__(self, session, tables=None, app_id='', redis_session=None):
        self._session = session
        self._tables = tables or set()
        self._app_id = app_id
        self._redis_session = redis_session
        self._reg_hook()
        super(CacheMixin).__init__(redis_session, self._expire_time)

    def _reg_hook(self):
        event.listen(self._session, 'after_commit', self._session_commit, session=self._session)
        event.listen(self._session, 'before_flush', self._session_update, session=self._session)

    def _session_update(self, session):
        session = self._session_init(session)
        self._update_pk(session)

    def _session_commit(self, session):
        session = self._session_init(session)
        session.todo_write |= set(session.new)
        session.todo_update |= set(session.dirty)
        session.todo_delete |= set(session.delete)

    def _update_pk(self, session):
        if not hasattr(session, 'pending_delete_rawdata'):
            session.pending_delete_rawdata = {}
        for obj in itertools.chain(session.todo_write,
                                   session.todo_update):
            key = obj.pk, obj.__tablename__

            session.pending_rawdata[key] = obj.__rawdata__, obj.__class__

        for k, v in session.pending_rawdata.iteritems():
            self.set(k, session.uuid, self._app_id, v)

        for obj in session.todo_delete:
            key = obj.pk, obj.__tablename__

            session.pending_delete_rawdata[key] = obj.__rawdata__, obj.__class__
        for k, v in session.pending_delete_rawdata.iteritems():
            self.delete(k, session.uuid, self._app_id, v)

    def _session_init(self, session):
        if hasattr(session, 'uuid'):
            return session
        for action in ("write", "update", "delete"):
            attr = "todo_%s" % action
            if not hasattr(session, attr):
                setattr(session, attr, set())
        session.uuid = uuid.uuid4().hex
        return session

    def _get_pk(self, session, pk):
        return self.get(pk, session.uuid, self._app_id)
