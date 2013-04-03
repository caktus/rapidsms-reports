from __future__ import unicode_literals
import datetime

from django.db import models

from healthcare.api import client
from healthcare.exceptions import PatientDoesNotExist, ProviderDoesNotExist


class Report(models.Model):
    """An abstract model describing the structure of a 1000 days report."""
    # Meta data.
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    # Information about the IncomingMessage from which the report was received.
    # If the report was not generated via SMS, then these fields will be
    # empty.
    raw_text = models.CharField(max_length=255, null=True, blank=True)
    connection = models.ForeignKey('rapidsms.Connection', null=True, blank=True)

    # Global identifiers, created by rapidsms-healthcare.
    global_provider_id = models.CharField(max_length=255, null=True, blank=True)
    global_patient_id = models.CharField(max_length=255, null=True, blank=True)

    # In the near future, we will want to incorporate the rapidsms facilities registry.

    # The date of the event that the report describes.
    data_date = models.DateField(null=True, blank=True, default=datetime.date.today)

    class Meta:
        abstract = True
        ordering = ['-data_date']

    def __unicode__(self):
        return 'Report created {0}'.format(self.created.date())

    def cancel(self, save=True):
        """Cancels this report if it is currently active."""
        self.active=False
        if save:
            self.save()

    @property
    def patient(self):
        """Retrieves the patient record associated with this report.

        This method returns None if self.global_patient_id is None, or if no
        patient exists with the identifier self.global_patient_id.
        """
        if not hasattr(self, '_patient'):
            if not self.global_patient_id:
                self._patient = None
            else:
                try:
                    self._patient = client.patients.get(self.global_patient_id)
                except PatientDoesNotExist:
                    self._patient = None
        return self._patient

    @property
    def provider(self):
        """Retrieves the provider record associated with this report.

        This method returns None if self.global_provider_id is None, or if no
        provider exists with the identifier self.global_provider_id.
        """
        if not hasattr(self, '_provider'):
            if not self.global_provider_id:
                self._provider = None
            else:
                try:
                    self._provider = client.providers.get(self.global_provider_id)
                except ProviderDoesNotExist:
                    self._provider = None
        return self._provider
