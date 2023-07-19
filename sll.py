# Name: Brian Walsh
# OSU Email: walsbria@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 3
# Due Date: 7/24/23
# Description: Implements a singly linked list. Methods are provided to return
# insert or remove at the front, back, or a specific index, remove the first
# instance of a value, count the occurrences of a value, search for a value,
# return the length, return whether the list is empty, and return a slice of
# the list.


from SLNode import *


class SLLException(Exception):
    """
    Custom exception class to be used by Singly Linked List
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class LinkedList:
    def __init__(self, start_list=None) -> None:
        """
        Initialize new linked list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._head = SLNode(None)

        # populate SLL with initial values (if provided)
        # before using this feature, implement insert_back() method
        if start_list is not None:
            for value in start_list:
                self.insert_back(value)

    def __str__(self) -> str:
        """
        Return content of singly linked list in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = 'SLL ['
        node = self._head.next
        while node:
            out += str(node.value)
            if node.next:
                out += ' -> '
            node = node.next
        out += ']'
        return out

    def length(self) -> int:
        """
        Return the length of the linked list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        length = 0
        node = self._head.next
        while node:
            length += 1
            node = node.next
        return length

    def is_empty(self) -> bool:
        """
        Return True is list is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return not self._head.next

    # ------------------------------------------------------------------ #

    def insert_front(self, value: object) -> None:
        """
        Inserts a node at the front of the linked list.

        Param value:    value to assign to the node
        Returns:        nothing
        """

        new_node = SLNode(value, self._head.next)
        self._head.next = new_node

    def insert_back(self, value: object) -> None:
        """
        Inserts a node at the end of the linked list.

        Param value:    value to assign to the node
        Returns:        nothing
        """

        new_node = SLNode(value)
        # find the end of the list where node.next = None
        node = self._head
        while node.next is not None:
            node = node.next
        node.next = new_node

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Inserts a node at the specified index.

        Param value:    value to assign to the node
        Param index:    where to insert in the list
        Returns:        nothing
        """

        if index < 0 or index > self.length():
            raise SLLException

        new_node = SLNode(value)
        node = self._head
        for i in range(index):
            node = node.next

        new_node.next = node.next
        node.next = new_node

    def remove_at_index(self, index: int) -> None:
        """
        Removes a node at the specified index.

        Param value:    value to assign to the node
        Param index:    index to remove from the list
        Returns:        nothing
        """
        if index < 0 or index >= self.length():
            raise SLLException


        node = self._head
        for i in range(index):
            node = node.next

        node.next = node.next.next

    def remove(self, value: object) -> bool:
        """
        Removes the first occurrence of a node with the specified value.
        Returns True if a node is removed, False otherwise.

        Param value:    value to assign to the node
        Returns:        True if value removed, False otherwise
        """

        node = self._head
        while node.next is not None:
            if node.next.value == value:
                node.next = node.next.next
                return True
            node = node.next

        return False

    def count(self, value: object) -> int:
        """
        Returns the occurrences of value in the list.

        Param value:    the value to count
        Returns:        the number of occurrences
        """

        count = 0
        node = self._head
        while node.next is not None:
            if node.next.value == value:
                count += 1
            node = node.next

        return count

    def find(self, value: object) -> bool:
        """
        Returns True if the value exists in the list. Returns False otherwise

        Param value:    The value to find
        Returns:        True if found, False if not
        """

        node = self._head
        while node.next is not None:
            if node.next.value == value:
                return True
            node = node.next

        return False

    def slice(self, start_index: int, size: int) -> "LinkedList":
        """
        Returns a LinkedList object containing a slice of the original list.

        Param start_index:      the index to start the slice at
        Param size:             how many successive values to return
        """

        if start_index < 0:
            raise SLLException

        return_list = LinkedList()
        node = self._head

        # move to the starting index
        for i in range(start_index + 1):
            node = node.next

        # save node.value to the return list and move to the next node
        # if value = None we have reached the end of the list
        for j in range(size):
            if node is None:
                raise SLLException
            return_list.insert_back(node.value)
            node = node.next

        return return_list




if __name__ == "__main__":

    print("\n# insert_front example 1")
    test_case = ["A", "B", "C"]
    lst = LinkedList()
    for case in test_case:
        lst.insert_front(case)
        print(lst)

    print("\n# insert_back example 1")
    test_case = ["C", "B", "A"]
    lst = LinkedList()
    for case in test_case:
        lst.insert_back(case)
        print(lst)

    print("\n# insert_at_index example 1")
    lst = LinkedList()
    test_cases = [(0, "A"), (0, "B"), (1, "C"), (3, "D"), (-1, "E"), (5, "F")]
    for index, value in test_cases:
        print("Inserted", value, "at index", index, ": ", end="")
        try:
            lst.insert_at_index(index, value)
            print(lst)
        except Exception as e:
            print(type(e))

    print("\n# remove_at_index example 1")
    lst = LinkedList([1, 2, 3, 4, 5, 6])
    print(f"Initial LinkedList : {lst}")
    for index in [0, 2, 0, 2, 2, -2]:
        print("Removed at index", index, ": ", end="")
        try:
            lst.remove_at_index(index)
            print(lst)
        except Exception as e:
            print(type(e))

    print("\n# remove example 1")
    lst = LinkedList([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(f"Initial LinkedList, Length: {lst.length()}\n  {lst}")
    for value in [7, 3, 3, 3, 3]:
        print(f"remove({value}): {lst.remove(value)}, Length: {lst.length()}"
              f"\n {lst}")

    print("\n# remove example 2")
    lst = LinkedList([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(f"Initial LinkedList, Length: {lst.length()}\n  {lst}")
    for value in [1, 2, 3, 1, 2, 3, 3, 2, 1]:
        print(f"remove({value}): {lst.remove(value)}, Length: {lst.length()}"
              f"\n {lst}")

    print("\n# count example 1")
    lst = LinkedList([1, 2, 3, 1, 2, 2])
    print(lst, lst.count(1), lst.count(2), lst.count(3), lst.count(4))

    print("\n# find example 1")
    lst = LinkedList(["Waldo", "Clark Kent", "Homer", "Santa Claus"])
    print(lst)
    print(lst.find("Waldo"))
    print(lst.find("Superman"))
    print(lst.find("Santa Claus"))

    print("\n# slice example 1")
    lst = LinkedList([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ll_slice = lst.slice(1, 3)
    print("Source:", lst)
    print("Start: 1 Size: 3 :", ll_slice)
    ll_slice.remove_at_index(0)
    print("Removed at index 0 :", ll_slice)

    print("\n# slice example 2")
    lst = LinkedList([10, 11, 12, 13, 14, 15, 16])
    print("Source:", lst)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1)]
    for index, size in slices:
        print("Start:", index, "Size:", size, end="")
        try:
            print(" :", lst.slice(index, size))
        except:
            print(" : exception occurred.")
