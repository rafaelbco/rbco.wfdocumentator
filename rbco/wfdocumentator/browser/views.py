from StringIO import StringIO

from Products.Five.browser import BrowserView
from rbco.wfdocumentator.interfaces import IWFDescription, IWFGraph



# TODO: create automatic tests.

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
    
    Accept "hide_roles" and "hide_permissions" in the request. The IDs of the
    roles or permissions must be delimited by ".". Example of query string:
    
    hide_roles=Anonymous.Authenticated
    &hide_permissions=Access+contents+information.List+folder+contents
    """
    
    
    def parse_seq_arg(self, arg):
        return [
            a.lower().strip()
            for a in self.request.get(arg, '').split('.')
        ]
    
    def hide_roles(self):
        return self.parse_seq_arg('hide_roles')
    
    def hide_permissions(self):
        return self.parse_seq_arg('hide_permissions')
    
    def role_ids(self):
        return [
            r for r in self.wf_description().role_ids 
            if r.lower() not in self.hide_roles()
        ]
    
    def permission_ids(self):
        return [
            p for p in self.wf_description().permission_ids 
            if p.lower() not in self.hide_permissions()
        ]        
