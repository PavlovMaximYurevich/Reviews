from django.http import Http404
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response

from reviews.models import Organization
from reviews.serializers import ReviewSerializer, OrganizationSerializer


class ReviewViewSet(viewsets.ModelViewSet):

    serializer_class = ReviewSerializer
    http_method_names = ('get', 'put', 'delete', 'post')
    # permission_classes = (
    #     IsAuthorAdminModer,
    # )

    def get_organization(self):
        return get_object_or_404(
            Organization,
            id=self.kwargs.get('org_id')
        )

    def get_queryset(self):
        return self.get_organization().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
             organization=self.get_organization()
        )


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
