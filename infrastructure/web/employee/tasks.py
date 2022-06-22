from celery import shared_task
from services.employee_services import EmployeeServices


@shared_task
def upload(image, empUID):
    EmployeeServices.upload_image(image)

    employee = EmployeeServices.get_employee_by_uuid(empUID)
    employee.image = image
    employee.save()
    return 'success'
