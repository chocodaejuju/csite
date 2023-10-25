from map.models import MarkerPosition
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotAllowed
from django.utils import timezone
from .forms import MarkerPositionForm
from .models import MarkerPosition

# Create your views here.
def index(request):
    marker_list = MarkerPosition.objects.order_by('-create_date')
    context = {'marker_list': marker_list}
    return render(request, 'map/map.html', context)


def marker_create(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    lat = request.POST.get('lat')
    lng = request.POST.get('lng')
    if request.method == "POST":
        form = MarkerPositionForm(request.POST)
        marker = MarkerPosition(title = title,create_date = timezone.now(), content = content, lat = lat, lng=lng)
        marker.save()
        return redirect('map:index')
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    return redirect('map:index')


def marker_modify(request):
    id = request.POST.get('markerIdL')
    title = request.POST.get('rtitle')
    content = request.POST.get('rcontent')
    marker = get_object_or_404(MarkerPosition, pk=id)
    if request.method == "POST":
        marker.title = title
        marker.content = content
        marker.save()
        return redirect('map:index')
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    return redirect('map:index')


def marker_delete(request):
    print("어이")
    id = request.POST.get('markerIdI')
    print(id)
    marker = get_object_or_404(MarkerPosition, pk=id)
    if request.method == "POST":
        marker.delete()
    return redirect('map:index')