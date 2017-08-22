from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.conf import settings

from .models import Layout

import os
import math
import matplotlib
matplotlib.use('Agg')  # need to use this to avoid matplotlib creating tk windows it doesn't need/use
import matplotlib.pyplot as plt
import numpy as np


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
        layout.outer_diameter_m = request.POST['outer_diameter_m']
        layout.cable_spacing_m = request.POST['cable_spacing_m']

    except (KeyError, Layout.DoesNotExist):
        # Redisplay the layout data input form.
        return render(request, 'calcs/layout.html',
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
    graphic_name = make_graphic(layout)

    context = {'layout': layout,
               'coords': sorted(coords.items()),
               'latest_layout_list': latest_layout_list,
               'plot_graphic': graphic_name
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
                          'x': '{:6.3f}'.format(0.0 - (cable_spacing_m / 2)),
                          'y': '{:6.3f}'.format(cable_1_y - (math.sqrt(3) / 2) * cable_spacing_m),
                          },
              'cable_2': {'name': 'Yellow',
                          'x': '{:6.3f}'.format(0.0),
                          'y': '{:6.3f}'.format(cable_1_y),
                          },
              'cable_3': {'name': 'Blue',
                          'x': '{:6.3f}'.format(0.0 + (cable_spacing_m / 2)),
                          'y': '{:6.3f}'.format(cable_1_y - (math.sqrt(3) / 2) * cable_spacing_m),
                          },
              }

    return output


def make_graphic(layout):

    def xy(r, phi, x_coord, y_coord):
        return r * np.cos(phi) + x_coord, r * np.sin(phi) + y_coord

    # print('\n layout_name: ', layout.layout_name,
    #       '\n pub_date: ', layout.pub_date,
    #       '\n depth_to_top_m: ', layout.depth_to_top_m,
    #       '\n arrangement: ', layout.arrangement,
    #       '\n cable_spacing_m: ', layout.cable_spacing_m,
    #       '\n outer_diameter_m: ', layout.outer_diameter_m,
    #       )

    these_coords = calc_coords(layout)
    r = layout.outer_diameter_m / 2
    max_depth = 0
    max_width = 0
    phis = np.arange(0, 6.28, 0.01)

    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal')

    for cable_name, cable_details in these_coords.items():
        # print(cable_name)
        # print(cable_details)
        cable_name = cable_details['name']
        cable_x = float(cable_details['x'])
        cable_y = float(cable_details['y'])
        if cable_name == 'Red':
            colour = 'r'
        elif cable_name == 'Yellow':
            colour = 'y'
        elif cable_name == 'Blue':
            colour = 'b'

        ax.plot(*xy(r, phis, cable_x, cable_y), c=colour, ls='-')

        if (cable_y - r) < max_depth:
            max_depth = (cable_y - r)

        if (abs(cable_x) + r) > max_width:
            max_width = (abs(cable_x) + r)

    max_depth = max_depth - 0.5
    max_width = max_width + 0.5

    ax.set_autoscaley_on(False)
    ax.set_ylim([max_depth, 0.2])
    ax.set_autoscalex_on(False)
    ax.set_xlim([-max_width, max_width])

    plt.axhline(y=0.0, color='g', linestyle='-')

    # need to debug to get this working without hard-coded path to this_plot.svg
    plot_name = os.path.join(settings.MEDIA_ROOT, 'this_plot.svg')
    fig.savefig(filename=plot_name, format='svg')
    # plt.show()
    return plot_name
