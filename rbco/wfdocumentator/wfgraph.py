from zope.i18n import translate
from StringIO import StringIO
from interfaces import IWFGraph, IWFDescription
from prdg.util.file import process_str_as_file_out
from zope.interface import implements
import rbco.commandwrap.decorators as cmdwrap

@cmdwrap.retain_only_output
@cmdwrap.check_status
@cmdwrap.run_command
@cmdwrap.wrap_command(
    'dot -T%(output_type)s %(kwargs)s %(input_filename)s'
)
def dot(input_filename, output_type='png', **kwargs): pass

def dots(input_str, *args, **kwargs):
    return process_str_as_file_out(input_str, dot, *args, **kwargs)


class WFDescToWFGraph(object):
    implements(IWFGraph)
    
    def __init__(self, wf_desc):
        self.wf_desc = wf_desc
        self.request = self.wf_desc.obj.REQUEST
    
    def _(self, text):
        return translate(text, domain='plone', context=self.request)
    
    def render(self, format='png'):
        wf = self.wf_desc
        out = StringIO()
        
        print >> out, u'digraph {'
        
        for s in wf.states:
            if s.is_initial_state:
                attrs = u'[color=grey, style = filled]'
            else:
                attrs = u''
            
            print >> out, u'"%s" %s;' % (self._(s.title), attrs)
        
        for s in wf.states:
            for t in s.transitions:              
                print >> out, (
                    u'"%s" -> "%s" [label="%s"];' 
                    % (self._(s.title), self._(t.dest_state.title), self._(t.title))
                )

        print >> out, u'}'        
        
        graph_desc = out.getvalue().encode('utf8')
        
        if format == 'dot':
            return graph_desc
        
        return dots(graph_desc, output_type=format)