# std::thread
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





