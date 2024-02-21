from django.forms import Form, FileField, FileInput


class UploadForm(Form):
    image = FileField(
        widget=FileInput(
            attrs={
                "class": "form-control form-control-lg"
            }
        )
    )
