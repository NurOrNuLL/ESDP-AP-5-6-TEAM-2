from django.http import HttpRequest

class ResetOrderCreateFormDataMixin:
    def delete_order_data_from_session(self, request:HttpRequest) -> None:
        if request.session.get('contractor') : del request.session['contractor']
        if request.session.get('own') : del request.session['own']

        if request.session.get('jobs') : del request.session['jobs']

        if request.session.get('note') : del request.session['note']
        if request.session.get('mileage') : del request.session['mileage']
