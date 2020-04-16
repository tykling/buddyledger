from .misc import render_to_response

def Frontpage(request):
    response = render_to_response(request, 'frontpage.html')
    return response


def ShowUsage(request):
    response = render_to_response(request, 'usage.html')
    return response

