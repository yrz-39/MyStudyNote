# 附录：考前自测题

> 配套《高级程序设计（C++）期末冲刺复习文档》。题目来自课程 PPT 代码与冲刺文档考点的改编，与冲刺文档正文中的例题**不重复**，可作为独立的实战自测。
>
> 共 **10 道程序分析题 + 10 道程序纠错题 + 5 道手写代码题**。建议**先合上答案做完全部题目**，再翻到后半部分对照"答案与解析"。所有程序分析题的预期输出均已通过编译运行核对。

---

# 第一部分　题目

## 一、程序分析题（10 题）
> 要求：写出程序输出 / 调用顺序 / 被调用的函数，并能说明理由。

### 分析题 A1
```cpp
#include <iostream>
using namespace std;
class X { public: X(){ cout<<"X()"<<endl; } ~X(){ cout<<"~X()"<<endl; } };
class Y { public: Y(){ cout<<"Y()"<<endl; } ~Y(){ cout<<"~Y()"<<endl; } };
class Z {
    X x;                       // 先声明
    Y y;                       // 后声明
public:
    Z() : y(), x() { cout<<"Z()"<<endl; }   // 注意初始化表写的是 y 在前、x 在后
    ~Z() { cout<<"~Z()"<<endl; }
};
int main() {
    Z z;
    return 0;
}
```
**问**：写出完整输出。初始化表里 `y()` 写在 `x()` 前面，会改变成员的构造顺序吗？

### 分析题 A2
```cpp
#include <iostream>
using namespace std;
class Animal {
public:
    virtual void sound() { cout<<"Animal"<<endl; }
    void name() { cout<<"animal"<<endl; }
};
class Dog : public Animal {
public:
    void sound() { cout<<"Dog"<<endl; }
    void name() { cout<<"dog"<<endl; }
};
void test(Animal &a) { a.sound(); a.name(); }
int main() {
    Animal an;
    Dog d;
    test(an);
    test(d);
    return 0;
}
```
**问**：写出输出。`test` 用的是**引用**参数，`sound()` 和 `name()` 分别调用谁？为什么不同？

### 分析题 A3
```cpp
#include <iostream>
using namespace std;
class T {
    int id;
public:
    T(int i)        { id = i; cout<<"ctor "<<id<<endl; }
    T(const T &t)   { id = t.id; cout<<"copy "<<id<<endl; }
    ~T()            { cout<<"dtor "<<id<<endl; }
};
void use(T t) { }              // 值参数
int main() {
    T a(1);
    T b(a);
    use(a);
    return 0;
}
```
**问**：写出完整输出。共发生几次拷贝构造？分别由什么触发？

### 分析题 A4
```cpp
#include <iostream>
using namespace std;
class Base {
    int a;
public:
    Base() { a = 0; }
    Base& operator=(const Base &b) { a = b.a; cout<<"Base="<<endl; return *this; }
    void seta(int v) { a = v; }
    int  geta() const { return a; }
};
class Derived : public Base {
    int b;
public:
    Derived() { b = 0; }
    Derived& operator=(const Derived &d) {
        if (this == &d) return *this;
        Base::operator=(d);
        b = d.b;
        cout<<"Derived="<<endl;
        return *this;
    }
    void setb(int v) { b = v; }
    int  getb() const { return b; }
};
int main() {
    Derived d1, d2;
    d1.seta(5); d1.setb(7);
    d2 = d1;
    cout << d2.geta() << " " << d2.getb() << endl;
    return 0;
}
```
**问**：写出输出。若把 `Derived::operator=` 中的 `Base::operator=(d);` 删掉，最后一行输出会变成什么？

### 分析题 A5
```cpp
#include <iostream>
#include <memory>
using namespace std;
int main() {
    weak_ptr<int> w;
    {
        shared_ptr<int> s(new int(42));
        w = s;
        cout << w.use_count() << endl;
        cout << w.expired()   << endl;
        shared_ptr<int> p = w.lock();
        cout << w.use_count() << endl;
    }
    cout << w.expired() << endl;
    shared_ptr<int> q = w.lock();
    cout << (q == nullptr) << endl;
    return 0;
}
```
**问**：写出 5 行输出（`bool` 按 0/1 打印）。`weak_ptr` 会增加引用计数吗？`lock()` 在对象已释放后返回什么？

### 分析题 A6
```cpp
#include <iostream>
using namespace std;
class Counter {
    int v;
public:
    Counter(int x = 0) { v = x; }
    Counter& operator++()        { v++; return *this; }              // 前置
    const Counter operator++(int){ Counter t = *this; v++; return t; } // 后置
    int get() const { return v; }
};
int main() {
    Counter a(5), b, c;
    b = ++a;
    cout << a.get() << " " << b.get() << endl;
    c = a++;
    cout << a.get() << " " << c.get() << endl;
    return 0;
}
```
**问**：写出输出。前置与后置 `++` 的返回值有何区别？

### 分析题 A7
```cpp
#include <iostream>
using namespace std;
class Widget {
    static int count;
public:
    Widget()  { count++; }
    ~Widget() { count--; }
    static int getCount() { return count; }
};
int Widget::count = 0;
int main() {
    Widget a;
    cout << Widget::getCount() << endl;
    {
        Widget b, c;
        cout << Widget::getCount() << endl;
    }
    cout << Widget::getCount() << endl;
    Widget *p = new Widget;
    cout << Widget::getCount() << endl;
    delete p;
    cout << Widget::getCount() << endl;
    return 0;
}
```
**问**：写出 5 行输出。`count` 为什么所有对象共享一份？

### 分析题 A8
```cpp
#include <iostream>
using namespace std;
void f(int sel) {
    if (sel == 0) throw 3.14;    // double
    if (sel == 1) throw 42;      // int
    throw 'x';                   // char
}
void g(int sel) {
    try { f(sel); }
    catch (int e)    { cout << "int " << e << endl; }
    catch (double e) { cout << "double " << e << endl; }
    catch (...)      { cout << "other" << endl; }
}
int main() {
    g(0);
    g(1);
    g(2);
    return 0;
}
```
**问**：写出输出。`g(2)` 抛出的 `char` 为什么落到 `catch(...)`？

### 分析题 A9
```cpp
#include <iostream>
using namespace std;
class Date {
    int year;
public:
    Date(int y) { year = y; }
    int  getYear() const { return year; }
    void setYear(int y)  { year = y; }
};
void show(const Date &d) {
    cout << d.getYear() << endl;
    // d.setYear(2000);   // 这一行若取消注释会怎样？
}
int main() {
    Date d(2024);
    show(d);
    d.setYear(2025);
    cout << d.getYear() << endl;
    return 0;
}
```
**问**：写出输出。若取消 `show` 中 `d.setYear(2000);` 的注释会发生什么？为什么？

### 分析题 A10
```cpp
#include <iostream>
using namespace std;
class Array {
    int data[5];
public:
    Array() { for (int i = 0; i < 5; i++) data[i] = i; }
    int& operator[](int i) { return data[i]; }
};
int main() {
    Array a;
    a[2] = 100;
    cout << a[2] << endl;
    cout << a[0] << endl;
    return 0;
}
```
**问**：写出输出。`a[2] = 100;` 为什么能作为赋值的左边？`operator[]` 的返回类型起了什么作用？

---

## 二、程序纠错题（10 题）
> 要求：指出代码中的全部错误并改正，说明每处为什么错。（题干已给出代码"想要实现的目标"。）

### 纠错题 B1
**目标**：`Buffer` 管理一个动态 `int` 数组，要求拷贝、赋值后两对象互不影响，且析构不重复释放。
```cpp
class Buffer {
    int size;
    int *data;
public:
    Buffer(int n) { size = n; data = new int[n]; }
    ~Buffer() { delete[] data; }
    // 只有上面这些
};
```

### 纠错题 B2
**目标**：为含动态字符串的类实现正确的赋值运算符。
```cpp
#include <cstring>
class Str {
    char *p;
public:
    Str(const char *s) { p = new char[strlen(s) + 1]; strcpy(p, s); }
    Str& operator=(const Str &s) {
        p = new char[strlen(s.p) + 1];
        strcpy(p, s.p);
    }
    ~Str() { delete[] p; }
};
```

### 纠错题 B3
**目标**：通过基类指针 `delete` 派生类对象时，派生类自己申请的资源应被正确释放。
```cpp
class Shape {
public:
    Shape() { }
    ~Shape() { }
    virtual double area() { return 0; }
};
class Circle : public Shape {
    double *r;
public:
    Circle()  { r = new double(1.0); }
    ~Circle() { delete r; }
    double area() { return 3.14 * (*r) * (*r); }
};
// 使用：Shape *s = new Circle;  ...  delete s;
```

### 纠错题 B4
**目标**：派生类 `Derived` 的拷贝构造既要拷贝派生类成员，也要正确拷贝从基类继承的成员。
```cpp
class Base {
    int x;
public:
    Base() { x = 0; }
    Base(const Base &b) { x = b.x; }
};
class Derived : public Base {
    int y;
public:
    Derived() { y = 0; }
    Derived(const Derived &d) { y = d.y; }
};
```

### 纠错题 B5
**目标**：为类 `A` 重载 `new`/`delete`，分配时从系统堆申请，释放时归还系统堆。
```cpp
#include <cstdlib>
class A {
    int x;
public:
    int operator new(size_t size) {
        return malloc(size);
    }
    void operator delete(int p) {
        free(p);
    }
};
```

### 纠错题 B6
**目标**：把一个独占所有权的指针所管理的对象，转交给另一个指针。
```cpp
#include <memory>
int main() {
    std::unique_ptr<int> a(new int(1));
    std::unique_ptr<int> b = a;     // 想把所有权交给 b
    return 0;
}
```

### 纠错题 B7
**目标**：让两个智能指针共享同一个堆对象，引用计数应为 2，且只释放一次。
```cpp
#include <memory>
int main() {
    int *p = new int(5);
    std::shared_ptr<int> a(p);
    std::shared_ptr<int> b(p);
    return 0;
}
```

### 纠错题 B8
**目标**：`List` 与 `Node` 是组合关系——`Node` 由 `List` 内部创建、随 `List` 析构而销毁。
```cpp
struct Node { int value; };
class List {
    Node *head;
public:
    List()  { head = new Node; }
    ~List() { }
};
```

### 纠错题 B9
**目标**：两个线程并发地对共享计数器累加，结果应正确且确定，主线程要等子线程结束。
```cpp
#include <iostream>
#include <thread>
using namespace std;
int counter = 0;
void work() {
    for (int i = 0; i < 100000; i++)
        counter++;
}
int main() {
    thread t1(work);
    thread t2(work);
    cout << counter << endl;
    return 0;
}
```

### 纠错题 B10
**目标**：`Config` 含一个常量编号 `id`（构造时确定后不再修改）和一个普通成员 `value`。
```cpp
class Config {
    const int id;
    int value;
public:
    Config(int i) {
        id = i;
        value = 0;
    }
};
```

---

## 三、手写代码题（5 题）
> 要求：完整写出类或函数，可直接编译；注意得分点。

### 手写题 C1
定义一个管理动态 `int` 数组的类 `Vec`，内部用 `int *data` 和 `int size` 表示。要求写出能正确**深拷贝**的"四件套"：① 构造函数 `Vec(int n)`（分配 `n` 个元素并初始化为 0）；② 拷贝构造函数；③ 赋值运算符；④ 析构函数。

### 手写题 C2
写一个简易智能指针类模板 `ToyPtr<T>`：构造时接管一个 `new` 出来的堆指针，析构时自动 `delete`，并重载 `*` 与 `->`，使其能像普通指针一样使用。再写两三行 `main` 演示用法。

### 手写题 C3
用抽象基类 `Animal` 定义统一接口 `speak()`（纯虚函数），派生出 `Dog` 和 `Cat` 各自实现 `speak()`（分别输出 `Woof` 和 `Meow`）。再写一段代码：用 `Animal*` 数组存放一个 `Dog` 和一个 `Cat`，通过动态绑定调用各自的 `speak()`，最后正确释放。要求基类有合适的析构函数。

### 手写题 C4
为类 `A`（含两个 `int` 成员，且**没有**定义任何构造函数）重载 `operator new` 与 `operator delete`：用 `new A` 创建的动态对象内存被初始化为全 0，用 `delete` 释放时归还系统堆。写出类定义并简述用法。

### 手写题 C5
用类模板实现一个定长栈 `Stack<T>`（内部用数组 `T buffer[100]` 和 `int top`）。要求提供：构造函数（`top` 初始化为 -1）、`void push(const T &x)`、`void pop(T &x)`、`bool empty() const`。其中 `push`/`pop` 的实现写在类**外部**。再写两行 `main` 演示对 `int` 类型的使用。

---
---

# 第二部分　答案与解析

## 一、程序分析题答案

### A1 答案
```
X()
Y()
Z()
~Z()
~Y()
~X()
```
**解析**：成员对象的构造顺序只由**声明顺序**决定，与初始化表书写顺序无关。`x` 先声明 → 先构造（`X()`），`y` 后声明 → 后构造（`Y()`），最后执行 `Z` 的构造体（`Z()`）。析构严格逆序：`~Z()` → `~Y()` → `~X()`。所以初始化表写 `y()` 在前**不会**改变构造顺序。

### A2 答案
```
Animal
animal
Dog
animal
```
**解析**：`test(Animal &a)` 用引用参数。`sound()` 是虚函数，通过引用调用 → **动态绑定**到实际对象类型：`test(an)` 调 `Animal::sound`、`test(d)` 调 `Dog::sound`。`name()` 不是虚函数 → **静态绑定**到引用的静态类型 `Animal`，两次都调 `Animal::name`（输出 `animal`）。要点：指针**和引用**都能触发动态绑定；非虚函数始终按静态类型。

### A3 答案
```
ctor 1
copy 1
copy 1
dtor 1
dtor 1
dtor 1
```
**解析**：`T a(1)` 调普通构造 → `ctor 1`。`T b(a)` 用对象初始化对象 → 拷贝构造 → `copy 1`。`use(a)` 形参是值参数，用 `a` 拷贝构造形参 → `copy 1`；函数返回时形参析构 → `dtor 1`。`main` 结束时按逆序析构 `b`、`a` → 两次 `dtor 1`。共发生 **2 次拷贝构造**：一次"对象初始化对象"，一次"对象作值参数"。

### A4 答案
```
Base=
Derived=
5 7
```
**解析**：`d2 = d1` 调 `Derived::operator=`：先自赋值检查（不等），再 `Base::operator=(d)` 赋值继承来的 `a`（输出 `Base=`），再赋值 `b`（输出 `Derived=`），返回 `*this`。所以 `a=5, b=7`。
**追问**：若删掉 `Base::operator=(d);`，基类成员 `a` 不会被赋值，仍是 `d2` 默认构造的 0，最后一行变成 **`0 7`**。这说明：派生类自定义赋值运算符**不会自动**调用基类赋值，必须显式调用。

### A5 答案
```
1
0
2
1
1
```
**解析**：
- `w = s` 后 `use_count()` 为 1（`weak_ptr` **不增加**引用计数，计数只来自 `s`）。
- `w.expired()` 此时为 `false` → 打印 `0`。
- `p = w.lock()` 得到一个共享所有权的 `shared_ptr`，计数变 2。
- 内层块结束，`s` 与 `p` 析构，对象计数归 0、被释放；`w.expired()` 变 `true` → 打印 `1`。
- `q = w.lock()` 在对象已释放后返回**空 `shared_ptr`**，`q == nullptr` 为真 → 打印 `1`。

### A6 答案
```
6 6
7 6
```
**解析**：`b = ++a`：前置 `++` 先自增（`a` 变 6）再返回 `*this`（自增后的 `a`），故 `b = 6`，输出 `6 6`。`c = a++`：后置 `++` 先保存旧值 `t`（6），再自增（`a` 变 7），返回旧值 `t`，故 `c = 6`、`a = 7`，输出 `7 6`。要点：前置返回自增**后**的对象引用，后置返回自增**前**的副本。

### A7 答案
```
1
3
1
2
1
```
**解析**：`count` 是**静态数据成员**，所有对象共享同一份。`a` 构造 → 1。内层 `b`、`c` 构造 → 3。内层块结束 `b`、`c` 析构 → 1。`new Widget` 构造 → 2。`delete p` 析构 → 1。静态成员属于类而非某个对象，故所有对象的构造/析构都改同一个 `count`。

### A8 答案
```
double 3.14
int 42
other
```
**解析**：`catch` 按类型精确匹配。`g(0)` 抛 `double(3.14)` → 命中 `catch(double)`。`g(1)` 抛 `int(42)` → 命中 `catch(int)`。`g(2)` 抛 `char('x')`，既不是 `int` 也不是 `double`，被**捕获所有类型**的 `catch(...)` 接住，输出 `other`。要点：`catch` 不会做隐式数值转换匹配；`catch(...)` 是兜底。

### A9 答案
```
2024
2025
```
**解析**：`show` 用 `const Date&`，只能调用**常成员函数**，`getYear()` 是 `const` 成员 → 合法，输出 2024。`main` 中 `d` 是普通对象，`setYear(2025)` 合法，再 `getYear()` 输出 2025。
**追问**：若取消 `d.setYear(2000);` 的注释 → **编译错误**。因为 `d` 是常量对象引用，而 `setYear` 不是常成员函数（会修改数据成员），常量对象不能调用非 `const` 成员函数。

### A10 答案
```
100
0
```
**解析**：`operator[]` 返回 `int&`（引用），所以 `a[2]` 是一个**左值**，`a[2] = 100;` 直接修改了 `data[2]`。随后 `a[2]` 读出 100，`a[0]` 仍是构造时赋的 0。要点：下标运算符返回**引用**才能既读又写；若返回 `int`（值）则不能作为赋值左边。

---

## 二、程序纠错题答案

### B1 答案
**错误**：只有构造和析构，**缺少拷贝构造函数和赋值运算符**。编译器生成的隐式版本是**浅拷贝**——两个对象的 `data` 指向同一块内存，会互相干扰、并在析构时被释放两次（double free）。
**改正**：补上深拷贝的拷贝构造与赋值运算符。
```cpp
class Buffer {
    int size;
    int *data;
public:
    Buffer(int n) { size = n; data = new int[n]; }
    Buffer(const Buffer &b) {                 // 深拷贝
        size = b.size;
        data = new int[size];
        for (int i = 0; i < size; i++) data[i] = b.data[i];
    }
    Buffer& operator=(const Buffer &b) {
        if (this == &b) return *this;
        delete[] data;
        size = b.size;
        data = new int[size];
        for (int i = 0; i < size; i++) data[i] = b.data[i];
        return *this;
    }
    ~Buffer() { delete[] data; }
};
```
**考试怎么答**：有裸指针成员的类，"拷贝构造 + 赋值 + 析构"必须配套实现深拷贝（三/五法则），否则浅拷贝会导致重复释放与互相干扰。

### B2 答案
**错误**：`operator=` 有三处问题——① 没有自赋值检查（`a=a` 时会先丢失再使用）；② 没有 `delete[]` 旧内存（内存泄漏）；③ 没有 `return *this`（无法链式赋值，且行为未定义）。
**改正**：
```cpp
Str& operator=(const Str &s) {
    if (this == &s) return *this;          // ① 自赋值检查
    delete[] p;                            // ② 释放旧空间
    p = new char[strlen(s.p) + 1];
    strcpy(p, s.p);
    return *this;                          // ③ 返回 *this
}
```
**考试怎么答**：自定义赋值运算符三要素——自赋值检查、先释放旧资源再分配新资源、返回 `*this`。

### B3 答案
**错误**：基类 `Shape` 的析构函数**不是虚函数**。`Shape *s = new Circle; delete s;` 时，按课程口径只会调用 `Shape::~Shape()`，不会调用 `Circle::~Circle()`，导致 `r` 指向的内存泄漏。（从标准 C++ 角度，通过基类指针 `delete` 没有虚析构的派生类对象属于未定义行为。）
**改正**：
```cpp
virtual ~Shape() { }      // 析构函数声明为虚函数
```
**考试怎么答**：凡是可能通过基类指针删除派生类对象的类，基类析构函数都应设为 `virtual`。

### B4 答案
**错误**：派生类自定义拷贝构造 `Derived(const Derived &d)` **没有在初始化表调用基类拷贝构造**，导致基类部分用**默认构造**初始化，继承来的 `x` 被置 0、丢失原值。
**改正**：
```cpp
Derived(const Derived &d) : Base(d) {     // 显式调用基类拷贝构造
    y = d.y;
}
```
**考试怎么答**：派生类自定义拷贝构造默认调基类**默认**构造；要正确拷贝基类部分，必须在初始化表写 `: Base(d)`。

### B5 答案
**错误**：① `operator new` 的返回类型必须是 `void*`，写成 `int` 错误（且 `malloc` 返回 `void*` 不能转 `int` 再返回）；② `operator delete` 的首参必须是 `void*`，写成 `int` 错误。
**改正**：
```cpp
#include <cstdlib>
class A {
    int x;
public:
    void *operator new(size_t size) { return malloc(size); }
    void  operator delete(void *p)  { free(p); }
};
```
**考试怎么答**：`operator new` 形如 `void* operator new(size_t)`，`operator delete` 形如 `void operator delete(void*)`（可选第二参数 `size_t`）。

### B6 答案
**错误**：`unique_ptr` 独占所有权，**拷贝构造被禁用**，`std::unique_ptr<int> b = a;` 编译报错。
**改正**：用 `std::move` 转移所有权。
```cpp
std::unique_ptr<int> b = std::move(a);   // a 变空，所有权交给 b
```
**考试怎么答**：`unique_ptr` 不能拷贝/赋值，只能通过 `std::move`（或 `release`/`reset`）转移所有权。

### B7 答案
**错误**：用同一个裸指针 `p` 分别构造 `a` 和 `b`，二者各自维护引用计数（都为 1），互不知晓。`main` 结束时 `a`、`b` 各 `delete` 一次同一块内存 → **重复释放（double free）**。
**改正**：让 `b` 由 `a` 拷贝得到，共享同一控制块。
```cpp
std::shared_ptr<int> a(new int(5));
std::shared_ptr<int> b = a;     // 引用计数为 2，只释放一次
```
**考试怎么答**：不能用同一个裸指针构造多个 `shared_ptr`，应通过拷贝/赋值共享。

### B8 答案
**错误**：组合关系下成员对象应随整体销毁，但析构函数 `~List()` **没有 `delete head`**，内部 `new` 出来的 `Node` 泄漏。
**改正**：
```cpp
~List() { delete head; }
```
**考试怎么答**：组合关系——成员由整体内部创建、整体析构时 `delete`；（对比聚合：成员来自外部，析构时**不应** `delete`，否则误删外部对象。）

### B9 答案
**错误**：① `counter++` 是对共享变量的读-改-写（非原子），两线程并发产生**数据竞争**，结果不确定；② 没有 `join`，主线程可能在子线程结束前就输出甚至退出。
**改正**：加互斥锁保护临界区 + `join` 等待。
```cpp
#include <iostream>
#include <thread>
#include <mutex>
using namespace std;
int counter = 0;
mutex mtx;
void work() {
    for (int i = 0; i < 100000; i++) {
        lock_guard<mutex> lk(mtx);   // 加锁保护
        counter++;
    }
}
int main() {
    thread t1(work);
    thread t2(work);
    t1.join();                       // 等待子线程
    t2.join();
    cout << counter << endl;         // 确定为 200000
    return 0;
}
```
**考试怎么答**：共享可写数据的访问必须放进受锁保护的临界区；主线程须 `join` 等待子线程结束。

### B10 答案
**错误**：`const int id;` 是常量成员，**只能在构造函数初始化表初始化**，不能在函数体内用 `id = i;` 赋值（编译报错）。
**改正**：
```cpp
Config(int i) : id(i) {     // const 成员在初始化表初始化
    value = 0;
}
```
**考试怎么答**：`const` 成员和引用成员都必须在初始化表初始化，不能在构造函数体内赋值。（附带提醒：成员初始化顺序按声明顺序，避免用后声明的成员去初始化先声明的成员。）

---

## 三、手写代码题参考答案

### C1 参考答案
```cpp
class Vec {
    int size;
    int *data;
public:
    Vec(int n) {                         // ① 构造
        size = n;
        data = new int[n];
        for (int i = 0; i < n; i++) data[i] = 0;
    }
    Vec(const Vec &v) {                  // ② 拷贝构造（深拷贝）
        size = v.size;
        data = new int[size];
        for (int i = 0; i < size; i++) data[i] = v.data[i];
    }
    Vec& operator=(const Vec &v) {       // ③ 赋值运算符（深拷贝）
        if (this == &v) return *this;    // 自赋值检查
        delete[] data;                   // 释放旧空间
        size = v.size;
        data = new int[size];
        for (int i = 0; i < size; i++) data[i] = v.data[i];
        return *this;
    }
    ~Vec() { delete[] data; }            // ④ 析构
};
```
**得分点**：构造与拷贝构造都重新 `new` 并逐元素复制（深拷贝）；`operator=` 三要素（自赋值检查、先 `delete[]` 再分配、`return *this`）；析构用 `delete[]`。

### C2 参考答案
```cpp
#include <iostream>
using namespace std;

template <typename T>
class ToyPtr {
    T *ptr_;
public:
    explicit ToyPtr(T *p) : ptr_(p) { }   // 构造：接管堆指针
    ~ToyPtr() { delete ptr_; }            // 析构：自动释放
    T& operator*()  { return *ptr_; }     // 重载 *
    T* operator->() { return ptr_; }      // 重载 ->
};

int main() {
    ToyPtr<int> p(new int(8));            // 离开作用域自动 delete
    cout << *p << endl;                   // 输出 8
    *p = 20;
    cout << *p << endl;                   // 输出 20
    return 0;
}
```
**得分点**：类模板 `template<typename T>`；析构 `delete ptr_`；重载 `T& operator*()` 与 `T* operator->()`；构造用 `explicit` 接管指针。

### C3 参考答案
```cpp
#include <iostream>
using namespace std;

class Animal {                            // 抽象基类
public:
    virtual void speak() const = 0;       // 纯虚函数
    virtual ~Animal() { }                 // 虚析构
};
class Dog : public Animal {
public:
    void speak() const { cout << "Woof" << endl; }
};
class Cat : public Animal {
public:
    void speak() const { cout << "Meow" << endl; }
};

int main() {
    Animal *arr[2];
    arr[0] = new Dog;
    arr[1] = new Cat;
    for (int i = 0; i < 2; i++)
        arr[i]->speak();                  // 动态绑定
    for (int i = 0; i < 2; i++)
        delete arr[i];                    // 有虚析构，正确释放
    return 0;
}
```
**得分点**：`Animal` 含纯虚函数 `= 0` → 抽象类，不能创建对象；`Dog`/`Cat` 各自实现 `speak()`（签名含 `const` 一致）；通过 `Animal*` 调用实现动态绑定；基类提供虚析构函数。

### C4 参考答案
```cpp
#include <cstdlib>     // malloc / free
#include <cstring>     // memset

class A {
    int x, y;
public:
    void *operator new(size_t size) {     // 分配 + 清零
        void *p = malloc(size);
        memset(p, 0, size);
        return p;
    }
    void operator delete(void *p) {       // 归还系统堆
        free(p);
    }
    int getx() const { return x; }
    int gety() const { return y; }
};
// 用法：
// A *p = new A;    // 调用重载 new，x、y 被清零，p->getx()==0, p->gety()==0
// delete p;        // 调用重载 delete
```
**得分点**：`operator new` 返回 `void*`、参数 `size_t`，用 `malloc`+`memset` 清零；`operator delete` 返回 `void`、首参 `void*`，用 `free`；理解即使无构造函数，重载的 `new` 也能完成初始化。

### C5 参考答案
```cpp
#include <iostream>
using namespace std;

template <typename T>
class Stack {
    T buffer[100];
    int top;
public:
    Stack() { top = -1; }
    void push(const T &x);
    void pop(T &x);
    bool empty() const { return top == -1; }
};

template <typename T>
void Stack<T>::push(const T &x) {         // 类外实现
    buffer[++top] = x;
}
template <typename T>
void Stack<T>::pop(T &x) {                // 类外实现
    x = buffer[top--];
}

int main() {
    Stack<int> s;
    s.push(10);
    int v;
    s.pop(v);
    cout << v << endl;                    // 输出 10
    return 0;
}
```
**得分点**：`template<typename T>` 类模板；`top` 初始化为 -1；类外实现成员函数时每个都要带 `template<typename T>` 并用 `Stack<T>::` 限定；使用时显式实例化 `Stack<int>`。

---

### 自测建议
- **程序分析题**：做完后务必和上面输出逐行对照；若错，回到对应模块复习"调用顺序 / 绑定规则 / 引用计数 / 异常匹配"。
- **程序纠错题**：要求能说出"为什么错 + 怎么改"，而不只是改对。
- **手写代码题**：脱稿写一遍，再对照参考答案查得分点是否齐全。
