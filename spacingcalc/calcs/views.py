from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import Layout

import math


def create_layout(request):
    new_layout = Layout(pub_date=timezone.now())
    new_layout.save()
    return HttpResponseRedirect(reverse('calcs:edit_layout', args=(new_layout.id,)))


def edit_layout(request, layout_id):
    layout = get_object_or_404(Layout, pk=layout_id)
    latest_layout_list = Layout.objects.order_by('-pub_date')
    context = {'layout': layout,
               'latest_layout_list': latest_layout_list,
               }
    return render(request, 'calcs/layout.html', context)


def save_layout(request, layout_id):
    layout = get_object_or_404(Layout, pk=layout_id)
    try:
        layout.layout_name = request.POST['layout_name']
        layout.depth_to_top_m = request.POST['depth_to_top_m']
        layout.arrangement = request.POST['arrangement']
        layout.cable_spacing_m = request.POST['cable_spacing_m']
        layout.outer_diameter_m = request.POST['outer_diameter_m']

    except (KeyError, Layout.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'calcs/edit_layout.html',
                      {'layout': layout,
                       'error_message': "You didn't complete all layout options.",
                       })
    else:
        layout.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('calcs:display_results', args=(layout.id,)))


def display_results(request, layout_id):
    layout = get_object_or_404(Layout, pk=layout_id)
    latest_layout_list = Layout.objects.order_by('-pub_date')

    coords = calc_coords(layout)

    context = {'layout': layout,
               'coords': sorted(coords.items()),
               'latest_layout_list': latest_layout_list,
               }

    return render(request, 'calcs/results.html', context)


def calc_coords(layout):

    if layout.arrangement == 'spaced trefoil':
        cable_spacing_m = layout.cable_spacing_m
    elif layout.arrangement == 'touching trefoil':
        cable_spacing_m = layout.outer_diameter_m
    else:
        raise ValueError('Error: Arrangement specified as {}./n'
                         'This arrangement is not supported.'.format(str(layout.arrangement)))

    cable_1_y = -1 * (layout.depth_to_top_m + (layout.outer_diameter_m / 2))

    output = {'cable_1': {'name': 'Red',
                          'x': '{:6.3f}m'.format(0.0 - (cable_spacing_m / 2)),
                          'y': '{:6.3f}m'.format(cable_1_y - (math.sqrt(3) / 2) * cable_spacing_m),
                          },
              'cable_2': {'name': 'Yellow',
                          'x': '{:6.3f}m'.format(0.0),
                          'y': '{:6.3f}m'.format(cable_1_y),
                          },
              'cable_3': {'name': 'Blue',
                          'x': '{:6.3f}m'.format(0.0 + (cable_spacing_m / 2)),
                          'y': '{:6.3f}m'.format(cable_1_y - (math.sqrt(3) / 2) * cable_spacing_m),
                          },
              }

    return output
