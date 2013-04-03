from __future__ import unicode_literals

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

    class Meta:
        abstract = True

    def __unicode__(self):
        return 'Report on {0}'.format(self.created.date())

    def cancel(self, save=True):
        """Cancels this report if it is currently active."""
        self.active=False
        if save:
            self.save()

    @property
    def patient(self):
        """Retrieves the patient record associated with this report.

        If the caller requires that the patient record actually exist, it must
        ensure that the return value is not None.
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

        If the caller requires that the provider record actually exist, it
        must ensure that the return value is not None.
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
