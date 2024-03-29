from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.decorators import require_api_calls_remaining

from neighborhood.models import Neighborhood

from datetime import  datetime

from pull.models import Pull

from gsv import settings

import samplingstrategies as ss

STRATEGIES = {'Uniform Random Sample':ss.RandomBuildings}

@login_required
@require_api_calls_remaining
def neighborhood_index(request):
    neighborhood_list = Neighborhood.objects.filter(author=request.user.id)
    context = {
        'neighborhood_list': neighborhood_list,
        'strategies': STRATEGIES,
    }

    return render(request, 'sample/sampling_index.html', context)

@login_required
@require_api_calls_remaining
def strategy_index(request, neighborhood_id):
    context = {
        'neighborhood_id': neighborhood_id,
        'strategies': STRATEGIES.keys(),
    }

    return render(request, 'sample/strategy_index.html', context)

@login_required
@require_api_calls_remaining
def sample_points(request, neighborhood_id, strategy_name):

    n = get_object_or_404(Neighborhood, pk=neighborhood_id)
    context = {
        'title':'Neighborhood Sampler',
        'neighborhood': n,
        'MAPS_API_KEY': settings.MAPS_API_KEY,
        'sample': []
    }

    if request.method == "POST":
        pull = Pull(date=datetime.now().date(), author=request.user, neighborhood_id=n)
        pull.save()
        message_q = []

        strategy = STRATEGIES[strategy_name]()
        ss_config = strategy.configure(request, pull, n, context['sample'], message_q)
        strategy.sample(ss_config)

        for msg_type, message in ss_config['message_q']:
            messages.add_message(request, msg_type, message)

        return redirect('sample_success', neighborhood_id, strategy_name, str(context['sample']).replace("'", '"'))

    return render(request, 'sample/sample.html', context)

@login_required
def sample_success(request, neighborhood_id, strategy_name, sample):
    n = get_object_or_404(Neighborhood, pk=neighborhood_id)
    image_data = messages.get_messages(request)

    for message in image_data:
        print("Sent_message:", message)

    context = {
        'title':'Neighborhood Sample Success Page',
        'neighborhood': n,
        'strategy': strategy_name,
        'MAPS_API_KEY': settings.MAPS_API_KEY,
        'sample': sample,
        # 'message_to_url': message_to_url
        'no_info_messages': True
    }
    return render(request, "sample/sample_success.html", context)
