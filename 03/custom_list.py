class CustomList(list):
    def __add__(self, other):
        if isinstance(other, int):
            other = [other] * len(self)
        result = CustomList()
        max_len = max(len(self), len(other))
        for i in range(max_len):
            val_self = self[i] if i < len(self) else 0
            val_other = other[i] if i < len(other) else 0
            result.append(val_self + val_other)
        return result

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        negative_other = [-x for x in other] if isinstance(other, (CustomList, list)) else -1 * other
        return self.__add__(negative_other)

    def __rsub__(self, other):
        negative_self = [-x for x in self]
        return CustomList(negative_self).__add__(other)

    def __lt__(self, other):
        if not isinstance(other, (list, CustomList)):
            raise TypeError("Можно сравнивать только с list или CustomList")
        return sum(self) < sum(other)

    def __gt__(self, other):
        if not isinstance(other, (list, CustomList)):
            raise TypeError("Можно сравнивать только с list или CustomList")
        return sum(self) > sum(other)

    def __le__(self, other):
        if not isinstance(other, (list, CustomList)):
            raise TypeError("Можно сравнивать только с list или CustomList")
        return sum(self) <= sum(other)

    def __ge__(self, other):
        if not isinstance(other, (list, CustomList)):
            raise TypeError("Можно сравнивать только с list или CustomList")
        return sum(self) >= sum(other)

    def __eq__(self, other):
        if not isinstance(other, (list, CustomList)):
            raise TypeError("Можно сравнивать только с list или CustomList")
        return sum(self) == sum(other)

    def __ne__(self, other):
        if not isinstance(other, (list, CustomList)):
            raise TypeError("Можно сравнивать только с list или CustomList")
        return sum(self) != sum(other)

    def __str__(self):
        elements = ", ".join(map(str, self))
        total = sum(self)
        return f"Элементы: {elements}\nСумма: {total}"


if __name__ == "__main__":
    lst1 = CustomList([2, 4])
    lst2 = [1, 3]
    final_lst = lst2 + lst1
    a = lst1 - 1
    print(a, type(a))
