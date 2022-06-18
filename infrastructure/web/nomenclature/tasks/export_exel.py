from time import sleep

from celery_progress.backend import ProgressRecorder
from core import celery_app
from .base import BaseTask
from services.nomenclature_services import NomenclatureService
from django.core.cache import cache
from django.http.response import JsonResponse


class ExportExcelTask(BaseTask):
    name = "ExportExcelTask"

    def run(
            self, nomenclature_pk: int, extension: str
    ) -> JsonResponse:  # noqa C901
        nomenclatures = cache.get('nomenclatures')
        if not nomenclatures:
            nomenclatures = NomenclatureService.get_all_nomenclatures()
            cache.set('nomenclatures', nomenclatures, 60 * 1440)
        if nomenclatures:
            for i, nomenclature in enumerate(list(nomenclatures)):
                if int(nomenclature_pk) == nomenclature.id:
                    progress_recorder = ProgressRecorder(self)
                    if nomenclature.services:
                        total_record = len(nomenclature.services)
                        for k, services in enumerate(nomenclature.services):
                            sleep(0.08)
                            progress_recorder.set_progress(k + 1, total=total_record,
                                                           description="Inserting record into row")  # noqa E501
                        json = {'main_data': nomenclature.services, 'extension': extension,
                                'nomenclature_pk': nomenclature_pk}
                        return json
                    else:
                        json = {'main_data': False, 'extension': extension}
                        return json

        else:
            json = {'main_data': False, 'extension': extension}
            return json


@celery_app.task(bind=True, base=ExportExcelTask)
def export_exel_file(self, *args, **kwargs):
    return super(type(self), self).run(*args, **kwargs)
