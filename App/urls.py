from django.urls import path
from App.views import *

urlpatterns = [
    path('', display_linked_list, name='display_linked_list'),
    path('add_head/', add_node_to_head, name='add_node_to_front'),
    path('add_tail/', add_node_to_tail, name='add_node_to_tail'),
    path("delete_head/", delete_head, name="delete_head"),
    path("delete_tail", delete_tail, name="delete_tail"),
    path("search_node/", search_node, name="search_node"),
    path("Node/<int:id>/", view_node, name="view_node"),
    path("add_to_nth", add_to_nth, name="add_to_nth"),
    path('delete_nth', delete_nth, name="delete_nth"),

    # {% url 'view_node' search_result.id %}

]
