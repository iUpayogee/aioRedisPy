from aioredis.util import wait_convert, wait_ok, _NOTSET


class StringCommandsMixin:
    """String commands mixin.

    For commands details see: http://redis.io/commands/#string
    """

    def append(self, key, value):
        """Append a value to key.

        :raises TypeError: if key is None
        """
        if key is None:
            raise TypeError("key argument must not be None")
        return self._conn.execute(b'APPEND', key, value)

    def bitcount(self, key, start=None, end=None):
        """Count set bits in a string.

        :raises TypeError: if key is None
        :raises TypeError: if only start or end specified.
        """
        if key is None:
            raise TypeError("key argument must not be None")
        if start is None and end is not None:
            raise TypeError("both start and stop must be specified")
        elif start is not None and end is None:
            raise TypeError("both start and stop must be specified")
        elif start is not None and end is not None:
            args = (start, end)
        else:
            args = ()
        return self._conn.execute(b'BITCOUNT', key, *args)

    def bitop_and(self, dest, key, *keys):
        """Perform bitwise AND operations between strings.

        :raises TypeError: if any of arguments is None
        """
        if dest is None:
            raise TypeError("dest argument must not be None")
        if key is None:
            raise TypeError("key argument must not be None")
        if None in set(keys):
            raise TypeError("keys must not contain None")
        return self._conn.execute(b'BITOP', b'AND', dest, key, *keys)

    def bitop_or(self, dest, key, *keys):
        """Perform bitwise OR operations between strings.

        :raises TypeError: if any of arguments is None
        """
        if dest is None:
            raise TypeError("dest argument must not be None")
        if key is None:
            raise TypeError("key argument must not be None")
        if None in set(keys):
            raise TypeError("keys must not contain None")
        return self._conn.execute(b'BITOP', b'OR', dest, key, *keys)

    def bitop_xor(self, dest, key, *keys):
        """Perform bitwise XOR operations between strings.

        :raises TypeError: if any of arguments is None
        """
        if dest is None:
            raise TypeError("dest argument must not be None")
        if key is None:
            raise TypeError("key argument must not be None")
        if None in set(keys):
            raise TypeError("keys must not contain None")
        return self._conn.execute(b'BITOP', b'XOR', dest, key, *keys)

    def bitop_not(self, dest, key):
        """Perform bitwise NOT operations between strings.

        :raises TypeError: if dest or key is None
        """
        if dest is None:
            raise TypeError("dest argument must not be None")
        if key is None:
            raise TypeError("key argument must not be None")
        return self._conn.execute(b'BITOP', b'NOT', dest, key)

    def bitpos(self, key, bit, start=None, end=None):
        """Find first bit set or clear in a string.

        :raises TypeError: if key is None
        :raises ValueError: if bit is not 0 or 1
        """
        if key is None:
            raise TypeError("key argument must not be None")
        if bit not in (1, 0):
            raise ValueError("bit argument must be either 1 or 0")
        bytes_range = []
        if start is not None:
            bytes_range.append(start)
        if end is not None:
            if start is None:
                bytes_range = [0, end]
            else:
                bytes_range.append(end)
        return self._conn.execute(b'BITPOS', key, bit, *bytes_range)

    def decr(self, key):
        """Decrement the integer value of a key by one.

        :raises TypeError: if key is None
        """
        if key is None:
            raise TypeError("key argument must not be None")
        return self._conn.execute(b'DECR', key)

    def decrby(self, key, decrement):
        """Decrement the integer value of a key by the given number.

        :raises TypeError: if key is None
        :raises TypeError: if decrement is not int
        """
        if key is None:
            raise TypeError("key argument must not be None")
        if not isinstance(decrement, int):
            raise TypeError("decrement must be of type int")
        return self._conn.execute(b'DECRBY', key, decrement)

    def get(self, key, *, encoding=_NOTSET):
        """Get the value of a key.

        :raises TypeError: if key is None
        """
        if key is None:
            raise TypeError("key argument must not be None")
        return self._conn.execute(b'GET', key, encoding=encoding)

    def getbit(self, key, offset):
        """Returns the bit value at offset in the string value stored at key.

        :raises TypeError: if key is None
        :raises TypeError: if offset is not int
        :raises ValueError: if offset is less then 0
        """
        if key is None:
            raise TypeError("key argument must not be None")
        if not isinstance(offset, int):
            raise TypeError("offset argument must be int")
        if offset < 0:
            raise ValueError("offset must be greater equal 0")
        return self._conn.execute(b'GETBIT', key, offset)

    def getrange(self, key, start, end):
        """Get a substring of the string stored at a key.

        :raises TypeError: if key is None
        :raises TypeError: if start or end is not int
        """
        if key is None:
            raise TypeError("key argument must not be None")
        if not isinstance(start, int):
            raise TypeError("start argument must be int")
        if not isinstance(end, int):
            raise TypeError("end argument must be int")
        return self._conn.execute(b'GETRANGE', key, start, end)

    def getset(self, key, value):
        """Set the string value of a key and return its old value.

        :raises TypeError: if key is None
        """
        if key is None:
            raise TypeError("key argument must not be None")
        return self._conn.execute(b'GETSET', key, value)

    def incr(self, key):
        """Increment the integer value of a key by one.

        :raises TypeError: if key is None
        """
        if key is None:
            raise TypeError("key argument must not be None")
        return self._conn.execute(b'INCR', key)

    def incrby(self, key, increment):
        """Increment the integer value of a key by the given amount.

        :raises TypeError: if key is None
        :raises TypeError: if increment is not int
        """
        if key is None:
            raise TypeError("key argument must not be None")
        if not isinstance(increment, int):
            raise TypeError("increment must be of type int")
        return self._conn.execute(b'INCRBY', key, increment)

    def incrbyfloat(self, key, increment):
        """Increment the float value of a key by the given amount.

        :raises TypeError: if key is None
        :raises TypeError: if increment is not int
        """
        if key is None:
            raise TypeError("key argument must not be None")
        if not isinstance(increment, float):
            raise TypeError("increment must be of type int")
        fut = self._conn.execute(b'INCRBYFLOAT', key, increment)
        return wait_convert(fut, float)

    def mget(self, key, *keys):
        """Get the values of all the given keys.

        :raises TypeError: if any of arguments is None
        """
        if key is None:
            raise TypeError("key argument must not be None")
        if None in set(keys):
            raise TypeError("keys must not contain None")
        return self._conn.execute(b'MGET', key, *keys)

    def mset(self, key, value, *pairs):
        """Set multiple keys to multiple values.

        :raises TypeError: if key is None
        :raises TypeError: if len of pairs is not event number
        """
        if key is None:
            raise TypeError("key argument must not be None")
        if len(pairs) % 2 != 0:
            raise TypeError("length of pairs must be even number")
        fut = self._conn.execute(b'MSET', key, value, *pairs)
        return wait_ok(fut)

    def msetnx(self, key, value, *pairs):
        """Set multiple keys to multiple values,
        only if none of the keys exist.

        :raises TypeError: if key is None
        :raises TypeError: if len of pairs is not event number
        """
        if key is None:
            raise TypeError("key argument must not be None")
        if len(pairs) % 2 != 0:
            raise TypeError("length of pairs must be even number")
        return self._conn.execute(b'MSETNX', key, value, *pairs)

    def psetex(self, key, milliseconds, value):
        """Set the value and expiration in milliseconds of a key.

        :raises TypeError: if key is None
        :raises TypeError: if milliseconds is not int
        """
        if key is None:
            raise TypeError("key argument must not be None")
        if not isinstance(milliseconds, int):
            raise TypeError("milliseconds argument must be int")
        fut = self._conn.execute(b'PSETEX', key, milliseconds, value)
        return wait_ok(fut)

    def set(self, key, value, expire=0, pexpire=0,
            only_if_not_exists=False, only_if_exists=False):
        """Set the string value of a key.

        :raises TypeError: if key is None
        :raises TypeError: if only_if_not_exists and  only_if_exists both
                           specified in same time.
        :raises TypeError: if expire is not int
        :raises TypeError: if pexpire is not int
        """
        if key is None:
            raise TypeError("key argument must not be None")
        if expire and not isinstance(expire, int):
            raise TypeError("expire argument must be int")
        if pexpire and not isinstance(pexpire, int):
            raise TypeError("pexpire argument must be int")

        args = []
        expire and args.extend((b'EX', expire))
        pexpire and args.extend((b'PX', pexpire))

        if only_if_not_exists and only_if_exists:
            raise TypeError('only_if_not_exists and only_if_exists '
                            'cannot be true simultaneously')
        only_if_not_exists and args.append(b'NX')
        only_if_exists and args.append(b'XX')
        return self._conn.execute(b'SET', key, value, *args)

    def setbit(self, key, offset, value):
        """Sets or clears the bit at offset in the string value stored at key.

        :raises TypeError: if key is None
        :raises TypeError: if offset is not int
        :raises ValueError: if offset is less then 0 or value is not 0 or 1
        """
        if key is None:
            raise TypeError("key argument must not be None")
        if not isinstance(offset, int):
            raise TypeError("offset argument must be int")
        if offset < 0:
            raise ValueError("offset must be greater equal 0")
        if value not in (0, 1):
            raise ValueError("value argument must be either 1 or 0")
        return self._conn.execute(b'SETBIT', key, offset, value)

    def setex(self, key, seconds, value):
        """Set the value and expiration of a key.

        If seconds is float it will be multiplied by 1000
        coerced to int and passed to `psetex` method.

        :raises TypeError: if key is None
        :raises TypeError: if seconds is neither int nor float
        """
        if key is None:
            raise TypeError("key argument must not be None")
        if isinstance(seconds, float):
            return self.psetex(key, int(seconds * 1000), value)
        if not isinstance(seconds, int):
            raise TypeError("milliseconds argument must be int")
        fut = self._conn.execute(b'SETEX', key, seconds, value)
        return wait_ok(fut)

    def setnx(self, key, value):
        """Set the value of a key, only if the key does not exist.

        :raises TypeError: if key is None
        """
        if key is None:
            raise TypeError("key argument must not be None")
        fut = self._conn.execute(b'SETNX', key, value)
        return wait_convert(fut, bool)

    def setrange(self, key, offset, value):
        """Overwrite part of a string at key starting at the specified offset.

        :raises TypeError: if key is None
        :raises TypeError: if offset is not int
        :raises ValueError: if offset less then 0
        """
        if key is None:
            raise TypeError("key argument must not be None")
        if not isinstance(offset, int):
            raise TypeError("offset argument must be int")
        if offset < 0:
            raise ValueError("offset must be greater equal 0")
        return self._conn.execute(b'SETRANGE', key, offset, value)

    def strlen(self, key):
        """Get the length of the value stored in a key.

        :raises TypeError: if key is None
        """
        if key is None:
            raise TypeError("key argument must not be None")
        return self._conn.execute(b'STRLEN', key)