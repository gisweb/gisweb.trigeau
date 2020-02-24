# -*- coding: utf-8 -*-
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.namedfile import field as namedfile
from plone.supermodel import model
# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
# from zope import schema
from zope.interface import implementer
import datetime
from datetime import date
from zope import schema
from zope.interface import invariant, Invalid
from z3c.form import button
from z3c.form.interfaces import ActionExecutionError
from z3c.form.interfaces import WidgetActionExecutionError



from gisweb.trigeau import _


class IMappaSimulazione(model.Schema):
    """ Marker interface and Dexterity Python Schema for MappaSimulazione
    """
    # If you want, you can load a xml model created TTW here
    # and customize it in Python:

    # model.load('mappa_simulazione.xml')

    # directives.widget(level=RadioFieldWidget)
    # level = schema.Choice(
    #     title=_(u'Sponsoring Level'),
    #     vocabulary=LevelVocabulary,
    #     required=True
    # )

    # text = RichText(
    #     title=_(u'Text'),
    #     required=False
    # )

    # url = schema.URI(
    #     title=_(u'Link'),
    #     required=False
    # )

    # fieldset('Images', fields=['logo', 'advertisement'])
    # logo = namedfile.NamedBlobImage(
    #     title=_(u'Logo'),
    #     required=False,
    # )

    start = schema.Date(
        title=u'First day of the conference',
        required=False,
        default=date(2019, 10, 21),
    )

    end = schema.Date(
        title=u'First day of the conference',
        required=False,
        default=date(2019, 10, 21),
    )

    file_simulazione = namedfile.NamedBlobFile(
        title=_(u'File di simulazione (file SWMM5)'),
        required=True,
    )

    directives.read_permission(notes='cmf.ManagePortal')
    directives.write_permission(notes='cmf.ManagePortal')
    notes = RichText(
        title=_(u'Secret Notes (only for site-admins)'),
        required=False
    )



@implementer(IMappaSimulazione)
class MappaSimulazione(Container):
    """
    """

    start = datetime.date.today()
    end = datetime.date.today()



    def pippo(self):
        #import pdb;pdb.set_trace()

        return 'pippo'

def pippo(MappaSimulazione, event):
    import os.path
    import pdb;pdb.set_trace()

    save_path = '/plone/trigeau5/'
    file_name = 'cicciobello.inp'
    completeName = os.path.join(save_path, file_name)         
    file1 = open(completeName, "wb")
    file1.write(MappaSimulazione.file_simulazione.data)
    file1.close()
    return 'ok'
