

def nega_to_dec(lst):
    """
    >>> nega_to_dec([0])
    0
    >>> nega_to_dec([1])
    1
    >>> nega_to_dec([1,0])
    -2
    >>> nega_to_dec([1,1])
    -1
    >>> nega_to_dec([1,0,0])
    4
    >>> nega_to_dec([1,0,1])
    5
    """

    d = 0
    p = 1
    for i in range(len(lst)-1,-1,-1):
        d += p*lst[i]
        p *= -2
    return d


def dec_to_nega(n):
    """
    >>> dec_to_nega(0)
    [0]
    >>> dec_to_nega(1)
    [1]
    >>> dec_to_nega(2)
    [1, 1, 0]
    """
    if n == 0:
        return [0]
    lst = []
    while n != 0:
        r = n % -2
        n = n // -2
        if r < 0:
            r += 2
            n += 1
        lst.append(r)
    return lst[::-1]


if __name__ == '__main__':
    import doctest
    doctest.testmod()
