# Name: Brian Walsh
# OSU Email: walsbria@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 2
# Due Date: 7/17/23
# Description: Implements the class DynamicArray using StaticArray to hold the data.
# Methods are included to set, retrieve, insert, remove, slice, merge, map, filter,
# and reduce the data.  A stand-alone function to find the mode of an array is
# included.


from static_array import StaticArray


class DynamicArrayException(Exception):
    """
    Custom exception class to be used by Dynamic Array
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class DynamicArray:
    def __init__(self, start_array=None):
        """
        Initialize new dynamic array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._size = 0
        self._capacity = 4
        self._data = StaticArray(self._capacity)

        # populate dynamic array with initial values (if provided)
        # before using this feature, implement append() method
        if start_array is not None:
            for value in start_array:
                self.append(value)

    def __str__(self) -> str:
        """
        Return content of dynamic array in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "DYN_ARR Size/Cap: "
        out += str(self._size) + "/" + str(self._capacity) + ' ['
        out += ', '.join([str(self._data[_]) for _ in range(self._size)])
        return out + ']'

    def __iter__(self):
        """
        Create iterator for loop
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        try:
            value = self[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return value

    def get_at_index(self, index: int) -> object:
        """
        Return value from given index position
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        return self._data[index]

    def set_at_index(self, index: int, value: object) -> None:
        """
        Store value at given index in the array
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        self._data[index] = value

    def __getitem__(self, index) -> object:
        """
        Same functionality as get_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.get_at_index(index)

    def __setitem__(self, index, value) -> None:
        """
        Same functionality as set_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.set_at_index(index, value)

    def is_empty(self) -> bool:
        """
        Return True is array is empty / False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size == 0

    def length(self) -> int:
        """
        Return number of elements stored in array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return the capacity of the array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    def print_da_variables(self) -> None:
        """
        Print information contained in the dynamic array.
        Used for testing purposes.
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        print(f"Length: {self._size}, Capacity: {self._capacity}, {self._data}")

    # -----------------------------------------------------------------------

    def resize(self, new_capacity: int) -> None:
        """
        Resize the dynamic array by creating a new StaticArray, copying the
        contents of the old array, and then setting the new array as the data.

        Param new_capacity: int defining the new array size
        Returns:            Nothing
        """
        # do nothing if new_capacity is < 0 or current size
        if new_capacity < 1 or new_capacity < self._size:
            return

        # if we're sizing down, only need the elements that will fit
        if new_capacity < self._capacity:
            length = new_capacity
        else:
            length = self._capacity

        new_array = StaticArray(new_capacity)
        for i in range(0, length):
            new_array[i] = self._data[i]
        self._capacity = new_capacity
        self._data = new_array

    def append(self, value: object) -> None:
        """
        Appends a value to the end of self._data

        Param value:    the value to append
        Returns:        Nothing
        """
        # array is full, create a new one before proceeding
        if self._size == self._capacity:
            self.resize(2 * self._size)

        self._data[self._size] = value
        self._size += 1

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Inserts a value in the array at the specified index.

        Param index:        int, the index to insert at
        Param value:        the value to insert
        Returns:            Nothing
        """
        # check that the index is valid
        if index > self._size or index < 0:
            raise DynamicArrayException

        # make a new array if required
        if self._size == self._capacity:
            self.resize(2 * self._size)

        # shift everything from the end to the requested index right
        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]
        self._data[index] = value
        self._size += 1

    def remove_at_index(self, index: int) -> None:
        """
        Removes the value at the specified index.

        Param index:        int of the index to remove
        Returns:            nothing
        """

        # check that the index is valid
        if index > self._size - 1 or index < 0:
            raise DynamicArrayException

        # if our current storage is < 1/4 of capacity, reduce it
        # minimum capacity is 10
        if self._size < self._capacity * .25 and self._capacity > 10:
            if self._size * 2 > 10:
                self.resize(self._size * 2)
            else:
                self.resize(10)

        # shift data left, overwriting the removed index
        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]

        self._size -= 1

    def slice(self, start_index: int, size: int) -> "DynamicArray":
        """
        Returns a slice of the array defined by a starting index and size.

        param start_index (int):    where to start the slice
        param size (int):           size of the slice
        returns:                    DynamicArray object with requested data
        """

        # check that size is non-negative
        if size < 0:
            raise DynamicArrayException

        # check that start_index is in range
        if start_index < 0 or start_index > self._size - 1:
            raise DynamicArrayException

        # check we have enough elements to fulfill the request
        if self._size - start_index < size:
            raise DynamicArrayException

        # create and return a new array with the requested data
        slice_array = DynamicArray()
        for i in range(start_index, start_index + size):
            slice_array.append(self._data[i])
        return slice_array

    def merge(self, second_da: "DynamicArray") -> None:
        """
        Merges a DynamicArray object with data by appending values

        Param second_da (DynamicArray)  The array to merge
        Returns:                        nothing
        """

        # iterate through second_da and append values to data
        for value in second_da:
            self.append(value)

    def map(self, map_func) -> "DynamicArray":
        """
        Returns a new array with values transformed from data by map_func.

        param map_func(x):    function by which values will be transformed
        returns:              DynamicArray object containing new values
        """

        # get values from data, transform with map_func, and append them
        map_array = DynamicArray()
        for value in self:
            map_array.append(map_func(value))

        return map_array

    def filter(self, filter_func) -> "DynamicArray":
        """
        Returns a new array with values filtered by filter_func.

        param filter_func(x):   function by which values will be filtered
        returns:                DynamicArray object containing filtered values
        """

        # test data values against the filter function, append if True
        filter_array = DynamicArray()
        for value in self:
            if filter_func(value):
                filter_array.append(value)

        return filter_array

    def reduce(self, reduce_func, initializer=None) -> object:
        """
        Returns a value calculated from elements in data by repeated sequential
        applications of reduce_func. An optional initializer parameter may be
        provided to be used as the first input to reduce_func, otherwise the
        first element of the array will be used.

        param reduce_func(x,y):     function used to calculate a value from two
                                    supplied elements
        param initializer:          optional value used as the first element
                                    passed to reduce_func
        return:                     final value calculated by reduce_func
        """

        # if array size is 0, return the initializer
        if self._size == 0:
            return initializer

        # if initializer != None, pass it in as the first parameter
        if initializer:
            for i in range(-1, self._size - 1):
                initializer = reduce_func(initializer, self._data[i + 1])

        # otherwise, use the first element of the array
        else:
            initializer = self._data[0]
            for i in range(0, self._size - 1):
                initializer = reduce_func(initializer, self._data[i + 1])

        return initializer


def update_mode_arr(return_arr, value, count, temp_count) -> (DynamicArray, int):
    """
    Helper function to update the array returned by find_mode.

    param return_arr:       DynamicArray object containing the mode of the array
    param value:            value to store
    param count:            current highest frequency
    param temp_count:       frequency of current object
    return:                 return_arr, count
    """

    # if object frequency = current highest, append it
    if temp_count == count:
        return_arr.append(value)

    # if frequency > other values, overwrite old array with new value
    if temp_count > count:
        return_arr = DynamicArray()
        return_arr.append(value)
        count = temp_count

    return return_arr, count


def find_mode(arr: DynamicArray) -> (DynamicArray, int):
    """
    Finds the mode of the array and returns a DynamicArray object composing the
    mode of the array, and an int with the frequency of the mode. Multiple
    values with the same frequency will be returned with the values appearing
    first in the array also appearing first in the return.

    param arr:      DynamicArray to find the mode of
    return:         DynamicArray of the mode, and int of the frequency
    """

    temp_count = 1
    count = 1
    return_arr = DynamicArray()

    # if array length is 1, return the array and frequency 1
    if arr.length() == 1:
        return arr, 1

    # move through the array and compare the current index with previous
    for i in range(1, arr.length()):

        # if current and previous values are the same, increment temp_count
        if arr.get_at_index(i) == arr.get_at_index(i - 1):
            temp_count += 1

        # new value found, store as required by temp_count vs count
        else:
            return_arr, count = update_mode_arr(return_arr, arr.get_at_index(i - 1), count, temp_count)
            temp_count = 1

        # reached the end of the array, store values if required
        if i == arr.length() - 1:
            return_arr, count = update_mode_arr(return_arr, arr.get_at_index(i), count, temp_count)

    return return_arr, count


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# resize - example 1")
    da = DynamicArray()

    # print dynamic array's size, capacity and the contents
    # of the underlying static array (data)
    da.print_da_variables()
    da.resize(8)
    da.print_da_variables()
    da.resize(2)
    da.print_da_variables()
    da.resize(0)
    da.print_da_variables()

    print("\n# resize - example 2")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8])
    print(da)
    da.resize(20)
    print(da)
    da.resize(4)
    print(da)

    print("\n# append - example 1")
    da = DynamicArray()
    da.print_da_variables()
    da.append(1)
    da.print_da_variables()
    print(da)

    print("\n# append - example 2")
    da = DynamicArray()
    for i in range(9):
        da.append(i + 101)
        print(da)

    print("\n# append - example 3")
    da = DynamicArray()
    for i in range(600):
        da.append(i)
    print(da.length())
    print(da.get_capacity())

    print("\n# insert_at_index - example 1")
    da = DynamicArray([100])
    print(da)
    da.insert_at_index(0, 200)
    da.insert_at_index(0, 300)
    da.insert_at_index(0, 400)
    print(da)
    da.insert_at_index(3, 500)
    print(da)
    da.insert_at_index(1, 600)
    print(da)

    print("\n# insert_at_index example 2")
    da = DynamicArray()
    try:
        da.insert_at_index(-1, 100)
    except Exception as e:
        print("Exception raised:", type(e))
    da.insert_at_index(0, 200)
    try:
        da.insert_at_index(2, 300)
    except Exception as e:
        print("Exception raised:", type(e))
    print(da)

    print("\n# insert at index example 3")
    da = DynamicArray()
    for i in range(1, 10):
        index, value = i - 4, i * 10
        try:
            da.insert_at_index(index, value)
        except Exception as e:
            print("Cannot insert value", value, "at index", index)
    print(da)

    print("\n# remove_at_index - example 1")
    da = DynamicArray([10, 20, 30, 40, 50, 60, 70, 80])
    print(da)
    da.remove_at_index(0)
    print(da)
    da.remove_at_index(6)
    print(da)
    da.remove_at_index(2)
    print(da)

    print("\n# remove_at_index - example 2")
    da = DynamicArray([1024])
    print(da)
    for i in range(17):
        da.insert_at_index(i, i)
    print(da.length(), da.get_capacity())
    for i in range(16, -1, -1):
        da.remove_at_index(0)
    print(da)

    print("\n# remove_at_index - example 3")
    da = DynamicArray()
    print(da.length(), da.get_capacity())
    [da.append(1) for i in range(100)]  # step 1 - add 100 elements
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(68)]  # step 2 - remove 68 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 3 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 4 - remove 1 element
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(14)]  # step 5 - remove 14 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 6 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 7 - remove 1 element
    print(da.length(), da.get_capacity())

    for i in range(14):
        print("Before remove_at_index(): ", da.length(), da.get_capacity(), end="")
        da.remove_at_index(0)
        print(" After remove_at_index(): ", da.length(), da.get_capacity())

    print("\n# remove at index - example 4")
    da = DynamicArray([1, 2, 3, 4, 5])
    print(da)
    for _ in range(5):
        da.remove_at_index(0)
        print(da)

    print("\n# slice example 1")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8, 9])
    da_slice = da.slice(1, 3)
    print(da, da_slice, sep="\n")
    da_slice.remove_at_index(0)
    print(da, da_slice, sep="\n")

    print("\n# slice example 2")
    da = DynamicArray([10, 11, 12, 13, 14, 15, 16])
    print("SOURCE:", da)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1), (6, -1)]
    for i, cnt in slices:
        print("Slice", i, "/", cnt, end="")
        try:
            print(" --- OK: ", da.slice(i, cnt))
        except:
            print(" --- exception occurred.")

    print("\n# merge example 1")
    da = DynamicArray([1, 2, 3, 4, 5])
    da2 = DynamicArray([10, 11, 12, 13])
    print(da)
    da.merge(da2)
    print(da)

    print("\n# merge example 2")
    da = DynamicArray([1, 2, 3])
    da2 = DynamicArray()
    da3 = DynamicArray()
    da.merge(da2)
    print(da)
    da2.merge(da3)
    print(da2)
    da3.merge(da)
    print(da3)

    print("\n# map example 1")
    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    print(da.map(lambda x: x ** 2))

    print("\n# map example 2")


    def double(value):
        return value * 2


    def square(value):
        return value ** 2


    def cube(value):
        return value ** 3


    def plus_one(value):
        return value + 1


    da = DynamicArray([plus_one, double, square, cube])
    for value in [1, 10, 20]:
        print(da.map(lambda x: x(value)))

    print("\n# filter example 1")


    def filter_a(e):
        return e > 10


    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    result = da.filter(filter_a)
    print(result)
    print(da.filter(lambda x: (10 <= x <= 20)))

    print("\n# filter example 2")


    def is_long_word(word, length):
        return len(word) > length


    da = DynamicArray("This is a sentence with some long words".split())
    print(da)
    for length in [3, 4, 7]:
        print(da.filter(lambda word: is_long_word(word, length)))

    print("\n# reduce example 1")
    values = [100, 5, 10, 15, 20, 25]
    da = DynamicArray(values)
    print(da)
    print(da.reduce(lambda x, y: (x // 5 + y ** 2)))
    print(da.reduce(lambda x, y: (x + y ** 2), -1))

    print("\n# reduce example 2")
    da = DynamicArray([100])
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))
    da.remove_at_index(0)
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))

    print("\n# find_mode - example 1")
    test_cases = (
        [1, 1, 2, 3, 3, 4],
        [1, 2, 3, 4, 5],
        ["Apple", "Banana", "Banana", "Carrot", "Carrot",
         "Date", "Date", "Date", "Eggplant", "Eggplant", "Eggplant",
         "Fig", "Fig", "Grape"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}\n")

    case = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    da = DynamicArray()
    for x in range(len(case)):
        da.append(case[x])
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}")
