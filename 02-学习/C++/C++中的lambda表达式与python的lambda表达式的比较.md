# lambda表达式的比较
## 1. 共同起点：lambda都是在创建“可调用对象”
- 链接[[程序设计中的可调用对象]] 
```python
square = lambda x: x * x
square(5) #25
```
```cpp
auto square = [](int x)->int { return x * x; }
square(5); //25
```
- 两个语法都是在定义一个没有名字的函数式对象，并把它绑定给变量square
- **差异：python的lambda更像是“表达式级匿名函数”；C++的lambda本质上会生成一个闭包类型的对象 

## 2. 闭包和环境捕获
```python
def make_adder(n):
	return lambda x: x + n
add3 = make_adder(3)
add3(10) #13
```
```cpp
auto make_adder(int n){
	return [n](int x) {
		return x + n;
	}
}
auto add3 = make_adder(3);
add3(10); //13
```
- **python的lambda会形成闭包，自动记住外层作用域中的n,C++也可以形成闭包,把捕获的外部变量存在闭包内部/形成一个指向外部变量的“指向”，但必须明确写出捕获方式(值捕获，引用捕获等)**
```cpp
[n]  //值捕获n,相当于生成了一个副本，内部修改不影响外部同名变量
[&n] //引用捕获n,内部修改时同时修改外部的n
[=]  //默认按值捕获用到的所有的外部变量
[&]  //默认按引用捕获用到的所有的外部变量
[this] //捕获当前对象指针，一般用于成员函数内部定义
```
### 2.1 捕获差异展现
#### 2.11Python的捕获特性
```python
funcs = []

for i in range(3):
	funcs.append(lambda: i)
	
print([f() for f in funcs]) #[2, 2, 2]
------------------------------------------------
for i in range(3):
	funcs.append(lambda:i)
i=10

print([f() for f in funcs]) #[10,10,10]
```
- 这里每一次append lambda的时候，相当于这个lambda对象捕获到了 i 本身(捕获的是变量的引用/绑定关系，而不是当时的值快照)，因为循环改动的是同一个 i ,并没有创建新的 i ，并不是保存了 i 的副本，所以最后print的时候，三个lambda指向到了同一个 i ，而这个 i 的值是2
- ==补充==: **这里的lambda : i 不是指当时保存了i的值，而是创建一个函数，等调用的时候返回i的值，而python的for循环的循环变量在循环结束后会保持最后一次迭代的值，在这个例子里i是在global frame里(循环在哪里，循环变量作用域就在哪里)，所以完全可以在循环结束后再改i的值**  
```python
funcs = []

for i in range(3):
	funcs.append(lambda i=i: i) # funcs.append(lambda x=i:x)

print([f() for f in funcs]) #[0, 1, 2]
```
- 这里写成lambda x=i:x更直观，是把当时的i的值保存在闭包内，绑定给x，<font color="#000000">调用的时候</font>就返回x的值
#### 2.12 C++的捕获特性
**针对C++，我们可以手动区分值捕获和引用捕获，因此不会像python那样混乱**
- 对于上述python的lambda : i,有以下类似的C++形式
```cpp
std::vector<std::function<int()>> funcs;
int i=0;

for(;i<3;i++){
	funcs.push_back([&i]()->int{
		return i;
	});
for(auto f:funcs){
	std::cout<<f(); //3,3,3 因为在i=3的时候跳出循环
}
```
- 这个就非常好理解了，引用捕获外部变量i, 等到调用的时候在返回现在i的值
```cpp
for(;i<3;i++){
	funcs.push_back([i]()->int{
		return i;
	});
//0,1,2
}
```
- 这里就是值捕获，捕获的是当时的值快照
