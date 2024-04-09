class MyClass:
    def __init__(self, value, env):
        self.value = value
        # self.env = env
        env.setTest(genFunc(self.my_method))

    def setMethod(self):
        self.env.setTest(self.my_method)

    def my_method(self, parameter):
        print("My value is:", self.value)
        print("Parameter passed:", parameter)


def genFunc(func):
    return func


class Env:
    def __init__(self, test) -> None:
        self.test = test
        pass

    def setTest(self, method):
        self.test.exe = method

    pass


class Test:
    def __init__(self) -> None:
        self.exe = None
        pass


def run():
    e = Env(Test())
    a = MyClass(21, e)
    e.test.exe("tt")


run()
