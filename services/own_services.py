from models.own.models import Own
from models.contractor.models import Contractor


class OwnServices:
    @staticmethod
    def create_own(data: dict, contractor_id: int) -> Own:
        return Own.objects.create(
            name=data['name'],
            number=data['number'],
            contractor=Contractor.objects.get(id=contractor_id)
        )

    @staticmethod
    def delete_own(own_id: int) -> None:
        own = Own.objects.get(id=own_id)
        own.delete()

    @staticmethod
    def get_own_by_id(kwargs: dict) -> Own:
        return Own.objects.get(id=kwargs['ownID'])
