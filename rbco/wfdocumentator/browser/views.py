from Products.Five.browser import BrowserView
from StringIO import StringIO
from rbco.wfdocumentator.interfaces import IWFDescription, IWFGraph
from rbco.wfdocumentator.util import translate as _
from Products.CMFCore.utils import getToolByName

class WFBaseView(BrowserView):
    
    def wf_description(self):
        return IWFDescription(self.context)
    
class WFGraphView(WFBaseView):
    """Render a WF definition as an image file."""

    def __call__(self):
        format = self.request.get('format', 'png').lower()
        
        if format != 'dot':
            self.request.response.setHeader('Content-type', 'image/%s' % format)
                
        return IWFGraph(self.wf_description()).render(format)        
    
class WFDocView(WFBaseView):
    """
    Render an HTML page describing the workflow.    
    
    Accept the following parameters in the request:
    - hide_roles: Sequence of role IDs to hide.
    - hide_permissions: Sequence of permission IDs to hide.
    - hide_acquire: Hide the "acquire" column.
    
    Roles and permissions IDs are delimited by a dot.
        
    hide_roles=Anonymous.Authenticated
    &hide_permissions=Access+contents+information.List+folder+contents
    """
        
    def parse_seq_arg(self, arg):
        return set(
            a.strip() 
            for a in self.request.get(arg, '').split('.')
            if a.strip()
        )

    def hide_acquire(self):
        return 'hide_acquire' in self.request    

        
    def hide_roles(self):
        return self.parse_seq_arg('hide_roles')
    
    def hide_permissions(self):
        return self.parse_seq_arg('hide_permissions')    
    
    def role_ids(self):
        return set(self.wf_description().role_ids) - self.hide_roles() 
    
    def permission_ids(self):
        return set(self.wf_description().permission_ids) - self.hide_permissions()
            
    def formatted_wf_description(self):
        translated = _(self.wf_description().description.strip())
        lines = [l.strip() for l in translated.split('- ')]
        lis = ['<li>%s</li>' % l for l in lines if l]
        return '<ul>\n' + '\n'.join(lis) + '</ul>'

    def roles_of_permission(self, permission):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        
        roles = set(
            r['name'] 
            for r in portal.rolesOfPermission(permission) 
            if r['selected']
        )
        roles &= set(self.role_ids())
                
        return u', '.join(_(r) for r in roles)

HIDE_ROLES = set(['Reader', 'Authenticated', 'Contributor', 'Member', 'Editor'])
HIDE_PERMISSIONS = set(['Change portal events', 'Access contents information'])

class WFDocUserFriendlyView(WFDocView):
    
    def hide_acquire(self):
        """Override: WFDocView"""
        return True
    
    def hide_roles(self):
        """Override: WFDocView"""
        return WFDocView.hide_roles(self) | HIDE_ROLES
    
    def hide_permissions(self):
        """Override: WFDocView"""
        return WFDocView.hide_permissions(self) | HIDE_PERMISSIONS
        
        
