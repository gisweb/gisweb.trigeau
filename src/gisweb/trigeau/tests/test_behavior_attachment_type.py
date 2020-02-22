# -*- coding: utf-8 -*-
from gisweb.trigeau.behaviors.attachment_type import IAttachmentTypeMarker
from gisweb.trigeau.testing import GISWEB_TRIGEAU_INTEGRATION_TESTING  # noqa
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from zope.component import getUtility

import unittest


class AttachmentTypeIntegrationTest(unittest.TestCase):

    layer = GISWEB_TRIGEAU_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_behavior_attachment_type(self):
        behavior = getUtility(IBehavior, 'gisweb.trigeau.attachment_type')
        self.assertEqual(
            behavior.marker,
            IAttachmentTypeMarker,
        )
