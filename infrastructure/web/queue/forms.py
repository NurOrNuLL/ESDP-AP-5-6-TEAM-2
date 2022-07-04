from django import forms
from models.queue.models import Queue


class QueueForm(forms.ModelForm):
    class Meta:
        model = Queue
        exclude = ['status', 'trade_point']
