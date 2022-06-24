import base64, io
import os
from celery import shared_task
from services.employee_services import EmployeeServices


@shared_task
def upload(encoded_image, empIIN):
    decoded_image = io.BytesIO(base64.b64decode(encoded_image))

    EmployeeServices.upload_image(decoded_image, empIIN)

    employee = EmployeeServices.get_employee_by_iin(empIIN)
    employee.image = f"https://s3.amazonaws.com/{os.environ.get('AWS_BUCKET_NAME')}/employee_image_{empIIN}.png",
    employee.save()
    return 'success'