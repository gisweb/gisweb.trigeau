# -*- coding: utf-8 -*-

from gisweb.trigeau import _
from Products.Five.browser import BrowserView
from Acquisition import aq_inner
from gisweb.trigeau.content.mappa_simulazione import IMappaSimulazione
from plone import api
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import datetime
from pyswmm import Simulation


class testView(BrowserView):
	"""
	prova
	"""

	def pippo(self):
		sim = Simulation('bovalico.inp')
		sim.execute()
		return 'cccc'







class MyView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('my_view.pt')

    def __call__(self):
        # Implement your own actions:
        self.msg = _(u'A small message')
        return self.index()


class ProgramView(BrowserView):

    def sessions(self):
        """Return a catalog search result of sessions to show."""

        context = aq_inner(self.context)
        catalog = api.portal.get_tool(name='portal_catalog')

        self.start = datetime.date.today()
        self.end = datetime.date.today()


        return catalog(
            object_provides=IMappaSimulazione.__identifier__,
            path='/'.join(context.getPhysicalPath()),
            sort_on='sortable_title')


    def __call__(self):
        # Implement your own actions:
        #self.start = datetime.date.today()
    	#self.end = datetime.date.today()
        #self.msg = _(u'A small message')
        return self.index()