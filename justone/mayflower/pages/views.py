# Create your views here.
from django.http import Http404
from django.shortcuts import render
from pages.models import Page


def show_page(request, page_code):
    """

    """
    try:
        return render(request, 'pages/page.html', {'page': Page.objects.get(code=page_code)})
    except Page.DoesNotExist:
        raise Http404()