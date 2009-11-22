from zope.interface import implements

from interfaces import (IWFElementDescription, IWFDescription, 
    IStateDescription, ITransitionDescription, IWFChildElementDescription)

from Acquisition import aq_parent, aq_inner
    
class ItemToWFElementDesc(object):
    implements(IWFElementDescription)
    
    def __init__(self, obj):
        self.obj = obj
    
    @property
    def id(self):
        return self.obj.id
    
    @property
    def title(self):
        return self.obj.title
    
    @property 
    def description(self):
        return self.obj.description
    
class ItemToWFChildElementDesc(ItemToWFElementDesc):
    implements(IWFChildElementDescription)
    
    @property
    def wf_description(self):
        return IWFDescription(aq_parent(aq_parent(aq_inner(self.obj)))) 
        
class DCWFDefToWFDesc(ItemToWFElementDesc):
    implements(IWFDescription)
    
    @property
    def state_ids(self):
        return self.obj.states.objectIds()
    
    def state(self, state_id):
        return StateDefToStateDesc(self.obj.states[state_id])
    
    @property
    def states(self):
        return [self.state(s_id) for s_id in self.state_ids]
    
    @property
    def transition_ids(self):
        return self.obj.transitions.objectIds()
    
    def transition(self, transition_id):
        t_obj = self.obj.transitions[transition_id]
        return TransitionDefToTransitionDesc(t_obj)
    
    @property
    def transitions(self):
        return [self.transition(t_id) for t_id in self.transition_ids]
    
    @property
    def initial_state_id(self):
        return self.obj.initial_state
        
    @property
    def initial_state(self):
        return self.state(self.initial_state_id)
    
    @property
    def permission_ids(self):
        return self.obj.permissions
            
    @property
    def role_ids(self):
        return self.obj.getAvailableRoles() 
        
class StateDefToStateDesc(ItemToWFChildElementDesc):
    implements(IStateDescription)
    
    @property
    def transition_ids(self):
        return self.obj.getTransitions()
    
    @property
    def transitions(self):
        return [
            self.wf_description.transition(t_id) 
            for t_id in self.transition_ids
        ]
        
    def role_ids(self, permission_id):
        return self.obj.getPermissionInfo(permission_id)['roles']
    
    
    def permission_ids(self, role_id):
        p_ids = set()        
        for p_id in self.wf_description.permission_ids:
            if role_id in self.role_ids(p_id):
                p_ids.add(p_id)
        
        return p_ids            
        
            
    def role_has_permission(self, role_id, permission_id):
        return permission_id in self.permission_ids(role_id)
    
    def permission_has_role(self, permission_id, role_id):
        return role_id in self.role_ids(permission_id)
    
    @property
    def is_initial_state(self):
        return self.id == self.wf_description.initial_state_id
    
    def acquired(self, permission_id):
        return self.obj.getPermissionInfo(permission_id)['acquired']
    
class TransitionDefToTransitionDesc(ItemToWFChildElementDesc):
    implements(ITransitionDescription)
    
    @property
    def title(self):
        """Override: ItemToWFChildElementDesc"""
        return self.obj.actbox_name    
    
    @property
    def dest_state_id(self):
        return self.obj.new_state_id
    
    @property
    def dest_state(self):
        return self.wf_description.state(self.dest_state_id)
         
    @property
    def guard_summary(self):
        return self.obj.getGuardSummary()
    
   
