rbco.wfdocumentator
===================

.. contents::

Overview
--------

This add-on for Zope and Plone aims to provide user-friendly automatically
generated documentation about workflow definitions.

Currently two Zope3-style views for
``Products.DCWorkflow.interfaces.IDCWorkflowDefinition`` are provided:

- ``@@wf-graph``: Render an image representing the workflow's states and
  transitions as a graph.
  
- ``@@wf-doc``: Render an HTML page describing the workflow. This includes
  the graph mentioned above.  
  
- ``@@wf-doc-user-friendly``: Same as ``@@wf-doc`` but hides some roles and permissions and the
  "acquire" column.

Requirements
------------

- Tested with Zope 2.10.7 + Plone 3.2.2. However only Zope 2 is required
  (hopefuly).

- Graphviz_. More precisely: there must be an executable called ``dot`` in the 
  system path and the user running Zope must have execute permission on it.
  
- Other requirements are pure Python packages registered on PyPI and distutils 
  should handle them without problems.

.. WARNING::
   It was not tested on Windows. I suspect it won't work because of the name
   of the executable, i.e ``dot`` != ``dot.exe``.

Installation
------------

This package is easy_install'able. Just make it available in your Zope Instance
and don't forget to load its ZCMLs. If you don't have any idea of what I'm
talking about please refer to `Installing an Add-on Product`_.

Usage
-----

Just use the provided views on an workflow definition. Examples (type these
URLs in your browser):

- http://localhost:8080/plone/portal_workflow/plone_workflow/@@wf-graph
- http://localhost:8080/plone/portal_workflow/plone_workflow/@@wf-doc

You can pass the following parameters to @@wf-graph in the query string:
``hide_roles`` and ``hide_permissions``. These are lists of things to hide
in the output, separated by ".". Example:

- http://localhost:8080/plone/portal_workflow/plone_workflow/@@wf-doc?hide_roles=Anonymous.Authenticated.Member&hide_permissions=Access+contents+information.List%20folder%20contents

There's also the ``hide_acquire`` parameter, which hides the "acquired" column.

To-do
-----

- Render an HTML image map, so the user can click on a state or transition
  and see its description.
  
- Test and adapt for Windows.

- Make the location of the ``dot`` executable configurable.

- Write automatic tests.

Credits
-------

- Author: Rafael Oliveira <rafaelbco@gmail.com>

- The idea of using Zope3-style views to render information about workflow 
  definitions was inspired by Martin Aspeli's `collective.wtf`_.

Contribute and report bugs
--------------------------

Help is welcome. Contact the author or file a ticket at the `Issue tracker`_.

Thanks
------

- To lucmult, for reporting the bug #2 (the one fixed in 0.0.3).

.. References
   ----------

.. _Graphviz: http://www.graphviz.org/
.. _collective.wtf: http://pypi.python.org/pypi/collective.wtf/
.. _`Issue tracker`: http://code.google.com/p/rbco-wfdocumentator/issues
.. _`Installing an Add-on Product`: http://plone.org/documentation/tutorial/third-party-products/installing





