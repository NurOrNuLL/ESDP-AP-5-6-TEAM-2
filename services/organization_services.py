from models.organization.models import Organization


class OrganizationService:
    @staticmethod
    def get_organization_by_id(kwargs: dict) -> Organization:
        return Organization.objects.get(id=kwargs['orgID'])
