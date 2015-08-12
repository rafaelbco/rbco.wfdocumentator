# coding=utf8
import itertools
import functools
from .util import iter_state_permissions


_VIEW_PERMISSIONS = ('View', 'Access contents information')
_EDIT_PERMISSIONS = ('Change portal events', 'Modify portal content')


def _validate_manager_in_all_permissions(wf_description):
    for (state_desc, permission_id, role_ids) in iter_state_permissions(wf_description):
        if 'Manager' not in role_ids:
            yield 'State: {}. Manager does not have permission "{}"'.format(
                state_desc.id,
                permission_id,
            )


def _validate_anonymous_conflicts_with_other_roles(wf_description):
    for (state_desc, permission_id, role_ids) in iter_state_permissions(wf_description):
        role_ids = set(role_ids)
        role_ids.difference_update({'Manager'})
        if ('Anonymous' in role_ids) and (len(role_ids) > 1):
            yield (
                'State: {}. Permission: {}. '
                'Other roles are superfulous since permission already has Anonymous role.'
            ).format(
                state_desc.id,
                permission_id,
            )


def _validate_action_url(wf_description):
    for transition_desc in wf_description.transitions:
        correct_action_url = (
            '%(content_url)s/content_status_modify?workflow_action=' + transition_desc.id
        )
        if correct_action_url != transition_desc.obj.actbox_url:
            yield 'Transition {}. Action URL should be "{}"'.format(
                transition_desc.id,
                correct_action_url
            )


def _validate_action_name(wf_description):
    for transition_desc in wf_description.transitions:
        if transition_desc.obj.title != transition_desc.obj.actbox_name:
            yield 'Transition {}. Action name ({}) different from transition title ({}).'.format(
                transition_desc.id,
                transition_desc.obj.actbox_name,
                transition_desc.obj.title,
            )


def _validate_action_category(wf_description):
    for transition_desc in wf_description.transitions:
        if transition_desc.obj.actbox_category != 'workflow':
            yield 'Transition {}. Action category should be "workflow".'.format(transition_desc.id)


def _validate_role_imply_other_role(wf_description, permission_id, role1, role2):
    for state_desc in wf_description.states:
        role_ids = state_desc.role_ids(permission_id)
        if (role1 in role_ids) ^ (role2 in role_ids):
            yield (
                'State: {}. {} and {} must be given together for permission {}. '
            ).format(state_desc.id, role1, role2,  permission_id)


def _validate_roles_conflicts(wf_description, permission_id, role1, role2):
    for state_desc in wf_description.states:
        role_ids = state_desc.role_ids(permission_id)
        if (role1 in role_ids) and (role2 in role_ids):
            yield (
                'State: {}. Roles {} and {} cannot be given together for permission {}.'
            ).format(state_desc.id, role1, role2,  permission_id)


def _validate_role_conflicts_with_permission(wf_description, role_id, permission_id):
    for state_desc in wf_description.states:
        if state_desc.role_has_permission(role_id, permission_id):
            yield 'State: {}. Role {} cannot have permission "{}".'.format(
                state_desc.id,
                role_id,
                permission_id,
            )


def _validate_permissions_must_be_equal(wf_description, permissions):
    for state_desc in wf_description.states:
        roles_for_permissions = [tuple(state_desc.role_ids(p)) for p in permissions]
        if len(set(roles_for_permissions)) > 1:
            yield 'State: {}. Permissions must have the same roles: {}'.format(
                state_desc.id,
                ', '.join(permissions)
            )


_validations_owner_imply_reader_in_view_permissions = [
    functools.partial(
        _validate_role_imply_other_role,
        permission_id=p,
        role1='Owner',
        role2='Reader'
    )
    for p in _VIEW_PERMISSIONS
]

_validations_owner_imply_editor_in_edit_permissions = [
    functools.partial(
        _validate_role_imply_other_role,
        permission_id=p,
        role1='Owner',
        role2='Editor'
    )
    for p in _EDIT_PERMISSIONS
]

_validate_reader_and_editor_roles_conflicts = [
    functools.partial(
        _validate_roles_conflicts,
        permission_id=p,
        role1='Reader',
        role2='Editor'
    )
    for p in _EDIT_PERMISSIONS + _VIEW_PERMISSIONS
]

_validate_view_permissions_must_be_equal = functools.partial(
    _validate_permissions_must_be_equal,
    permissions=_VIEW_PERMISSIONS
)
_validate_edit_permissions_must_be_equal = functools.partial(
    _validate_permissions_must_be_equal,
    permissions=_EDIT_PERMISSIONS
)

_validations_editor_conflicts_with_view_permissions = [
    functools.partial(_validate_role_conflicts_with_permission, role_id='Editor', permission_id=p)
    for p in _VIEW_PERMISSIONS
]
_validations_reader_conflicts_with_edit_permissions = [
    functools.partial(_validate_role_conflicts_with_permission, role_id='Reader', permission_id=p)
    for p in _EDIT_PERMISSIONS
]

_validations = [
    _validate_manager_in_all_permissions,
    _validate_anonymous_conflicts_with_other_roles,
    _validate_action_url,
    _validate_action_name,
    _validate_action_category,
    _validate_view_permissions_must_be_equal,
    _validate_edit_permissions_must_be_equal,
]
_validations.extend(_validations_owner_imply_reader_in_view_permissions)
_validations.extend(_validations_owner_imply_editor_in_edit_permissions)
_validations.extend(_validate_reader_and_editor_roles_conflicts)
_validations.extend(_validations_editor_conflicts_with_view_permissions)
_validations.extend(_validations_reader_conflicts_with_edit_permissions)


def validate_wf(wf_description):
    """Return a sequence of strings describing validation errors in the workflow.

    Returna an empty sequence if no errors are found.
    """
    return list(itertools.chain.from_iterable(
        assertion(wf_description) for assertion in _validations
    ))
