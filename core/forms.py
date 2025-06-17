from django import forms
from .models import Review, Master, Order
from .models import Service


class ReviewForm(forms.ModelForm):

    master = forms.ModelChoiceField(queryset=Master.objects.all())

    class Meta:
        model = Review
        exclude = ["is_published"]


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


class ServiceForm(forms.ModelForm):
    # Расширим инициализатор для добавления form-control к полям формы

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем класс form-control к каждому полю формы (кроме чекбоксов)
        for field_name, field in self.fields.items():
            if field_name != "is_popular":  # Пропускаем чекбокс
                field.widget.attrs.update({"class": "form-control"})
            else:  # Для чекбокса добавляем класс переключателя
                field.widget.attrs.update({"class": "form-check-input"})

    # Валидатор deля поля description
    def clean_description(self):
        description = self.cleaned_data.get("description")
        if len(description) < 10:
            raise ValidationError("Описание должно содержать не менее 10 символов.")
        return description

    class Meta:
        model = Service
        # # Поля, которые будут отображаться в форме
        fields = ["name", "description", "price", "duration", "is_popular", "image"]


class ServiceEasyForm(ServiceForm):
    class Meta:
        model = Service
        fields = ["name", "description", "price"]