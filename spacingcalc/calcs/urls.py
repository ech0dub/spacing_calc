from django.conf.urls import url

from . import views

app_name = 'calcs'
urlpatterns = [
    # ex: /calcs/
    url(r'^$', views.create_layout, name='create_layout'),
    # ex: /calcs/5/
    url(r'^(?P<layout_id>[0-9]+)/$', views.edit_layout, name='edit_layout'),
    # ex: /calcs/5/results/
    url(r'^(?P<layout_id>[0-9]+)/results/$', views.display_results, name='display_results'),
    # ex: /calcs/5/save/
    url(r'^(?P<layout_id>[0-9]+)/save/$', views.save_layout, name='save_layout'),
]
