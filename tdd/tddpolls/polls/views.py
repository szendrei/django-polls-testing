from django.http import HttpResponse
from django.shortcuts import render

def main_page(request):
    return HttpResponse('<html><title>TDD Polls</title></html>')
