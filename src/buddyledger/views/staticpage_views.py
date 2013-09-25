from django.shortcuts import render, render_to_response

def Frontpage(request):
    response = render_to_response('frontpage.html')
    return response


def ShowUsage(request):
    response = render_to_response('usage.html')
    return response

