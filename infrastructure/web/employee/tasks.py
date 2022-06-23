import base64, io
import os
from celery import shared_task
from services.employee_services import EmployeeServices


@shared_task
def upload(encoded_image, empUID):
    decoded_image = io.BytesIO(base64.b64decode(encoded_image))

    EmployeeServices.upload_image(decoded_image, empUID)

    employee = EmployeeServices.get_employee_by_uuid(empUID)
    employee.image = f"https://s3.amazonaws.com/{os.environ.get('AWS_BUCKET_NAME')}/employee_image_{empUID}.png",
    employee.save()

    return 'success'
