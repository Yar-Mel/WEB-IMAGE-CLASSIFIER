from django.shortcuts import render
from .model_data import CLASSES_LIST
from .forms import UploadForm
from django.http import JsonResponse


def upload_image(request):
    form = UploadForm(request.POST or None, request.FILES or None)
    if (request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest') and form.is_valid():
        form.save()
    return form


def main(request):
    form = upload_image(request)

    context = {'classes': CLASSES_LIST, 'form': form}
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

    form = upload_image(request)

    results = {
        'class_1': '97%',
        'class_2': '87%',
        'class_3': '77%',
    }  # TODO

    context = {"results": results, 'form': form}
    return render(request, "main_app/results.html", context)
