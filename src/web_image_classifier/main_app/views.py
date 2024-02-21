from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse
from .tf_models.models_info import CIFAR_10_LIST, cifar_10_model
from .forms import UploadForm
from .utils import UploadProcessing, ImageClassification


upload = UploadProcessing()


def upload_image(request):
    form = UploadForm(request.POST or None, request.FILES or None)
    if (
        request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"
    ) and form.is_valid():
        try:
            upload.image = request.FILES["image"]
        except HttpResponseBadRequest as error:
            return error
    return form


def main(request):
    upload_form = upload_image(request)
    context = {"upload_form": upload_form, "classes": CIFAR_10_LIST}

    return render(request, "main_app/main.html", context)


def information(request):
    upload_form = upload_image(request)
    context = {"upload_form": upload_form}

    return render(request, "main_app/information.html", context)


def results(request):
    if request.GET:
        try:
            image_classification = ImageClassification(cifar_10_model, upload.image)
            classification_results = image_classification.get_results()
            return JsonResponse(classification_results)
        except HttpResponseBadRequest as error:
            return error
