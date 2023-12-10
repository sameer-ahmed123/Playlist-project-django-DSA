from django.contrib import admin
from App.models import  LinkedList,Node
# Register your models here.


class NodeAdmin(admin.ModelAdmin):
    list_display = ('Title', 'next_node', 'prev_node')


admin.site.register(Node, NodeAdmin)

admin.site.register(LinkedList)