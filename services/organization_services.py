<<<<<<< HEAD
from models.organization.models import Organization


class OrganizationService:
    @staticmethod
    def get_organization_by_id(kwargs: dict) -> Organization:
        return Organization.objects.get(id=kwargs['orgID'])
=======
from models.organization.models import Organization


class OrganizationService:
    @staticmethod
    def get_organization_by_id(kwargs: dict) -> Organization:
        return Organization.objects.get(id=kwargs['orgID'])
>>>>>>> 2d2f703ec0e0e74897d9ec3e4aacdff666715879
