from pathlib import Path
from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse
from .tf_models.models_info import CIFAR_10_LIST, cifar_10_model
from .forms import UploadForm
from .utils import UploadProcessing, ImageClassification


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
    upload_form = upload_image(request)
    context = {'upload_form': upload_form, 'classes': CIFAR_10_LIST}

    return render(request, "main_app/main.html", context)


def information(request):
    form = upload_image(request)
    context = {'form': form}

    txt_folder = Path('src/web_image_classifier/main_app/static/main_app/txt')

    with open(txt_folder/'model_10_summary.txt') as f:
        model_10 = [line.rstrip() for line in f]
        context['model_10_info'] = model_10

    return render(request, "main_app/information.html", context)


# def statistic(request):
#     form = upload_image(request)
#     context = {'form': form}
#
#     return render(request, "main_app/statistic.html", context)


def results(request):
    if request.GET:
        print('Start Classification')
        image_classification = ImageClassification(cifar_10_model, upload.image)
        classification_results = image_classification.get_results()
        print(classification_results)
        return JsonResponse(classification_results)
