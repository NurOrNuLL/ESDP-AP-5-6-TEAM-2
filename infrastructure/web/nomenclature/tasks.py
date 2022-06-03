from celery import shared_task
from models.nomenclature.models import Nomenclature


@shared_task()
def get_services_task(nomenclature_pk, extension):
    nomenclatures = Nomenclature.objects.all()
    if nomenclatures:
        for nomenclature in list(nomenclatures):
            if int(nomenclature_pk) == nomenclature.id:
                if nomenclature.services:
                    json = {'main_data': nomenclature.services, 'extension': extension}
                    return json
    else:
        json = {'main_data': False, 'extension': extension}
        return json
