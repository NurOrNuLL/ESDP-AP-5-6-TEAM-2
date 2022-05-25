from models.organization.models import Organization
from django.shortcuts import get_object_or_404


def get_organization_by_id(kwargs):
    return get_object_or_404(Organization, id=kwargs['orgID'])
