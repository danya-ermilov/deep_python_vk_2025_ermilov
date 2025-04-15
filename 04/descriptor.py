from abc import ABC, abstractmethod


class Base(ABC):
    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name, None)

    def __set__(self, instance, value):
        if self._validate(value):
            setattr(instance, self.name, value)
        else:
            raise ValueError(f"Not the correct type for {self.name[1:]}")

    @abstractmethod
    def _validate(self, value):
        raise NotImplementedError("Need to redefine")


class Integer(Base):
    def _validate(self, value):
        return isinstance(value, int)


class Double(Base):
    def _validate(self, value):
        return isinstance(value, float)


class String(Base):
    def _validate(self, value):
        return isinstance(value, str)


class Example:
    integer = Integer()
    string = String()
    double = Double()

    def __init__(self, integ, double, string):
        self.integer = integ
        self.double = double
        self.string = string
