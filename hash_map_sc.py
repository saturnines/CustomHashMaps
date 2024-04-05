# Name: Kevin Leung
# OSU Email: leungke@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6: Hashmaps separate chaining:
# Due Date: 3/16
# Description: This is a hashmap that uses separate chaining


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def get_buckets(self):
        """Getter to return number of buckets"""
        return self._buckets

    def put(self, key: str, value: object) -> None:
        """
        Inserts or updates a key-value pair in the hashmap. If the load factor reaches or exceeds 1.0,
        the hashmap's capacity is doubled before inserting the new element.

        Parameters:
        - key (str): The key to insert or update in the hashmap.
        - value (object): The value associated with the key.

        Returns:
        - None
        """
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity * 2)

        hashed = self._hash_function(key)
        ll_nodes = self._buckets.get_at_index(hashed % self._capacity)

        for node in ll_nodes:
            if node.key == key:
                node.value = value
                return

        ll_nodes.insert(key, value)
        self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hashmap to a specified capacity. If the new capacity is less than the minimum size (1)
        or not a prime number, adjustments are made to ensure it meets requirements (e.g., finding the next prime).

        Parameters:
        - new_capacity (int): The new capacity for the hashmap.

        Returns:
        - None
        """
        if new_capacity < 1:
            return

        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        new_bucket = DynamicArray()
        self._capacity = new_capacity

        for _ in range(self._capacity):
            new_bucket.append(LinkedList())

        #  rehash (key % new_size)
        for i in range(self._buckets.length()):
            buckets = self._buckets.get_at_index(i)
            for node in buckets:
                new_hash = self._hash_function(node.key) % new_capacity
                new_bucket.get_at_index(new_hash).insert(node.key, node.value)

        self._buckets = new_bucket

    def table_load(self) -> float:
        """
        Calculates and returns the load factor of the hashmap, defined as the ratio of the number of elements
        to the number of buckets.

        Returns:
        - float: The current load factor of the hashmap.
        """
        res = self._size / self._buckets.length()
        return res

    def empty_buckets(self) -> int:
        """
        Counts and returns the number of buckets in the hashmap that are empty.

        Returns:
        - int: The number of empty buckets.
        """
        count = 0
        for i in range(self._buckets.length()):
            ll = self._buckets.get_at_index(i)
            if ll.length() == 0:
                count += 1
        return count

    def get(self, key: str):
        """
        Retrieves the value associated with a given key from the hashmap. If the key does not exist,
        returns None.

        Parameters:
        - key (str): The key whose value is to be retrieved.

        Returns:
        - object: The value associated with the key, or None if the key is not found.
        """
        hashed = self._hash_function(key)
        ll_nodes = self._buckets.get_at_index(hashed % self._capacity)
        node = ll_nodes.contains(key)
        return node.value if node is not None else None

    def contains_key(self, key: str) -> bool:
        """
        Checks whether a specified key exists in the hashmap.

        Parameters:
        - key (str): The key to check in the hashmap.

        Returns:
        - bool: True if the key exists, False otherwise.
        """

        hashed = self._hash_function(key)
        ll_nodes = self._buckets.get_at_index(hashed % self._capacity)
        node = ll_nodes.contains(key)
        return True if node is not None else False

    def remove(self, key: str) -> None:
        """
        Removes a key-value pair from the hashmap based on the specified key. If the key is found
        and successfully removed, the size of the hashmap is decremented.

        Parameters:
        - key (str): The key of the pair to be removed.

        Returns:
        - None
        """
        hashed = self._hash_function(key)
        ll_nodes = self._buckets.get_at_index(hashed % self._capacity)
        if ll_nodes.remove(key):
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Collects and returns all key-value pairs present in the hashmap.

        Returns:
        - DynamicArray: An array containing tuples (key, value) for each entry in the hashmap.
        """
        res = DynamicArray()

        for i in range(self._buckets.length()):
            ll = self._buckets.get_at_index(i)
            for nodes in ll:
                if nodes is not None:
                    res.append((nodes.key, nodes.value))
        return res

    def clear(self) -> None:
        """
        Clears the hashmap, removing all key-value pairs and resetting its size to zero.

        Returns:
        - None
        """
        for i in range(self._buckets.length()):
            self._buckets.set_at_index(i, LinkedList())

        self._size = 0


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Identifies and returns the mode(s) of the values in a DynamicArray and their frequency.

    The function iterates over the array, counting the occurrences of each element using a hashmap,
    and then determines the element(s) with the highest frequency.

    Parameters:
    - da (DynamicArray): The array from which to find the mode.

    Returns:
    - tuple[DynamicArray, int]: A tuple containing a DynamicArray of the most frequent element(s) and
      an integer representing their frequency.
    """
    map = HashMap()

    for i in range(da.length()):
        values = da.get_at_index(i)
        if map.contains_key(values) is True:
            add_one = map.get(values)
            map.put(values, add_one + 1)
        else:
            map.put(values, 1)

    # Find the highest frequency
    highest_mode = 0
    for i in range(map.get_capacity()):
        bucket = map.get_buckets().get_at_index(i)
        for node in bucket:
            if node and node.value > highest_mode:
                highest_mode = node.value

    res = DynamicArray()
    for i in range(map.get_capacity()):
        bucket = map.get_buckets().get_at_index(i)
        for node in bucket:
            if node and node.value == highest_mode:
                res.append(node.key)

    return res, highest_mode


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
