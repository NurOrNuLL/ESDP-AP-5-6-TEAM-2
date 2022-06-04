from celery import shared_task
from models.nomenclature.models import Nomenclature
from celery_progress.backend import ProgressRecorder


@shared_task(bind=True)
def get_services_task(self, nomenclature_pk, extension):
    progress_recorder = ProgressRecorder(self)
    nomenclatures = Nomenclature.objects.all()
    total_record = nomenclatures.count()
    if nomenclatures:
        for i, nomenclature in enumerate(list(nomenclatures)):
            if int(nomenclature_pk) == nomenclature.id:
                if nomenclature.services:
                    json = {'main_data': nomenclature.services, 'extension': extension}
                    progress_recorder.set_progress(i + 1, total=total_record,
                                                   description="Inserting record into row")
                    return json

    else:
        json = {'main_data': False, 'extension': extension}
        return json
