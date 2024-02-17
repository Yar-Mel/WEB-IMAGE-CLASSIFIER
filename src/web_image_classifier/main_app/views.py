from pathlib import Path
from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse
from .tf_models import CIFAR_10_model
from .forms import UploadForm, ModelChoiceForm
from .utils import UploadProcessing, ImageClassification

import csv

upload = UploadProcessing()


class TestClass:
    image = None


test_class = TestClass()


def model_choice(request):
    form = ModelChoiceForm()
    if request.GET:
        temp = request.GET['choices_field']
        print(temp)
    return form


def upload_image(request):
    form = UploadForm(request.POST or None, request.FILES or None)
    if (request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest') and form.is_valid():
        try:
            test_class.image = request.FILES['image']
        except HttpResponseBadRequest as e:
            return e
    return form


def main(request):
    upload_form = upload_image(request)
    model_choice_form = ModelChoiceForm()
    context = {'upload_form': upload_form, 'model_choice_form': model_choice_form}

    return render(request, "main_app/main.html", context)


def information(request):
    form = upload_image(request)
    context = {'form': form}

    txt_folder = Path('src/web_image_classifier/main_app/static/main_app/txt')
    img_folder = Path('src/web_image_classifier/main_app/static/main_app/img')

    with open(txt_folder/'model_10_summary.txt') as f:
        model_10 = [line.rstrip() for line in f]
        context['model_10_info'] = model_10

    with open(txt_folder/'model_10_summary.txt') as f:
        model_100 = [line.rstrip() for line in f]
        context['model_100_info'] = model_100

    return render(request, "main_app/information.html", context)


# def statistic(request):
#     form = upload_image(request)
#     context = {'form': form}
#
#     return render(request, "main_app/statistic.html", context)


def results(request):

    if request.GET:
        print(request.GET)
        temp = request.GET['choices_field']
        print(temp)

    print('start classification')
    image_classification = ImageClassification(CIFAR_10_model, test_class.image)
    print(image_classification())
    return JsonResponse(image_classification())
