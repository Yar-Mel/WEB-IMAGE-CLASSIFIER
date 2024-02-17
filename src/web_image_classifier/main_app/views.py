from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse
from .tf_models import CIFAR_10_LIST, CIFAR_10_model
from .forms import UploadForm
from .utils import UploadProcessing, Classification

upload = UploadProcessing()


def upload_image(request):
    form = UploadForm(request.POST or None, request.FILES or None)
    if (request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest') and form.is_valid():
        try:
            upload.image = request.FILES['image']
        except HttpResponseBadRequest as e:
            return e
    return form


def main(request):
    form = upload_image(request)
    context = {'classes': CIFAR_10_LIST, 'form': form}
    return render(request, "main_app/main.html", context)


def information(request):
    form = upload_image(request)

    context = {'form': form}
    return render(request, "main_app/information.html", context)


def statistic(request):
    form = upload_image(request)

    accuracy = 0.31     # TODO
    context = {"accuracy": accuracy, 'form': form}
    return render(request, "main_app/statistic.html", context)


def results(request):
    print('start classification')
    if upload.image:
        classification = Classification(CIFAR_10_model, upload.image)
        predictions = classification()
        return JsonResponse(predictions)
    else:
        return HttpResponseBadRequest("Файл изображения не был загружен или не удалось обработать.")
