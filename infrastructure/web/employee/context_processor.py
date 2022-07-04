import ast

from services.employee_services import EmployeeServices


def request_user_employee(request):
    try:
        if not request.user.is_staff:
            return {
                'request_user_employee': EmployeeServices.get_employee_by_uuid(request.user.uuid)
            }
        else:
            return {
                'request_user_employee': ''
            }
    except AttributeError:
        return {
            'request_user_employee': ''
        }


def trade_point_id(request):
    return {
        'tradepoint_id': ast.literal_eval(str(request.COOKIES.get('tradepointID')))
    }
