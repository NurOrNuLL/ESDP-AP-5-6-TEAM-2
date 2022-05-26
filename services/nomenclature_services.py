from models.nomenclature.models import Nomenclature
from models.organization.models import Organization
from django.shortcuts import get_object_or_404


def create_nomenclature(data: dict) -> Nomenclature:
    return Nomenclature.objects.create(
        name=data['name'],
        organization=get_object_or_404(Organization, id=1)
    )
