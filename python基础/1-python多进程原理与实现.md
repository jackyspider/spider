#### 1  进程的基本概念

什么是进程？

​	进程就是一个程序在一个数据集上的一次动态执行过程。进程一般由程序、数据集、进程控制块三部分组成。我们编写的程序用来描述进程要完成哪些功能以及如何完成；数据集则是程序在执行过程中所需要使用的资源；进程控制块用来记录进程的外部特征，描述进程的执行变化过程，系统可以利用它来控制和管理进程，它是系统感知进程存在的唯一标志。

进程的生命周期:创建(New),就绪(Runnable),运行(Running),阻塞(Block),销毁(Destroy)

进程的状态/分类:(Actived)活动进程,可见进程(Visiable),后台进程(Background),服务进程(Service),空进程



进程是一个动态的实体，从创建到消亡，是一个进程的整个生命周期。进程可能会经历各种不同的状态，一般来说有三种状态。
\+ 就绪态： 进程已经获得了除cpu以外的所有其它资源，在就绪队列中等待cpu调度
\+ 执行状态： 已经获得cpu以及所有需要的资源正在运行
\+ 阻塞状态(等待状态)： 进程因等待所需要的资源而放弃处理器，或者进程本来就不拥有处理器，且其它资源也没有满足

状态转换： 就绪态的进程得到cpu调度就会变为执行状态，执行态的进程如果因为休眠或等待某种资源就会变为等待状态，执行态的进程如果时间片到了就会重新变为就绪状态放入就绪队列末尾，等待状态的进程如果得到除cpu以外的资源就会变为就绪状态

注意处于等待状态的进程不能直接转变为执行状态，而首先要变为就绪状态，哪怕系统中只有一个进程



#### 2  父进程和子进程

​     Linux 操作系统提供了一个 fork() 函数用来创建子进程，这个函数很特殊，调用一次，返回两次，因为操作系统是将当前的进程（父进程）复制了一份（子进程），然后分别在父进程和子进程内返回。子进程永远返回0，而父进程返回子进程的 PID。我们可以通过判断返回值是不是 0 来判断当前是在父进程还是子进程中执行。

​    在 Python 中同样提供了 fork() 函数，此函数位于 os 模块下。

```
# -*- coding: utf-8 -*-  
__author__ = 'zhougy'
__date__ = '2018/5/31 下午5:17' 

import os
import time

print("在创建子进程前: pid=%s, ppid=%s" % (os.getpid(), os.getppid()))

pid = os.fork()
if pid == 0:
    print("子进程信息： pid=%s, ppid=%s" % (os.getpid(), os.getppid()))
    time.sleep(5)
else:
    print("父进程信息: pid=%s, ppid=%s" % (os.getpid(), os.getppid()))
    # pid表示回收的子进程的pid
    #pid, result = os.wait()  # 回收子进程资源　　阻塞
    time.sleep(5)
    #print("父进程：回收的子进程pid=%d" % pid)
    #print("父进程：子进程退出时 result=%d" % result)

# 下面的内容会被打印两次，一次是在父进程中，一次是在子进程中。
# 父进程中拿到的返回值是创建的子进程的pid，大于0
print("fork创建完后: pid=%s, ppid=%s" % (os.getpid(), os.getppid()))
```



##### 2.1 父子进程如何区分?

​    子进程是父进程通过fork()产生出来的，pid = os.fork()

​    通过返回值pid是否为0，判断是否为子进程，如果是0，则表示是子进程

​    由于 fork() 是 Linux 上的概念，所以如果要跨平台，最好还是使用 subprocess 模块来创建子进程。



##### 2.2 子进程如何回收？

python中采用os.wait()方法用来回收子进程占用的资源

pid, result = os.wait()  # 回收子进程资源　　阻塞，等待子进程执行完成回收

如果有子进程没有被回收的，但是父进程已经死掉了，这个子进程就是僵尸进程。



#### 3  Python进程模块

​     python的进程multiprocessing模块有多种创建进程的方式，每种创建方式和进程资源的回收都不太相同，下面分别针对Process,Pool及系统自带的fork三种进程分析。

##### 3.1  fork()

```
import os
pid = os.fork() # 创建一个子进程
os.wait() # 等待子进程结束释放资源
pid为0的代表子进程。
```

缺点：
​    1.兼容性差，只能在类linux系统下使用，windows系统不可使用；
​    2.扩展性差，当需要多条进程的时候，进程管理变得很复杂；
​    3.会产生“孤儿”进程和“僵尸”进程，需要手动回收资源。
优点：
​    是系统自带的接近低层的创建方式，运行效率高。



##### 3.2 **Process进程**

multiprocessing模块提供Process类实现新建进程

```
# -*- coding: utf-8 -*-
import os
from multiprocessing  import Process
import time

def fun(name):
	print("2 子进程信息： pid=%s, ppid=%s" % (os.getpid(), os.getppid()))
	print("hello " + name)
	

def test():
	print('ssss')


if __name__ == "__main__":
	print("1 主进程信息： pid=%s, ppid=%s" % (os.getpid(), os.getppid()))
	ps = Process(target=fun, args=('jingsanpang', ))
	print("111 ##### ps pid: " + str(ps.pid) + ", ident:" + str(ps.ident))
	print("3 进程信息： pid=%s, ppid=%s" % (os.getpid(), os.getppid()))
	print(ps.is_alive())
	ps.start()
	print(ps.is_alive())
	print("222 #### ps pid: " + str(ps.pid) + ", ident:" + str(ps.ident))
	print("4 进程信息： pid=%s, ppid=%s" % (os.getpid(), os.getppid()))
	ps.join()
	print(ps.is_alive())
	print("5 进程信息： pid=%s, ppid=%s" % (os.getpid(), os.getppid()))
	ps.terminate()
	print("6 进程信息： pid=%s, ppid=%s" % (os.getpid(), os.getppid()))
```

**特点：**
​    1.注意：Process对象可以创建进程，但Process对象不是进程，其删除与否与系统资源是否被回收没有直接的关系。
   2.主进程执行完毕后会默认等待子进程结束后回收资源，不需要手动回收资源；join()函数用来控制子进程
​    结束的顺序,其内部也有一个清除僵尸进程的函数，可以回收资源；
   3.Process进程创建时，子进程会将主进程的Process对象完全复制一份，这样在主进程和子进程各有一个    Process对象，但是p.start()启动的是子进程，主进程中的Process对象作为一个静态对象存在，不执行。

   4.当子进程执行完毕后，会产生一个僵尸进程，其会被join函数回收，或者再有一条进程开启，start函数也会回收僵尸进程，所以不一定需要写join函数。
   5.windows系统在子进程结束后会立即自动清除子进程的Process对象，而linux系统子进程的Process对象如果没有join函数和start函数的话会在主进程结束后统一清除。

另外还可以通过继承Process对象来重写run方法创建进程



##### 3.3  进程池POOL (多个进程)

```
# -*- coding: utf-8 -*-
__author__ = 'zhougy'
__date__ = '2018/5/31 下午9:16'

import multiprocessing
import time

def work(msg):
	mult_proces_name = multiprocessing.current_process().name
	print('process: ' + mult_proces_name + '-' + msg)
	

if __name__ == "__main__":
	pool = multiprocessing.Pool(processes=4) # 创建4个进程
	for i in range(20):
		msg = "process %d" %(i)
		pool.apply_async(work, (msg, ))#异步
	pool.close() # 关闭进程池，表示不能在往进程池中添加进程
	pool.join() # 等待进程池中的所有进程执行完毕，必须在close()之后调用
	print("Sub-process all done.")
```

​     上述代码中的`pool.apply_async()`是`apply()`函数的变体，`apply_async()`是`apply()`的并行版本，`apply()`是`apply_async()`的阻塞版本，使用`apply()`主进程会被阻塞直到函数执行结束，所以说是阻塞版本。`apply()`既是`Pool`的方法，也是Python内置的函数，两者等价。可以看到输出结果并不是按照代码for循环中的顺序输出的。



多个子进程并返回值

`      apply_async()`本身就可以返回被进程调用的函数的返回值。上一个创建多个子进程的代码中，如果在函数`func`中返回一个值，那么`pool.apply_async(func, (msg, ))`的结果就是返回pool中所有进程的**值的对象（注意是对象，不是值本身）**。

```
import multiprocessing
import time

def func(msg):
    return multiprocessing.current_process().name + '-' + msg

if __name__ == "__main__":
    pool = multiprocessing.Pool(processes=4) # 创建4个进程
    results = []
    for i in range(20):
        msg = "process %d" %(i)
        results.append(pool.apply_async(func, (msg, )))
    pool.close() # 关闭进程池，表示不能再往进程池中添加进程，需要在join之前调用
    pool.join() # 等待进程池中的所有进程执行完毕
    print ("Sub-process(es) done.")

    for res in results:
        print (res.get())
```

​     与之前的输出不同，这次的输出是有序的。

​     如果电脑是八核，建立8个进程，在Ubuntu下输入top命令再按下大键盘的1，可以看到每个CPU的使用率是比较平均的



#### 4  进程间通信方式

1. 管道pipe(全双工True,半双工False)：管道是一种半双工的通信方式，数据只能单向流动，而且只能在具有亲缘关系的进程间使用。进程的亲缘关系通常是指父子进程关系。 
2. 命名管道FIFO：有名管道也是半双工的通信方式，但是它允许无亲缘关系进程间的通信。
3. 消息队列MessageQueue：消息队列是由消息的链表，存放在内核中并由消息队列标识符标识。消息队列克服了信号传递信息少、管道只能承载无格式字节流以及缓冲区大小受限等缺点。
4. 共享存储SharedMemory：共享内存就是映射一段能被其他进程所访问的内存，这段共享内存由一个进程创建，但多个进程都可以访问。共享内存是最快的 IPC 方式，它是针对其他进程间通信方式运行效率低而专门设计的。它往往与其他通信机制，如信号两，配合使用，来实现进程间的同步和通信。



以上几种进程间通信方式中，消息队列是使用的比较频繁的方式。

（1）管道pipe**

```
import multiprocessing

def foo(sk):
   sk.send('hello father')
   print(sk.recv())

if __name__ == '__main__':
   conn1,conn2=multiprocessing.Pipe()    #开辟两个口，都是能进能出，括号中如果False即单向通信
   p=multiprocessing.Process(target=foo,args=(conn1,))  #子进程使用sock口，调用foo函数
   p.start()
   print(conn2.recv())  #主进程使用conn口接收
   conn2.send('hi son') #主进程使用conn口发送
```



（2）消息队列Queue

Queue是多进程的安全队列，可以使用Queue实现多进程之间的数据传递。

Queue的一些常用方法：

- Queue.qsize()：返回当前队列包含的消息数量；
- Queue.empty()：如果队列为空，返回True，反之False ；
- Queue.full()：如果队列满了，返回True,反之False；
- Queue.get():获取队列中的一条消息，然后将其从列队中移除，可传参超时时长。
- Queue.get_nowait()：相当Queue.get(False),取不到值时触发异常：Empty；
- Queue.put():将一个值添加进数列，可传参超时时长。
- Queue.put_nowait():相当于Queue.get(False),当队列满了时报错：Full。

案例：

```
from multiprocessing import Process, Queue
import time


def write(q):
   for i in ['A', 'B', 'C', 'D', 'E']:
      print('Put %s to queue' % i)
      q.put(i)
      time.sleep(0.5)


def read(q):
   while True:
      v = q.get(True)
      print('get %s from queue' % v)


if __name__ == '__main__':
   q = Queue()
   pw = Process(target=write, args=(q,))
   pr = Process(target=read, args=(q,))
   print('write process = ', pw)
   print('read  process = ', pr)
   pw.start()
   pr.start()
   pw.join()
   pr.join()
   pr.terminate()
   pw.terminate()

```



Queue和pipe只是实现了数据交互，并没实现数据共享，即一个进程去更改另一个进程的数据**。**

注：进程间通信应该尽量避免使用共享数据的方式





#### 5   多进程实现生产者消费者

以下通过多进程实现生产者，消费者模式

```
import multiprocessing
from multiprocessing import Process
from time import sleep
import time


class MultiProcessProducer(multiprocessing.Process):
   def __init__(self, num, queue):
      """Constructor"""
      multiprocessing.Process.__init__(self)
      self.num = num
      self.queue = queue

   def run(self):
      t1 = time.time()
      print('producer start ' + str(self.num))
      for i in range(1000):
         self.queue.put((i, self.num))
      # print 'producer put', i, self.num
      t2 = time.time()

      print('producer exit ' + str(self.num))
      use_time = str(t2 - t1)
      print('producer ' + str(self.num) + ', 
      use_time: '+ use_time)



class MultiProcessConsumer(multiprocessing.Process):
   def __init__(self, num, queue):
      """Constructor"""
      multiprocessing.Process.__init__(self)
      self.num = num
      self.queue = queue

   def run(self):
      t1 = time.time()
      print('consumer start ' + str(self.num))
      while True:
         d = self.queue.get()
         if d != None:
            # print 'consumer get', d, self.num
            continue
         else:
            break
      t2 = time.time()
      print('consumer exit ' + str(self.num))
      print('consumer ' + str(self.num) + ', use time:' + str(t2 - t1))


def main():
   # create queue
   queue = multiprocessing.Queue()

   # create processes
   producer = []
   for i in range(5):
      producer.append(MultiProcessProducer(i, queue))

   consumer = []
   for i in range(5):
      consumer.append(MultiProcessConsumer(i, queue))

   # start processes
   for i in range(len(producer)):
      producer[i].start()

   for i in range(len(consumer)):
      consumer[i].start()

   # wait for processs to exit
   for i in range(len(producer)):
      producer[i].join()

   for i in range(len(consumer)):
      queue.put(None)

   for i in range(len(consumer)):
      consumer[i].join()

   print('all done finish')


if __name__ == "__main__":
   main()
```



#### 6  总结

​    python中的多进程创建有以下两种方式：

   （1）fork子进程

   （2）采用 **multiprocessing** 这个库创建子进程

​     需要注意的是队列中Queue.Queue是线程安全的，但并不是进程安全，所以多进程一般使用线程、进程安全的multiprocessing.Queue()

​     另外, 进程池使用 multiprocessing.Pool实现，pool = multiprocessing.Pool(processes = 3)，产生一个进程池，pool.apply_async实现非租塞模式，pool.apply实现阻塞模式。

 apply_async和 apply函数，前者是非阻塞的，后者是阻塞。可以看出运行时间相差的倍数正是进程池数量。

​    同时可以通过result.append(pool.apply_async(func, (msg, )))获取非租塞式调用结果信息的。





