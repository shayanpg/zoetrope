from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.decorators import require_api_calls_remaining

from utils import create_presigned_url, create_s3_client

from neighborhood.models import Neighborhood
from address.models import Address
from pull.models import Pull
from image.models import Image

@login_required
def history(request):
    pull_list = Pull.objects.filter(author=request.user.id).order_by('-date')
    context = {
        'pull_list': pull_list,
    }

    return render(request, 'pull/history.html', context)

@login_required
@require_api_calls_remaining
def get_pull(request, pull_id):
    s3 = create_s3_client()
    pull = get_object_or_404(Pull, pk=pull_id)
    images = Image.objects.filter(pull_id=pull)
    for image in images:
        message = image.address_id.name +" in "+ str(image.year)
        messages.add_message(request, messages.INFO, message)
        url = create_presigned_url(s3, image.file_path)
        messages.add_message(request, messages.INFO, url)
    context = {
        'title':'View History',
        'p': pull,
        'no_info_messages': True
    }
    return render(request, "pull/history_success.html", context)
