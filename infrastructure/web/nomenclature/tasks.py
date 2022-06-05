from celery import shared_task
from celery_progress.backend import ProgressRecorder
from services.nomenclature_services import NomenclatureService


@shared_task(bind=True)
def get_services_task(self, nomenclature_pk, extension):
    progress_recorder = ProgressRecorder(self)
    nomenclatures = NomenclatureService.get_all_nomenclatures()
    if nomenclatures:
        for i, nomenclature in enumerate(list(nomenclatures)):
            if int(nomenclature_pk) == nomenclature.id:
                if nomenclature.services:
                    total_record = len(nomenclature.services)
                    for k, services in enumerate(nomenclature.services):
                        progress_recorder.set_progress(k + 1, total=total_record,
                                                       description="Inserting record into row")
                    json = {'main_data': nomenclature.services, 'extension': extension}
                    return json

    else:
        json = {'main_data': False, 'extension': extension}
        return json
