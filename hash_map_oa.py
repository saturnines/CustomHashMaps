# Name: Kevin Leung
# OSU Email: leungke@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6: Hashmaps Open addressing:
# Due Date: 3/16
# Description: This is a hashmap that uses open addressing

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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

    def put(self, key: str, value: object) -> None:
        """
        Inserts or updates a key-value pair in the hashmap.

        If the key already exists, updates its value. Otherwise, it will add a new key-value pair.
        Automatically resizes the hashmap if the load factor is greater than or equal to 0.5.

        Parameters:
        - key (str): The key for the key-value pair.
        - value (object): The value associated with the key.

        Returns:
        - None
        """
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)
        # double the capacity

        hashed_key = self._hash_function(key)

        j = 0

        while j < self._capacity:
            new_key = (hashed_key + j ** 2) % self._buckets.length()
            curr_bucket = self._buckets.get_at_index(new_key)

            if curr_bucket is None or curr_bucket.is_tombstone:  # if none insert?
                to_insert = HashEntry(key, value)
                self._buckets.set_at_index(new_key, to_insert)
                self._size += 1
                break
            elif curr_bucket.key == key:
                curr_bucket.value = value
                break
            j += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hashmap to the specified capacity or the next prime number greater than it.

        Does nothing if new_capacity is less than the current size of the hashmap.
        It's ensured that the new capacity is prime to have better distribution of entries.

        Parameters:
        - new_capacity (int): The new capacity of the hashmap.

        Returns:
        - None
        """
        if new_capacity < self.get_size():
            return

        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        temp_buckets = DynamicArray()
        for _ in range(new_capacity):
            temp_buckets.append(None)

        old_capacity = self._capacity
        self._capacity = new_capacity
        self._size = 0

        old_buckets = self._buckets
        self._buckets = temp_buckets

        for ind in range(old_capacity):
            old_entry = old_buckets.get_at_index(ind)
            if old_entry is not None and not old_entry.is_tombstone:
                self.put(old_entry.key, old_entry.value)

    def table_load(self) -> float:
        """
        Computes and returns the current load factor of the hashmap.

        The load factor is the ratio of the number of stored entries to the total number of buckets.

        Returns:
        - float: The current load factor of the hashmap.
        """

        res = self._size / self._buckets.length()
        return res

    def empty_buckets(self) -> int:
        """
        Counts and returns the number of empty buckets in the hashmap.

        Returns:
        - int: The number of buckets that are currently not storing any key-value pair.
        """
        count = 0
        for bucket in range(self._buckets.length()):
            hash_entries = self._buckets.get_at_index(bucket)
            if hash_entries is None:
                count += 1

        return count

    def get(self, key: str) -> object:
        """
        Retrieves the value associated with the given key.

        Parameters:
        - key (str): The key whose value is to be retrieved.

        Returns:
        - object: The value associated with the key, or None if the key does not exist.
        """
        hashed_key = self._hash_function(key)

        j = 0

        while j < self._capacity:
            new_key = (hashed_key + j ** 2) % self._buckets.length()
            curr_bucket = self._buckets.get_at_index(new_key)

            if curr_bucket is None:
                return None
            elif key == curr_bucket.key and not curr_bucket.is_tombstone:
                return curr_bucket.value
            j += 1

        return None

    def contains_key(self, key: str) -> bool:
        """
        Checks if the specified key exists in the hashmap.

        Parameters:
        - key (str): The key to check if it exists.

        Returns:
        - bool: True if the key exists, False otherwise.
        """
        hashed_key = self._hash_function(key)

        j = 0

        while j < self._capacity:
            new_key = (hashed_key + j ** 2) % self._buckets.length()
            curr_bucket = self._buckets.get_at_index(new_key)

            if curr_bucket is None:
                return False
            elif key == curr_bucket.key and not curr_bucket.is_tombstone:
                return True
            j += 1

        return False

    def remove(self, key: str) -> None:
        """
        Removes the key-value pair associated with the given key from the hashmap.

        Marks the entry as a tombstone if found, effectively removing it from active entries.

        Parameters:
        - key (str): The key of the pair to be removed.

        Returns:
        - None
        """
        hashed_key = self._hash_function(key)

        j = 0

        while j < self._capacity:
            new_key = (hashed_key + j ** 2) % self._buckets.length()
            curr_bucket = self._buckets.get_at_index(new_key)

            if curr_bucket is None:
                return
            elif key == curr_bucket.key and not curr_bucket.is_tombstone:
                curr_bucket.is_tombstone = True
                self._size -= 1
                return
            j += 1

        return

    def get_keys_and_values(self) -> DynamicArray:
        """
        Retrieves all key-value pairs stored in the hashmap.

        Returns:
        - DynamicArray: An array containing tuples of (key, value) for each active entry.
        """
        result = DynamicArray()
        for bucket in range(self._buckets.length()):
            hash_entries = self._buckets.get_at_index(bucket)
            if hash_entries is not None and not hash_entries.is_tombstone:
                result.append((hash_entries.key, hash_entries.value))

        return result

    def clear(self) -> None:
        """
        Clears the hashmap, removing all key-value pairs and resetting its size.

        Returns:
        - None
        """
        for bucket in range(self._buckets.length()):
            self._buckets.set_at_index(bucket, None)

        self._size = 0

    def __iter__(self):
        """
        Initializes the iterator for traversing the hashmap.

        Resets the internal index used for iteration to 0 and returns the iterable object itself.

        Returns:
        - self: The instance itself as an iterator.
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Advances to the next item in the iteration sequence.

        Iterates through the buckets until a non-tombstone, non-empty entry is found, returning it.
        Will Raise StopIteration when all buckets have been traversed resulting in the end of the iteration.

        Returns:
        - The next active hash entry in the hashmap.

        Raises:
        - StopIteration: If no more active entries are available for iteration.
        """
        while self._index < self._capacity:
            result = self._buckets.get_at_index(self._index)
            self._index += 1

            if result is not None and not result.is_tombstone:
                return result

        raise StopIteration

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)