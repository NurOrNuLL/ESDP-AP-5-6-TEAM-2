from models.own.models import Own
from models.contractor.models import Contractor
from django.shortcuts import get_object_or_404


class OwnServices:
    @staticmethod
    def create_own(data: dict, contractor_id: int) -> Own:
        return Own.objects.create(
            name=data['name'],
            number=data['number'],
            contractor=get_object_or_404(Contractor, id=contractor_id)
        )

    @staticmethod
    def delete_own(own_id: int) -> None:
        own = get_object_or_404(Own, id=own_id)
        own.delete()
