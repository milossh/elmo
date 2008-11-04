'''Utility and help code for buildbot-mbdb adapters.'''


from datetime import datetime

from mbdb.models import Change, Tag, File


def timeHelper(t):
    if t is None:
        return t
    return datetime.utcfromtimestamp(t)


def modelForChange(change):
    try:
        dbchange = Change.objects.get(number = change.number)
        return dbchange
    except Change.DoesNotExist:
        dbchange = Change.objects.create(number = change.number,
                                         when = timeHelper(change.when))
        for prop in ('branch', 'revision', 'who', 'comments'):
            val = getattr(change, prop)
            if val:
                setattr(dbchange, prop, val)
        if hasattr(change, 'locale'):
            tag, created = Tag.objects.get_or_create(value = change.locale)
            dbchange.tags.add(tag)
        dbchange.save()
        if not change.files:
            return dbchange

        dbfiles = list(File.objects.filter(path__in = change.files))
        newfiles = set(change.files) - set(map(unicode, dbfiles))
        dbfiles += [File.objects.create(path = file) for file in newfiles]
        dbchange.files.add(*dbfiles)
        dbchange.save()
        return dbchange
