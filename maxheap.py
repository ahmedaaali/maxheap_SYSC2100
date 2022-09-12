# Ahmed Ali (101181126)
# SYSC 2100 Winter 2022 Lab 11

"""Class BinaryHeap implements a max-heap. The algorithms derived from
the binary heap (min-heap) presented in Section 10.1 of 'Open Data Structures
(in pseudocode)', Edition 0.1G Beta.

This heap implements the priority queue interface. The remove/delete_max
operation always removes the largest element from the heap, which is the
element with the highest priority.

This module was adapted from code from the Open Data Structures project,
opendatastructures.org.

This code (and the code from which it was derived) is released under a
Creative Commons Attribution (CC BY) license. The full text of the license is
available here:

http://creativecommons.org/licenses/by/2.5/ca/
"""

# History:
# Version 1.00 April 4, 2022 - Initial release.

import ctypes
from typing import Any

# A heap is a complete binary tree. Class BinaryHeap represents this tree
# as an array, laying out the nodes in breadth-first order.


def left(i: int) -> int:
    """Return the index of the left child of the node at index i in the array.
    """
    return 2 * i + 1


def right(i: int) -> int:
    """Return the index of the right child of the node at index i in the array.
    """
    return 2 * (i + 1)


def parent(i: int) -> int:
    """Return the index of the parent of the node at index i in the array."""
    return (i - 1) // 2


class BinaryHeap:
    def __init__(self, iterable=[]) -> None:
        """Initialize this BinaryHeap with the contents of iterable.

        If iterable isn't provided, the new heap is empty.
        """
        self._a = _new_array(1)
        self._n = 0
        for elem in iterable:
            self.add(elem)  # add() updates self._n

    def __str__(self) -> str:
        """Return a string representation of this BinaryHeap."""
        # Use repr(x) instead of str(x) in the list comprehension so that
        # elements of type str are enclosed in quotes.
        return "[{0}]".format(", ".join([repr(x) for x in self]))

    def __repr__(self) -> str:
        """Return the canonical string representation of this BinaryHeap."""
        # For a BinaryHeap object, obj, the expression eval(repr(obj))
        # returns a new BinaryHeap that is identical to obj.
        return "{0}({1})".format(self.__class__.__name__, str(self))

    def __len__(self) -> int:
        """Return the number of elements in this BinaryHeap."""
        return self._n

    def __iter__(self):
        """Return an iterator for this BinaryHeap.

        Elements are returned in breadth-first order, starting with the
        root of the heap's tree.
        """
        for i in range(self._n):
            yield self._a[i]

# Operations in the priority queue interface are:
# add, remove/delete_max and find_max.

    def add(self, x: Any) -> bool:
        """Insert x in this BinaryHeap."""
        # Double the capacity of the heap's array if it's full.
        if len(self._a) < self._n + 1:
            self._resize()

        self._a[self._n] = x
        self._n += 1
        # "Bubble" x up the heap's tree until the heap property has been
        # restored.
        self._bubble_up(self._n - 1)
        return True

    def _bubble_up(self, i: int) -> None:
        """A new element was stored at index i in the heap's array.
        Bubble this element up the tree until the heap has been reformed.
        """
        # Repeatedly swap x with its parent, until x is no longer larger
        # than its parent.
        p = parent(i)
        while i > 0 and self._a[i] > self._a[p]:
            self._a[i], self._a[p] = self._a[p], self._a[i]
            i = p
            p = parent(i)

    def remove(self):
        """Remove the largest value from this BinaryHeap and return it."""
        x = self._a[0]  # largest value
        self._a[0] = self._a[self._n - 1]   # Replace the root element
        self._n -= 1

        # "Trickle" the root element down the heap's tree until the heap
        # property has been restored.
        self._trickle_down(0)

        # Decrease the capacity of the heap's array if less than 1/3 of it
        # is used.
        if 3 * self._n < len(self._a):
            self._resize()
        return x

    # The highest priority value can be removed by calling delete_max
    # instead of remove.
    delete_max = remove

    def _trickle_down(self, i: int) -> None:
        """Starting with the element stored at index i in the heap's array,
        trickle this element down the tree until the heap has been reformed.
        """
        # Repeatedly swap the element with its largest child, until the
        # element is larger than its children.
        while i >= 0:
            j = -1  # Index of the child node that will be swapped with its
            # parent.

            # Compare the node at index i with its right child, if it has one.
            r = right(i)
            if r < self._n and self._a[r] > self._a[i]:
                # The node at index i has two children, and is smaller than
                # its right child. Determine which child is the smallest.
                l = left(i)
                if self._a[l] > self._a[r]:
                    # The left child is the largest child, so we'll swap
                    # the parent and its left child.
                    j = l
                else:
                    # The right child is the largest child, so we'll swap
                    # the parent and its right child.
                    j = r
            else:
                # This chunk of code handles two cases:
                # Case 1: the node at index i doesn't have a right child,
                # so compare the node at index i with its left child,
                # if it has one.
                # Case 2: the node at index i has a right child, but its
                # larger than the right child, so compare the node at
                # index i with its left child.

                l = left(i)
                if l < self._n and self._a[l] > self._a[i]:
                    # The node at index i is smaller than its left child,
                    # so we'll swap the two nodes.
                    j = l

            if j >= 0:
                self._a[j], self._a[i] = self._a[i], self._a[j]

            i = j  # If a swap occurred, the element we're trickling down
            # is now at index i.

    def find_max(self):
        """Return the largest value in this BinaryHeap.

        Raise IndexError if the heap is empty.
        """
        if self._n == 0:
            raise IndexError("find_max: empty heap")
        return self._a[0]

    def _resize(self) -> None:
        """Change the capacity of this heap's array to 2 * n, where n is the
        number of elements in the heap. If the heap is empty, change the
        array's capacity to 1.
        """
        b = _new_array(max(2 * self._n, 1))
        b[0:self._n] = self._a[0:self._n]
#         for i in range(self._n):
#             b[i] = self._a[i]
        self._a = b

# Pat's new_array function uses numpy. We're using Python's ctypes module,
# so that students don't have to install numpy.


def _new_array(capacity: int) -> 'py_object_Array_<capacity>':
    """Return a new array with the specified capacity that stores
    references to Python objects.
    """
    if capacity <= 0:
        raise ValueError('new_array: capacity must be > 0')
    PyCArrayType = ctypes.py_object * capacity
    a = PyCArrayType()
    for i in range(len(a)):
        a[i] = None
    return a


if __name__ == '__main__':
    # This script tests the min-heap from the lecture slides, and will require
    # modifications in order to test a max-heap.

    h = BinaryHeap([4, 9, 8, 17, 26, 50, 16, 19, 69, 32])
    assert len(h) == 10
    assert str(h) == '[69, 50, 26, 19, 32, 8, 16, 4, 17, 9]'
    assert repr(h) == 'BinaryHeap([69, 50, 26, 19, 32, 8, 16, 4, 17, 9])'

    h.add(6)
    assert len(h) == 11
    assert str(h) == '[69, 50, 26, 19, 32, 8, 16, 4, 17, 9, 6]'

    assert h.find_max() == 69
    assert h.remove() == 69
    assert len(h) == 10
    assert str(h) == '[50, 32, 26, 19, 9, 8, 16, 4, 17, 6]'

    assert h.find_max() == 50
    assert h.remove() == 50
    assert len(h) == 9

    assert h.find_max() == 32
    assert h.remove() == 32
    assert len(h) == 8

    assert h.find_max() == 26
    assert h.remove() == 26
    assert len(h) == 7

    assert h. find_max() == 19
    assert h.remove() == 19
    assert len(h) == 6

    assert h.find_max() == 17
    assert h.remove() == 17
    assert len(h) == 5

    assert h.find_max() == 16
    assert h.remove() == 16
    assert len(h) == 4

    assert h.find_max() == 9
    assert h.remove() == 9
    assert len(h) == 3

    assert h.find_max() == 8
    assert h.remove() == 8
    assert len(h) == 2

    assert h.find_max() == 6
    assert h.remove() == 6
    assert len(h) == 1

    assert h.find_max() == 4
    assert h.remove() == 4
    assert len(h) == 0
