# Name: Brian Walsh
# OSU Email: walsbria@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 3
# Due Date: 7/24/23
# Description: Implements a stack ADT using a singly linked list. In this
# implementation, the head of the list is the top of the stack. Methods are
# provided to push, pop, and peek, as well as find size and if the stack
# is empty.


from SLNode import SLNode


class StackException(Exception):
    """
    Custom exception to be used by Stack class
    DO NOT CHANGE THIS METHOD IN ANY WAY
    """
    pass


class Stack:
    def __init__(self) -> None:
        """
        Initialize new stack with head node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._head = None

    def __str__(self) -> str:
        """
        Return content of stack in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = 'STACK ['
        if not self.is_empty():
            node = self._head
            out = out + str(node.value)
            node = node.next
            while node:
                out = out + ' -> ' + str(node.value)
                node = node.next
        return out + ']'

    def is_empty(self) -> bool:
        """
        Return True is the stack is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._head is None

    def size(self) -> int:
        """
        Return number of elements currently in the stack
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        node = self._head
        length = 0
        while node:
            length += 1
            node = node.next
        return length

    # -----------------------------------------------------------------------

    def push(self, value: object) -> None:
        """
        Inserts a node with value at the head of the linked list.

        param value:    the value to store in the list
        returns:        nothing
        """

        new_node = SLNode(value)

        if self._head is None:
            self._head = new_node
        else:
            new_node.next = self._head
            self._head = new_node

    def pop(self) -> object:
        """
        Returns the value at the head of the linked list and removes it.

        param:      nothing
        returns:    nothing
        """

        if self.size() == 0:
            return StackException

        ret_val = self._head.value
        self._head = self._head.next
        return ret_val


    def top(self) -> object:
        """
        Returns the value at the head of the list. This method does not modify
        the list.
        """

        if self.size() == 0:
            return StackException

        return self._head.value

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# push example 1")
    s = Stack()
    print(s)
    for value in [1, 2, 3, 4, 5]:
        s.push(value)
    print(s)

    print("\n# pop example 1")
    s = Stack()
    try:
        print(s.pop())
    except Exception as e:
        print("Exception:", type(e))
    for value in [1, 2, 3, 4, 5]:
        s.push(value)
    for i in range(6):
        try:
            print(s.pop())
        except Exception as e:
            print("Exception:", type(e))

    print("\n# top example 1")
    s = Stack()
    try:
        s.top()
    except Exception as e:
        print("No elements in stack", type(e))
    s.push(10)
    s.push(20)
    print(s)
    print(s.top())
    print(s.top())
    print(s)
