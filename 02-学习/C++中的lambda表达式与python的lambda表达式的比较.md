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
```python
funcs = []

for i in range(3):
	funcs.append(lambda: i)
	
print([f() for f in funcs]) #[2, 2, 2]
```
- 这里每一次append lambda的时候，相当于把这个lambda对象做了一个到 i 的指向，因为循环改动的是同一个 i ,并没有创建新的 i ，并不是保存了 i 的副本，所以最后print的时候，三个lambda指向到了同一个 i ，而这个 i 的值是2
```python
funcs = []

for i in range(3):
	funcs.append(lambda i: i)

print([f() for f in funcs]) #[0, 1, 2]
```
- 这里