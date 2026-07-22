# 互斥锁mutex
## 1.为什么需要互斥锁？
>[[数据竞争与临界区]]中提到，当两个线程同时修改同一个变量的时候，可能会造成数据竞争，从而造成错误

- 因此互斥锁的作用就是：再**同一时刻保证只能有一个线程进入临界区**来修改变量，也就是“==谁先拿到锁，谁执行，下一个只能等解锁后才能重新拿锁==”

## 2.基本写法
```cpp
#include<mutex>
#include<thread>

int counter=0;
std::mutex mtx;

void add(){
	for(int i=0;i<10000;i++){
		mtx.lock();
		counter++;
		mtx.unlock();
	}
}

int main(){
	std::thread t1(add);
	std::thread t2(add);
	
	t1.join();
	t2.join();
	
	std::cout<<counter;
}
```
这里用`mtx.lock()`和`mtx.unlock()`手动加锁解锁，保证同一时刻只有一个进程修改counter
- 但是手动加锁解锁不太适合复杂的情况:
	1. 如果代码提前return但是忘记解锁，就**死锁**了
	2. 如果代码抛出异常，也会**死锁**
所以可以用**std::lock_guard**解决
## 3.std::lock_guard
基本写法就是:
```cpp
void add(){
	for(int i=0;i<100000;i++){
		std::lock_guard<std::mutex> lock(mtx);
		counter++;
	}
}
```
这里的:
```cpp
std::lock_guard<std::mutex> lock(mtx);
```
意思是：
- 创建lock对象时，自动调用`mtx.lock()`
- 离开作用域时，自动调用`mtx.unlock()`
- 作用域一般都是函数作用域，也就是子线程执行的函数