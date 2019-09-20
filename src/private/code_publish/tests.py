from django.test import TestCase
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from .cron import release_env_lock_cron
# Create your tests here.


class TestCodePublishCron(mixins.ListModelMixin, viewsets.GenericViewSet):

    def list(self, request, *args, **kwargs):
        release_env_lock_cron()

        return Response(status=200)