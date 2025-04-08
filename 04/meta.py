class CustomMeta(type):
    def __new__(mcs, name, bases, namespace):
        custom_namespace = {}

        for attr_name, attr_value in namespace.items():
            if not attr_name.startswith('__'):
                custom_namespace[f'custom_{attr_name}'] = attr_value
            else:
                custom_namespace[attr_name] = attr_value

        cls = super().__new__(mcs, name, bases, custom_namespace)

        def my_setattr(instance, name, value):
            if not name.startswith('__') and not name.startswith('custom_'):
                super(cls, instance).__setattr__(f'custom_{name}', value)
            else:
                super(cls, instance).__setattr__(name, value)

        cls.__setattr__ = my_setattr

        return cls


class CustomClass(metaclass=CustomMeta):
    x = 50

    def __init__(self, val=99):
        self.val = val

    def line(self):
        return 100

    def __str__(self):
        return "Custom_by_metaclass"
