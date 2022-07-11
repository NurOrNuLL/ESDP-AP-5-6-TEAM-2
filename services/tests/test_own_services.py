from unittest import TestCase
from unittest.mock import Mock, patch
from models.contractor.models import Contractor
from models.own.models import Own
from services.own_services import OwnServices


class OwnServicesTest(TestCase):
    def test_get_own_by_id(self):
        own = Mock(spec=Own, id=1)

        with patch('models.own.models.Own.objects.get') as get_own:
            get_own.return_value = own
            returned_own = OwnServices.get_own_by_id(own.id)

            self.assertEqual(returned_own, own)
            get_own.assert_called_once_with(id=own.id)

    def test_create_own(self):
        contractor = Mock(spec=Contractor, id=1)
        queryset = [Mock(spec=Own)]
        data = {
            'name': 'Gaz',
            'number': 'HHH777J',
            'comment': 'some comment',
            'is_part': 'False'
        }
        with patch('models.own.models.Own.objects.create') as create_own:
            with patch(
                    'models.contractor.models.Contractor.objects.get'
            ) as get_contractor:
                create_own.return_value = Mock(
                    spec=Own,
                    name=data['name'],
                    number=data['number'],
                    comment=data['comment'],
                    is_part=data['is_part']
                )

                get_contractor.return_value = contractor

                own = OwnServices.create_own(data, contractor_id=contractor.id)
                queryset.append(own)

                self.assertIn(own, queryset)
                create_own.assert_called_once_with(
                    name=data['name'],
                    number=data['number'],
                    comment=data['comment'],
                    is_part=data['is_part'],
                    contractor=contractor
                )

    def test_delete_own(self):
        own = Mock(spec=Own, id=1)
        queryset = [own]

        with patch('models.own.models.Own.delete'):
            with patch('models.own.models.Own.objects.get') as get_own:
                get_own.return_value = own
                OwnServices.delete_own(own.id)
                queryset.pop(queryset.index(own))

                self.assertNotIn(own, queryset)
                get_own.assert_called_once_with(id=own.id)
