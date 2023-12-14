from .models import LinkedList
from django.shortcuts import render, redirect
from django.shortcuts import render

# Create your views here.


def display_linked_list(request):
    nodes = []

    linked_list = LinkedList.objects.first()
    if linked_list is None:
        linked_list = LinkedList()
        linked_list.save()
    else:
        # nodes = linked_list.display_from_tail()
        nodes = linked_list.display_from_head()

    return render(request, 'display_linked_list.html', {'nodes': nodes})


def add_node_to_head(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        music_file = request.FILES.get('music_file')
        author = request.POST.get('author')

        linked_list = LinkedList.objects.first()
        if linked_list is None:
            linked_list = LinkedList()
            linked_list.save()
        else:
            linked_list.add_node_to_head(title, music_file, author)

    return redirect('display_linked_list')


def add_node_to_tail(request):
    if request.method == 'POST':
        title = request.POST.get('title_b')
        music_file = request.FILES.get('music_file_b')
        author = request.POST.get('author_b')
        print("tail title " + title)

        linked_list = LinkedList.objects.first()
        if linked_list is None:
            linked_list = LinkedList()
            linked_list.save()
        else:
            linked_list.add_node_to_tail(title, music_file, author)

    return redirect('display_linked_list')


def delete_head(self):
    linked_list = LinkedList.objects.first()

    if linked_list is None:
        linked_list = LinkedList()
        linked_list.save()

    linked_list.delete_head()

    return redirect("display_linked_list")


def delete_tail(self):
    linked_list = LinkedList.objects.first()

    if linked_list is None:
        linked_list = LinkedList()
        linked_list.save()

    linked_list.delete_tail()

    return redirect("display_linked_list")


def search_node(request):
    if (request.method == "POST"):
        search_item = request.POST.get("search_parameter")

        linked_list = LinkedList.objects.first()
        if linked_list is None:
            linked_list = LinkedList()
            linked_list.save()
        search_result = linked_list.search_node(search_item)

    return render(request, "search_result.html", {"search_result": search_result})
