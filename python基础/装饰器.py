# 普通函数装饰器(不加参数)

def outer(f):
    def inner():
        print("---装饰器---")
        f()

    return inner


@outer
def func():
    print('-我是函数主体-')


func()
print('1*************************************')

# 普通函数装饰器(加参数)

def outer(*args,**kwargs):
    def middle(f):

    # print('---middle---')
        def inner():

            print('--inner--')
            f()
            print(args)
            return f
        return inner
    return middle

@outer('jacky')
def func():
    print('函数体')

func()

print('2*************************************')

#类装饰器,不加参数
class Outer():
    def __init__(self,f):
        self.f=f

    def __call__(self, *args, **kwargs):
        print('--装饰器--')
        self.f()
        # return self.f
@Outer
def fun():
    print('函数体')

fun()

print('3***********************************')

#类装饰器,加参数
class Outer():
    def __init__(self,level,**kwargs):
        self.level=level

    def __call__(self, f):
        def inner():
            print('--装饰器--')
            print(self.level)
            f()
        return inner

@Outer(level='V1')
def fun():
    print('函数体')

fun()
