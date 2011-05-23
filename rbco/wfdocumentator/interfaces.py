from zope.interface import Interface, Attribute

class IWFElementDescription(Interface):
    
    id = Attribute(u'ID')
    title = Attribute(u'Title')
    description = Attribute(u'Title')
    
class IWFChildElementDescription(IWFElementDescription):
    
    wf_description = Attribute(u'The parent IWFDescription')    
    
class IWFDescription(IWFElementDescription):
    
    state_ids = Attribute(u'Sequence of IDs.')
    
    states = Attribute(u'Sequence of IStateDescription.')
    
    def state(state_id):
        """Return the IStateDescription correspondent to the given ID."""
            
    transition_ids = Attribute(u'Sequence of IDs.')    
    transitions = Attribute(u'Sequence of ITransitionDescription.')

    def transition(state_id):
        """Return the ITransitionDescription correspondent to the given ID."""
    
    initial_state_id = Attribute(u'ID of the initial state.')    
    initial_state = Attribute(
        u' IStateDescription correspondent to initial state.'
    )
    
    permission_ids = Attribute(u'Sequence of IDs.')    
    role_ids = Attribute(u'Sequence of IDs.')
        
class IStateDescription(IWFChildElementDescription):
    
    transition_ids = Attribute(u'Sequence of IDs.')
    transitions = Attribute(u'Sequence of ITransitionDescription.')
        
    def role_ids(permission_id):
        """
        Return a sequence containing the ID of the roles for the given 
        permission ID.
        """
    
    def permission_ids(role_id):
        """
        Return a sequence containing the ID of the permissions for the given 
        role ID.
        """
    
    def role_has_permission(role_id, permission_id):
        """Return: boolean."""
    
    def permission_has_role(permission_id, role_id):
        """Return: boolean."""
    
    def is_initial_state():
        """Return: boolean."""
    
    def acquired(permission_id):
        """Are permission settings for the given permission acquired ?"""
    
class ITransitionDescription(IWFChildElementDescription):
    
    dest_state_id = Attribute(u'ID of the destination state.')
    dest_state = Attribute(u'IStateDescription.')
    
    guard_permissions = Attribute(u'Sequence of permissions IDs.')
    guard_roles = Attribute(u'Sequence of roles IDs.')
    guard_groups = Attribute(u'Sequence of group IDs.')
    guard_expression = Attribute(u'Guard expression.')
    
class IWFGraph(Interface):
    
    def render(format='png'):
        """Render an image describing the workflow."""
