from __future__ import unicode_literals
import datetime
import random

from django.conf import settings

from rapidsms.tests.harness import RapidTest

from healthcare.api import client


class ReportTestBase(RapidTest):

    def setUp(self):
        # Before doing anything else, we must clear out the dummy backend
        # as this is not automatically flushed between tests.
        self.clear_healthcare_backends()

    def clear_healthcare_backends(self):
        if 'healthcare.backends.dummy' in settings.INSTALLED_APPS:
            for registry in (client.providers, client.patients):
                registry.backend._patients = {}
                registry.backend._patient_ids = {}
                registry.backend._providers = {}

    def create_patient(self, **kwargs):
        defaults = {
            'name': self.random_string(25),
            'birth_date': datetime.date.today() - datetime.timedelta(365),
            'sex': random.choice(['M', 'F'])
        }
        defaults.update(kwargs)
        return client.patients.create(**defaults)

    def create_provider(self, **kwargs):
        defaults = {
            'name': self.random_string(25),
        }
        defaults.update(kwargs)
        return client.providers.create(**defaults)
