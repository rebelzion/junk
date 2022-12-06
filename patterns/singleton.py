
"""
Implementing the Singleton pattern using Singleton class
where the instance and state are the same.
"""
class Singleton:

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance

    @classmethod
    def get_instance(cls):
        return cls.instance

    def __str__(self):
        return str(self.__dict__)

shared_state = Singleton()
shared_state.v = "v"
another_state = Singleton()

print("Singleton using a class\n" + "-" * 100)
print(f"Is shared_state the same as another_state?", shared_state is another_state)
print(f"{shared_state.v=}")
print(f"{another_state.v=}")
print()

"""
Implementing the Singleton pattern using Borg Singleton
where different instances share the same state.
"""

class BorgSingleton:
    _shared_state = {}

    def __new__(cls, *args, **kwargs):
        obj = super(BorgSingleton, cls).__new__(cls, *args, **kwargs)
        obj.__dict__ = cls._shared_state
        return obj

class BorgChild(BorgSingleton):
    pass


borg = BorgSingleton()
borg.shared_variable = "v"

child_borg = BorgChild()
print("Singleton using a Borg class\n" + "-" * 100)
print(f"Is borg the same as child_borg?", borg is child_borg)
print(f"{borg.shared_variable=}")
print(f"{child_borg.shared_variable=}")
print()


s = """
When to use Singleton ?
- when managing a database connection
- file manager
- logger
"""
print(s)


