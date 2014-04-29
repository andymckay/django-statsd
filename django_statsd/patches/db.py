import django
from django.db.backends import util

from django_statsd.patches.utils import wrap


def key(db, attr):
    return 'db.%s.%s.%s' % (db.client.executable_name, db.alias, attr)


def __getattr__(self, attr):
    """
    The CursorWrapper is a pretty small wrapper around the cursor.
    If you are NOT in debug mode, this is the wrapper that's used.
    Sadly if it's in debug mode, we get a different wrapper.
    """
    if django.VERSION < (1, 6) and self.db.is_managed():
        # In Django 1.6 you can't put a connection in managed mode
        self.db.set_dirty()
    if attr in self.__dict__:
        return self.__dict__[attr]
    else:
        if attr in ['execute', 'executemany']:
            def wrapped(query, *args, **kwargs):
                query_type = (query.split(None, 1) or ['__empty__'])[0].lower()
                return wrap(getattr(self.cursor, attr), key(self.db, "%s.%s" % (attr, query_type)))(query, *args, **kwargs)
            return wrapped
        return getattr(self.cursor, attr)


def wrap_class(base):
    class Wrapper(base):
        def execute(self, query, *args, **kw):
            query_type = (query.split(None, 1) or ['__empty__'])[0].lower()
            return wrap(super(Wrapper, self).execute,
                        key(self.db, 'execute.%s' % query_type))(query, *args, **kw)

        def executemany(self, query, *args, **kw):
            query_type = (query.split(None, 1) or ['__empty__'])[0].lower()
            return wrap(super(Wrapper, self).executemany,
                        key(self.db, 'executemany.%s' % query_type))(query, *args, **kw)

    return Wrapper


def patch():
    # So that it will work when DEBUG = True.
    util.CursorDebugWrapper = wrap_class(util.CursorDebugWrapper)
    # So that it will work when DEBUG = False.
    util.CursorWrapper.__getattr__ = __getattr__
