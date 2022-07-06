from models.own.models import Own
from models.contractor.models import Contractor
from typing import List


class OwnServices:
    @staticmethod
    def create_own(data: dict, contractor_id: int) -> Own:
        return Own.objects.create(
            name=data['name'],
            number=data['number'],
            comment=data['comment'],
            is_part=data['is_part'],
            contractor=Contractor.objects.get(id=contractor_id)
        )

    @staticmethod
    def delete_own(own_id: int) -> None:
        own = Own.objects.get(id=own_id)
        own.delete()

    @staticmethod
    def get_own_by_id(own_id: int) -> Own:
        return Own.objects.get(id=own_id)

    @staticmethod
    def get_own_by_contr_id(contr_id: int) -> List[Own]:
        contractor = Contractor.objects.get(id=contr_id)

        return Own.objects.filter(contractor=contractor)

    @staticmethod
    def get_owns() -> List[Own]:
        return Own.objects.all()

