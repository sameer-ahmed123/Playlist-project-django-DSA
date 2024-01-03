import os
from django.db import models


class Node(models.Model):
    Title = models.CharField(max_length=350)
    Music_file = models.FileField(upload_to="Audio_files", null=True)
    Author = models.CharField(max_length=250, null=True, blank=True)
    next_node = models.OneToOneField(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='prev_node_of')
    prev_node = models.OneToOneField(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name="next_node_of", unique=False)

    # prev_node and next_node are the reference to the next and previous node in the linked list
    # both are referncing 'self' which means
    # next has a datatype of its self i.e next_node's datatype is Node

    def delete(self, *args, **kwargs):
        if self.Music_file:
            path = self.Music_file.path
            os.remove(path)
            # to remove the music file from the device

        super(Node, self).delete(*args, **kwargs)

    def __str__(self):
        return f"{self.Title}"


class LinkedList(models.Model):

    head = models.ForeignKey(Node, null=True, blank=True,
                             on_delete=models.SET_NULL, related_name="head_node")
    tail = models.ForeignKey(Node, null=True, blank=True,
                             on_delete=models.SET_NULL, related_name="tail_node")

    def is_empty(self):
        return self.head is None

    def display_from_head(self):
        nodes = []

        if self.head:
            current_node = self.head
            while current_node:
                nodes.append(current_node)
                current_node = current_node.next_node
        return nodes

    def display_from_tail(self):
        nodes = []

        if self.tail:
            current_node = self.tail
            while current_node:
                nodes.append(current_node)
                current_node = current_node.prev_node
        return nodes

    def add_node_to_head(self, Title, Music_file, Author):
        new_node = Node(Title=Title, Music_file=Music_file, Author=Author,)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
            new_node.save()
            self.head.save()
        else:
            new_node.next_node = self.head
            self.head.prev_node = new_node
            new_node.save()  # saves the new node in database
            self.head.save()  # saves the head_node changes
            self.head = new_node  # assigns the new_node as the NEW head_node

        self.save()  # saves the changes made to the "LINKED LIST"

    def add_node_to_tail(self, Title, Music_file, Author):
        new_node = Node(Title=Title, Music_file=Music_file, Author=Author)
        if (self.is_empty()):
            self.head = new_node
            self.tail = new_node
            new_node.save()
            self.head.save()

        else:
            # assign the next of current tail to the  "new_node"
            self.tail.next_node = new_node
            # assign the previous node of "new_node" to the current tail
            new_node.prev_node = self.tail
            new_node.save()
            self.tail.save()
            self.tail = new_node  # move the "Tail" to the newly added node

        self.save()

    def delete_head(self):
        if (self.is_empty()):
            print("the doubly linked list is empty ")
        else:
            nxNode = self.head.next_node  # nxNode is the node that comes after the current head
            if nxNode:
                nxNode.prev_node.delete()  # delete the node that was before the nxNode (current head)
                nxNode.prev_node = None
                self.head = nxNode      # set the new head as nxNode
                self.head.save()  # save changed head to the database
                self.save()  # save linked list only if multiple nodes are present in the linked list

            else:
                self.head.delete()
                self = None
                # set the linked list  itself to none without saving when only one item is in the list
                # saving while deleting the last item was causing foreign key constraint issues

    def delete_tail(self):
        if self.is_empty():
            print("the node list is empty")
        else:
            previous_node = self.tail.prev_node

            if previous_node:
                previous_node.next_node.delete()
                previous_node.next_node = None
                self.tail = previous_node
                self.tail.save()
                self.save()
            else:
                self.tail.delete()
                self = None    # same logic as delete head  but in reverse / from the tail

    def search_node(self, search_target):
        # search function . same as display function but with condition
        if self.head:
            current_node = self.head
            while current_node:
                if (current_node.Title == search_target):
                    return current_node
                current_node = current_node.next_node

    def add_to_nth(self, Title, Music_file, Author, position):
        new_node = Node(Title=Title, Music_file=Music_file, Author=Author)

        if self.is_empty():
            self.head = new_node
            self.tail = new_node
            new_node.save()
            self.save()
            return

        if position == 1:
            self.add_node_to_head(Title, Music_file, Author)
            return

        current_position = 1
        current_node = self.head
        # find the current node and then add the new node accoding to current node
        while current_node and (current_position < position - 1):
            current_node = current_node.next_node
            current_position += 1

        # agar position list size se greater hai toh add to tail
        if (position-1 > current_position):
            self.add_node_to_tail(Title, Music_file, Author)
            return

        #  agar current node khud tail hai toh ==> add to tail new_node
        if current_node.next_node is None:
            self.add_node_to_tail(Title, Music_file, Author)
            return

        # Check if adding new_node would violate the unique constraint
        if current_node.next_node and current_node.next_node.prev_node == current_node:
            # Handle the conflict by updating existing nodes
            curents_nextNode = current_node.next_node
            # new node database me exist kare ga toh changes apply ho gi....
            new_node.save()

            curents_nextNode.prev_node = new_node
            new_node.next_node = curents_nextNode
            curents_nextNode.save()  # this node comes after the new_node

            current_node.next_node = new_node
            current_node.save()  # save current node after applying changes
            # / yeh node new_node se pehle aata

            new_node.prev_node = current_node
            new_node.save()  # at this time next of current node is the "NEW_NODE"
            current_node.save()

        new_node.save()
        self.save()

    def delete_nth(self, position):
        if (self.is_empty()):
            print("Linked list is empty!!")
        else:
            if (position == 1):
                # delete the head if user wants to delete the first position node
                self.delete_head()
                return

            current_position = 1
            current_node = self.head

            while current_node and (current_position < position-1):
                current_node = current_node.next_node
                current_position += 1

            if (position - 1 > current_position):
                # delete tail if user wants to delete nth_item that is at a position greater then the size of linked list
                self.delete_tail()
                return

            if current_node.next_node is None:
                # delete the tail if the current node has no next node  / (Current node IS the tail node)
                self.delete_tail()
                return

            # if current_node.prev_node is None:
            #     # self.delete_head()
            #     return

            if current_node.next_node:

                current_node.next_node.delete()  # the position node
                nx = current_node.next_node.next_node
                nx.prev_node = current_node
                current_node.next_node = nx
                nx.save()
                current_node.save()

                # current_node.next_node.next_node.save()

        self.save()


# make queue
