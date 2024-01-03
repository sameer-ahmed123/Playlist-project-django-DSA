from .models import LinkedList, Node
from django.shortcuts import get_object_or_404, render, redirect
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


def search_node(request):
    if (request.method == "POST"):
        search_item = request.POST.get("search_parameter")

        linked_list = LinkedList.objects.first()
        if linked_list is None:
            linked_list = LinkedList()
            linked_list.save()
        search_result = linked_list.search_node(search_item)

    return render(request, "search_result.html", {"search_result": search_result})


def view_node(request, id):
    node = get_object_or_404(Node, id=id)

    context = {
        "node": node
    }
    return render(request, "node_detail.html", context)


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


def add_to_nth(request):
    if request.method == "POST":
        Title = request.POST.get("nth_title")
        Music_file = request.FILES.get("nth_music_file")
        Author = request.POST.get("nth_author")
        position = int(request.POST.get("nth_pos"))

        linked_list = LinkedList.objects.first()
        if linked_list is None:
            linked_list = LinkedList()
            linked_list.save()

        linked_list.add_to_nth(Title, Music_file, Author, position)

    return redirect("display_linked_list")


def delete_head(request):
    linked_list = LinkedList.objects.first()

    if linked_list is None:
        linked_list = LinkedList()
        linked_list.save()

    linked_list.delete_head()

    return redirect("display_linked_list")


def delete_tail(request):
    linked_list = LinkedList.objects.first()

    if linked_list is None:
        linked_list = LinkedList()
        linked_list.save()

    linked_list.delete_tail()

    return redirect("display_linked_list")


def delete_nth(request):
    if (request.method == "POST"):
        position = int(request.POST.get("delete_nth_pos"))
        # print("delete postiotion is :" + str(position))

        linkedlist = LinkedList.objects.first()
        if linkedlist is None:
            linkedlist = LinkedList()
            linkedlist.save()

        linkedlist.delete_nth(position)

    return redirect("display_linked_list")
