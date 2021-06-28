from django.shortcuts import render

# Create your views here.

class Save_Request:
    def __init__(self, request):
        html_data = request.GET
        self.api_key = str(html_data['api_key'])
        self.address = str(html_data["address"])

def address(request):
    return render(request, 'address/address.html', {'title':'Address Finder'})

def response(request):

    # Gets all the specified values in the html form
    download_information = Save_Request(request)

    return render(request, 'address/response.html',
     {'title':'Download Images',
      'api_key': download_information.api_key,
      'address': download_information.address})
