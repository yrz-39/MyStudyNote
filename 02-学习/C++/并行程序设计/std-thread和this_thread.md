# std::thread和std::this_thread
## 1. std::thread 是什么，用来干什么
- 定义：std::thread 是C++标准库中用来**创建**和**管理线程**的类，定义在头文件`<thread>`中
> std::thread可以让程序在主线程(main) 之外，再开一个路线，让两个任务同时运行

比如正常程序是:
```text
main()一行行往下执行，哪怕中间有多个函数跳转，也是顺序执行
```
使用std::thread后就可以:
```text
main()往下执行
同时子函数func()执行别的逻辑
```
- 适用场景: 并发执行，后台任务，提高响应性
- 不适合的场景: 任务很小，管理成本高，共享数据太多

## 2. 最小例子，创建一个线程
```cpp
#include<iostream>
#include<thread>

void download(){
	std::cout<<"正在下载"<< std::endl;
	std::cout<<"下载完成"<< std::endl;
}

int main(){
	std::cout<<"主线程开始"<<std::endl;
	
	std::thread t(download);
	t.join();
	
	std::cout<<"主线程结束"<<std::endl;
	return 0;
}
```
- 这里当创建线程`std::thread t(download)`的时候,子线程就开始运行了,然后`t.join()`表示主线程等待子线程结束后再继续执行(例如主线程需要子线程的运行结果)
## 3.线程对象的生命周期
>关于`join()`和`detach()`:
[[join 和 detach]]

## 4.线程函数的传参方式
`std::thread`的基本形式是:
```cpp
std::thread t(函数名,参数1,参数2...);
```
例如:
```cpp
void func(int x){
	//
}

std::thread t(func,10);
t.join();
```
- 注意:thread是会创建一个对象,所以会把传入的参数保存到对象内部,然后在线程对象中调用函数,所以可以理解为==默认会复制传入的参数,也就是是传值==
--- 
### 4.1传值
```cpp
int a=10;
std::thread t(func,a);
```
这里a会被复制一份传入线程,也就是子线程中对a的处理不会影响主线程中的a
同时如果之后修改a,线程里a也不变
### 4.2传引用: std::ref
如果希望线程函数修改外部变量,要用如下方法:
```cpp
void func(int& x){
	x++;
}

int a=10;

std::thread t(func,std::ref(a));
j.join();
```
- 注:也可以传只读引用 `std::cref()`同时函数形参类型要改成const&

### 4.3 传移动对象
- 这个主要是针对一些不能被复制的对象,比如`std::unique_ptr`
所以要写:
```cpp
std::unique_ptr ptr=std::make_unique<int>(100);
std::thread t(func,std::move(ptr));
```

### 4.4 lambda作为线程函数
- 这里就很容易区分是传值还是传引用,只需要修改lambda的捕获列表即可
```cpp
int a=10;

std::thread t([a](){
	//
});

std::thread t([&a](){
	a++;
});
```

### 4.5 传成员函数(待整理)
## 5. 简单说一下std::this_thread
- 主要是几个常用api的使用
	- get_id(),返回当前运行线程的id,用来区分不同线程
	- yield(),让出CPU,告诉操作系统,现在这个线程可以停一下,让别的线程先运行,但不一定会跳到别的线程
	- sleep_for(),让当前线程停止一定时间,如：
	 `std::this_thread::sleep_for(std::chrono::seconds(2));`停止两秒
	- sleep_until(),暂停到某个具体的时间点





