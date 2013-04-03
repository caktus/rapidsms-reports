from django.core.management.color import no_style
from django.db import connection
from django.db.models.base import ModelBase

from reports.models import Report
from reports.tests.base import ReportTestBase


class ReportModelTestCase(ReportTestBase):
    """
    Dummy model created to test an abstract model is adapted from
    http://michael.mior.ca/2012/01/14/unit-testing-django-model-mixins/
    """
    mixin = Report

    def setUp(self):
        # Create a dummy model which extends the abstract model.
        self.model = ModelBase(
            '__TestModel__' + self.mixin.__name__,
            (self.mixin,),
            {'__module__': self.mixin.__module__},
        )

        # Create the schema for our test model.
        self._style = no_style()
        sql, _ = connection.creation.sql_create_model(self.model, self._style)

        self._cursor = connection.cursor()
        for statement in sql:
            self._cursor.execute(statement)

    def tearDown(self):
        # Delete the schema for the test model.
        sql = connection.creation.sql_destroy_model(self.model, (), self._style)
        for statement in sql:
            self._cursor.execute(statement)

    def create_report(self, **kwargs):
        return self.model.objects.create(**kwargs)

    def test_retrieve_patient(self):
        patient = self.create_patient()
        report = self.create_report(global_patient_id=patient['id'])
        self.assertEquals(report.patient, patient)

    def test_retrieve_no_patient(self):
        report = self.create_report(global_patient_id=None)
        self.assertEquals(report.patient, None)

    def test_retrieve_bad_patient(self):
        report = self.create_report(global_patient_id='bad')
        self.assertEquals(report.patient, None)

    def test_retrieve_provider(self):
        provider = self.create_provider()
        report = self.create_report(global_provider_id=provider['id'])
        self.assertEquals(report.provider, provider)

    def test_retrieve_no_provider(self):
        report = self.create_report(global_provider_id=None)
        self.assertEquals(report.provider, None)

    def test_retrieve_bad_provider(self):
        report = self.create_report(global_provider_id='bad')
        self.assertEquals(report.provider, None)

    def test_cancel(self):
        report = self.create_report()
        self.assertTrue(report.active)
        report.cancel()
        self.assertFalse(report.active)

    def test_cancel_inactive(self):
        report = self.create_report(active=False)
        self.assertFalse(report.active)
        report.cancel()
        self.assertFalse(report.active)
