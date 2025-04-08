from abc import ABC, abstractmethod


class Base(ABC):
    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, instanse, owner):
        return getattr(instanse, self.name, None)

    def __set__(self, instance, value):
        if self._validate(value):
            setattr(instance, self.name, value)
        else:
            raise ValueError("Not the right type")

    @abstractmethod
    def _validate(self, value):
        raise NotImplementedError("Need to redefine")


class Integer(Base):
    def _validate(self, value):
        return isinstance(value, int)


class Float(Base):
    def _validate(self, value):
        return isinstance(value, float)


class String(Base):
    def _validate(self, value):
        return isinstance(value, str)


class Example:
    integer = Integer()
    string = String()
    float = Float()

    def __init__(self, integ, float, string):
        self.integer = integ
        self.float = float
        self.string = string


a = Example(3, 4.5, "asd")

# a.integ = 1.9

print(a.__dict__)
