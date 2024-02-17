from django.forms import Form, FileField, ChoiceField, RadioSelect


class UploadForm(Form):
    image = FileField()


class ModelChoiceForm(Form):
    CHOICES = [
        ('1', 'Model 10'),
        ('2', 'Model 100'),
    ]
    choices_field = ChoiceField(choices=CHOICES)
