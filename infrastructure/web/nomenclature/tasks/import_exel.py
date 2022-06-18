from celery_progress.backend import ProgressRecorder
from core import celery_app
from .base import BaseTask
from services.nomenclature_services import NomenclatureService
from django.core.cache import cache
from django.http.response import JsonResponse


class ImportExcelTask(BaseTask):
    name = "ImportExcelTask"

    def run(self, file: str, nom_id: int) -> JsonResponse:
        cache.delete('nomenclatures')
        progress_recorder = ProgressRecorder(self)
        for k, file_item in enumerate(file):
            progress_recorder.set_progress(k + 1, total=len(file),
                                           description="Inserting record into row")
        NomenclatureService.import_services(file, nom_id)
        return {
            "detail": "Successfully import exel file"
        }


@celery_app.task(bind=True, base=ImportExcelTask)
def import_exel_file(self, *args, **kwargs):
    return super(type(self), self).run(*args, **kwargs)
