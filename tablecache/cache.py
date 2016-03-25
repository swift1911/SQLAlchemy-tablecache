from hook import CacheMixin


def gen_cache_region(session, app_id, redis_session, expire_time):
    class Cache(CacheMixin):
        _session = session
        _app_id = app_id
        _redis_session = redis_session
        _expire_time = expire_time

    return Cache
