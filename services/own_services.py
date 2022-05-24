from models.own.models import Own
from models.contractor.models import Contractor
from django.shortcuts import get_object_or_404


def create_own(data, contractor_id):
    Own.objects.create(
        name=data['name'],
        number=data['number'],
        contractor=get_object_or_404(Contractor, id=contractor_id)
    )


def delete_own(own_id):
    own = get_object_or_404(Own, id=own_id)
    own.delete()

