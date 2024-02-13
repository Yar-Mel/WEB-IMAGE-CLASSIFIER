from django.shortcuts import render
from .model_data import CLASSES_LIST


def main(request):
    context = {"classes": CLASSES_LIST}
    return render(request, "main_app/main.html", context)
