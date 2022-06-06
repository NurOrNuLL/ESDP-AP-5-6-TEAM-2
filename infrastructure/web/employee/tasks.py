from celery import shared_task
from services.employee_services import EmployeeServices


@shared_task
def upload(local_path, path):
    EmployeeServices.upload_image(local_path, path)
    return 'success'
