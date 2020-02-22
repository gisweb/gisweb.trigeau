# -*- coding: utf-8 -*-
from gisweb.trigeau.content.mappa_simulazione import IMappaSimulazione  # NOQA E501
from gisweb.trigeau.testing import GISWEB_TRIGEAU_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class MappaSimulazioneIntegrationTest(unittest.TestCase):

    layer = GISWEB_TRIGEAU_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_mappa_simulazione_schema(self):
        fti = queryUtility(IDexterityFTI, name='Mappa simulazione')
        schema = fti.lookupSchema()
        self.assertEqual(IMappaSimulazione, schema)

    def test_ct_mappa_simulazione_fti(self):
        fti = queryUtility(IDexterityFTI, name='Mappa simulazione')
        self.assertTrue(fti)

    def test_ct_mappa_simulazione_factory(self):
        fti = queryUtility(IDexterityFTI, name='Mappa simulazione')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IMappaSimulazione.providedBy(obj),
            u'IMappaSimulazione not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_mappa_simulazione_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='Mappa simulazione',
            id='mappa_simulazione',
        )

        self.assertTrue(
            IMappaSimulazione.providedBy(obj),
            u'IMappaSimulazione not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('mappa_simulazione', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('mappa_simulazione', parent.objectIds())

    def test_ct_mappa_simulazione_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Mappa simulazione')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_mappa_simulazione_filter_content_type_false(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Mappa simulazione')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'mappa_simulazione_id',
            title='Mappa simulazione container',
         )
        self.parent = self.portal[parent_id]
        obj = api.content.create(
            container=self.parent,
            type='Document',
            title='My Content',
        )
        self.assertTrue(
            obj,
            u'Cannot add {0} to {1} container!'.format(obj.id, fti.id)
        )
