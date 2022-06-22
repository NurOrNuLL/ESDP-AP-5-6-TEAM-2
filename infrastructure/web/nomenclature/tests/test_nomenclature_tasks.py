import json
from unittest import TestCase
from unittest.mock import Mock, patch
from ..tasks.import_exel import import_exel_file
from ..tasks.export_exel import export_exel_file
from models.nomenclature.models import Nomenclature
from core import celery_app


class TestExportImportCelery(TestCase):
    def setUp(self):
        celery_app.conf.update(CELERY_ALWAYS_EAGER=True)

    def test_export_exel(self):
        nomenclatures = [Mock(spec=Nomenclature, id=1, services=[{'Цена': 4000,'Марка': 'Газель','Название': 'Компьютерная диагностика двигателя ','Категория': 'Диагностика','Примечание': '406,405,409 ЕВРО 2,405,409,4216 - ЕВРО 3,4'}]), Mock(spec=Nomenclature, id=2)]

        with patch('celery_progress.backend.ProgressRecorder.set_progress') as set_progress:
            set_progress.return_value = None

            with patch('django.core.cache.cache.get') as get_cache:
                get_cache.return_value = None

                with patch('services.nomenclature_services.NomenclatureService.get_all_nomenclatures') as get_nomenclatures:
                    get_nomenclatures.return_value = nomenclatures

                    with patch('django.core.cache.cache.set') as set_cache:
                        set_cache.return_value = None

                        results = export_exel_file(nomenclatures[0].id, 'xls')

                        self.assertDictEqual(results, {
                            'main_data': nomenclatures[0].services,
                            'extension': 'xls',
                            'nomenclature_pk': nomenclatures[0].id
                        })
                        get_cache.assert_called_once_with('nomenclatures')
                        get_nomenclatures.assert_called_once()
                        set_cache.assert_called_once_with('nomenclatures', nomenclatures, 60 * 1440)

    def test_import_excel(self):
        nomenclature = Mock(spec=Nomenclature, id=1, services=[])

        with patch('celery_progress.backend.ProgressRecorder.set_progress') as set_progress:
            set_progress.return_value = None

            with patch('django.core.cache.cache.delete') as delete_cache:
                delete_cache.return_value = None

                with patch('models.nomenclature.models.Nomenclature.objects.get') as get_nomenclature:
                    get_nomenclature.return_value = nomenclature

                    with patch('models.nomenclature.models.Nomenclature.save') as save_nomenclature:
                        save_nomenclature.return_value = None

                        data = [
                            {
                                'Цена': 4000,
                                'Марка': 'Газель',
                                'Название': 'Компьютерная диагностика двигателя ',
                                'Категория': 'Диагностика',
                                'Примечание': '406,405,409 ЕВРО 2,405,409,4216 - ЕВРО 3,4'
                            }
                        ]

                        result = import_exel_file(json.dumps(data), nomenclature.id)

                        nomenclature.services = data

                        self.assertEqual(result, {"detail": "Successfully import exel file"})
                        self.assertListEqual(nomenclature.services, data)
                        delete_cache.assert_called_once_with('nomenclatures')
                        get_nomenclature.assert_called_once_with(id=nomenclature.id)