# coding=utf8
from zope.component.hooks import getSite
from zope.i18n import translate as old_translate

_VIEW_PERMISSIONS = ('View', 'Access contents information')
_EDIT_PERMISSIONS = ('Change portal events', 'Modify portal content')


def translate(text, domain='plone'):
    # Prevents encoding errors when workflow descriptions have accentuated chars.
    if isinstance(text, str):
        text = unicode(text, 'utf8')

    return old_translate(msgid=text, domain=domain, context=getSite().REQUEST)


def iter_state_permissions(wf_description):
    """Iterator producing `(IStateDescription, permission_id, role_ids)` tuples."""
    for state_desc in wf_description.states:
        for permission_id in wf_description.permission_ids:
            yield (state_desc, permission_id, state_desc.role_ids(permission_id))
