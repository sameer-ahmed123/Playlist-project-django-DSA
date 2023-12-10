from django.db import models


class Node(models.Model):
    Title = models.CharField(max_length=350)
    Music_file = models.FileField(upload_to="Audio_files", null=True)
    Author = models.CharField(max_length=250, null=True, blank=True)
    next_node = models.OneToOneField(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='prev_node_of')
    prev_node = models.OneToOneField(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name="next_node_of")

    def __str__(self):
        return f"{self.Title}'s Node"

    def delete(self, *args, **kwargs):
        super(Node, self).delete(*args, **kwargs)


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
        new_node = Node(Title=Title, Music_file=Music_file, Author=Author)
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
            print(nxNode)

            if nxNode:
                nxNode.prev_node.delete()  # delete the node that was before the nxNode (current head)
                nxNode.prev_node = None
                self.head = nxNode      # set the new head as nxNode
                self.head.save()  # save changed head to the database
                self.save()  # save linked list only if multiple nodes are present in the linked list

            else:
                print("single item in list , head and tail")
                self.head.delete()
                self = None
                # set the linked list  itself to none without saving when only one item is in the list
                # saving while deleting the last item was causing foreign key constraint issues

    def delete_tail(self):
        if self.is_empty():
            print("the node list is empty")
        else:
            prNode = self.tail.prev_node

            if prNode:
                prNode.next_node.delete()
                prNode.next_node = None
                self.tail = prNode
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
