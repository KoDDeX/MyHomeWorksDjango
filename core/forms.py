from django import forms
from .models import Review, Master, Order

class ReviewForm(forms.ModelForm):

    master = forms.ModelChoiceField(queryset = Master.objects.all())

    class Meta:
        model = Review
        fields = ['client_name', 'text', 'rating', 'master', 'photo']

class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем класс form-control к каждому полю формы
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})


    class Meta:
        model = Order
        fields = [
            "client_name",
            "phone",
            "comment",
            "master",
            "services",
            "appointment_date",
        ]
