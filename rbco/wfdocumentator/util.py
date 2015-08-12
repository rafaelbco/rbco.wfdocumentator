# coding=utf8
from zope.component.hooks import getSite
from zope.i18n import translate as old_translate


def translate(text, domain='plone'):
    # Prevents encoding errors when workflow descriptions have accentuated chars.
    if isinstance(text, str):
        text = unicode(text, 'utf8')

    return old_translate(msgid=text, domain=domain, context=getSite().REQUEST)
