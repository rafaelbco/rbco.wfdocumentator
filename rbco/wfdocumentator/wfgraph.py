from StringIO import StringIO

from zope.interface import implements
from interfaces import (IWFGraph, IWFDescription)

import rbco.commandwrap.decorators as cmdwrap
from prdg.util.file import process_str_as_file_out

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
    
    def render(self, format='png'):
        wf = self.wf_desc
        out = StringIO()
        
        print >> out, 'digraph {'
        
        for s in wf.states:
            if s.is_initial_state:
                attrs = '[color=grey, style = filled]'
            else:
                attrs = ''
                
            print >> out, '"%s" %s;' % (s.title, attrs)
        
        for s in wf.states:
            for t in s.transitions:              
                print >> out, (
                    '"%s" -> "%s" [label="%s"];' 
                    % (s.title, t.dest_state.title, t.title)
                )

        print >> out, '}'        
        
        graph_desc = out.getvalue()
        
        if format == 'dot':
            return graph_desc
        
        return dots(graph_desc, output_type=format)