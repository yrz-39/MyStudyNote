# 高级程序设计（C++）期末冲刺复习文档：考点、题型与实战训练

> 本文在原《复习规划》基础上做"考前实战化升级"：保留考点分层与题型框架，新增**可直接练手的题目（含标准答案与逐步解析）**，并把"预测"改写成"复习动作"。代码尽量贴近课程 PPT 风格，可直接阅读与手写。

## 怎么用这份文档

1. 先看 **第二节考点优先级地图**，明确哪些是大题、哪些是小题。
2. **第三节"重要勘误与口径说明"** 务必先读，避免被几处常见误述带偏。
3. **第四节分模块实战训练** 是核心：每个第一梯队模块都给出"必须会什么 / 怎么改编 / 手写什么 / 练什么分析题 / 易错点 / 答题步骤"，外加 **程序分析题、程序纠错题、手写代码题** 各至少一道，均带标准答案与解析。
4. 临考用 **第八节"考前最后一天必过清单"** 做最后冲刺。

---

## 一、考试结构与三大题型拆解

| 题型 | 给你什么 | 要你做什么 | 备考核心能力 |
|------|----------|------------|--------------|
| **程序分析题** | 一段代码 | 分析其作用 / 预测输出 / 判断调用了哪个函数 | 在脑中"跑程序"：构造/析构/拷贝/赋值调用顺序，静态 vs 动态绑定，引用计数变化，异常匹配 |
| **程序纠错题** | 一段有目标说明的代码 + 若干错误 | 找出全部错误并改正、说明原因 | 熟记"标准正确写法"，对照差异定位（深浅拷贝、`delete[]`、虚析构、`const`、`move/release/reset` 等） |
| **手写代码题**（篇幅不短） | 一个功能目标 | 完整写出类/函数 | 默写经典骨架：String 四件套、智能指针、RAII、操作符重载、模板、线程安全代码 |

**素材来源判断**：三种题型的素材大多来自 PPT 现有代码的改编，常见手法是：
- 把"正确版"挖空或改错（→ 纠错题、填空式分析题）；
- 把省略号 `......` 补全（→ 手写题）；
- 删掉"分析注释"让你重新推导（→ 分析题，尤其构造/析构/虚函数调用链）；
- 把单一类换业务外壳（`String`→`Buffer`、`Complex`→`Fraction`、`Counter`→`Timer`），骨架不变。

---

## 二、考点优先级地图

### 🔴 第一梯队（高概率出大题，应能默写 + 能跑程序）
1. 拷贝构造函数与深浅拷贝（`String` 类是头号素材）
2. 构造/析构函数调用顺序（含成员对象、含继承链 `基类→成员对象→派生类`）
3. 虚函数与静态/动态绑定（基类指针/引用调用谁；构造/析构中调用虚函数）
4. 派生类对象的初始化、消亡、拷贝构造与赋值（显式调用基类构造/赋值）
5. `new`/`delete` 操作符重载（自由空间链表、定位 new、`new[]/delete[]`）
6. 结构化异常处理与异常嵌套（`try/throw/catch` 类型匹配、沿调用链查找）
7. 内存安全问题识别 + RAII + 智能指针（`unique_ptr`/`shared_ptr`/`weak_ptr`，引用计数）
8. 聚合与组合（指针成员 vs 对象成员，谁负责创建/销毁）
9. 并行程序设计（`std::thread`、`join/detach`、`mutex`、`lock_guard`、数据竞争）
10. 访问控制 + 子类型（继承方式访问表、向上赋值合法性）

### ⚫ 第二梯队（小题/概念题/纠错点，掌握原理即可）
- 静态成员与静态成员函数、常成员函数（`const`）
- 抽象类与纯虚函数
- 基本操作符重载（双目/单目/`++` 前后置）、`[]`、`()` 函数对象、`->`、类型转换
- 友元（函数/类/成员函数友元，`<<`/`>>` 重载）
- 面向对象输入输出
- 泛型（函数模板、类模板、非类型参数、模板复用与头文件问题）
- STL（容器/迭代器/算法三件套）
- 派生类成员标识符作用域（同名隐藏、`using` 声明）

---

## 三、重要勘误与口径说明（务必先读）

下面几点是高频"似是而非"的表述，考试与标准 C++ 口径有细微差别，单独列出避免被误导。

**1. 关于"派生类同型构函数自动是虚函数"的精确表述**
更严谨的说法是：**如果基类中的某个成员函数是虚函数，那么派生类中同签名（同型构）重写它的函数，即使不写 `virtual` 关键字，也仍然具有虚函数性质。** 它并不是"任何同名函数自动变虚"，前提是基类对应函数本身为虚函数且签名匹配（重写 override）。

**2. 关于 `throw "abcd"` 的类型**
字符串字面量 `"abcd"` 的类型更准确地说是 `const char*`（在 C++ 中数组退化为指向常量字符的指针）。课程 PPT 里常写 `catch(char*)`，**考试时按课件口径作答即可**；但需知道**规范 C++ 更推荐写 `catch(const char*)`**。答题时如果题目用了 PPT 风格 `catch(char*)`，就按它匹配。

**3. 关于"基类析构非虚时 delete 派生类对象"的后果**
课程通常的标准答案是：**通过基类指针 `delete` 派生类对象时，若基类析构函数不是虚函数，则派生类的析构函数不会被调用，可能造成（派生类自己申请的）资源泄漏。** 需要补充一个小注释：**从标准 C++ 角度看，这种情形属于"未定义行为（undefined behavior）"**，因此不应把"一定只调用基类析构、一定泄漏多少"说得过于绝对——结论方向（应把基类析构设为虚函数）是确定的，具体表现依实现而定。

**4. 代码风格**
本文代码尽量使用课程 PPT 风格（`iostream`、`using namespace std`、裸 `new/delete`、简单模板），不引入课件未讲的复杂或过于现代的写法，方便你直接照着手写。

---

## 四、分模块实战训练

> 每个第一梯队模块结构统一：**必须会什么 → 怎么改编 → 手写什么 → 练什么分析题 → 易错点 → 答题步骤**，随后给出 **分析 / 纠错 / 手写** 三类实战题（含答案与解析）。

---

### 模块 1：拷贝构造、深浅拷贝与 String 四件套 🔴🔴🔴

**这个模块必须会什么**
- 拷贝构造的三种触发场景：① 用同类对象初始化新对象；② 对象作值参数传入函数；③ 对象作函数返回值。
- 隐式拷贝构造 = 逐成员拷贝（对成员对象递归调用其拷贝构造）；对裸指针只复制地址（浅拷贝）。
- 含裸指针 + 自申请资源的类必须自定义"四件套"：构造、拷贝构造、赋值运算符、析构，实现深拷贝。
- 初始化 `A b=a;` / `B b2(b1);` 调拷贝构造；赋值 `b=a;` 调 `operator=`。

**最可能怎样改编 PPT 代码**：把 PPT 的 `String` 换皮成 `Buffer`/`DynArray`/`MyString`，或故意删掉拷贝构造、赋值中的某一句。

**应该手写哪段代码**：String 四件套（见手写题 1-3）。

**应该练哪类分析题**：带 `cout` 的构造/拷贝/析构计数，预测输出与析构顺序。

**最容易出错的地方**：`new char[len]` 漏 `+1`；`operator=` 漏自赋值检查 / 漏 `delete[]` / 漏 `return *this`；只写析构不写拷贝构造。

**赋值操作符 `operator=` 重点展开**：它处理的是“已经存在的对象之间赋值”，例如 `b = a;`。这和 `String b = a;` 不同，后者是用已有对象初始化新对象，调用的是拷贝构造函数。

一个管理动态内存的类，赋值运算符通常要做三件事：
```cpp
String& operator=(const String &s) {
    if (this == &s) return *this;     // ① 防止自赋值

    delete[] str;                     // ② 释放原来对象已有资源

    len = s.len;
    str = new char[len + 1];          // ③ 重新申请足够空间
    strcpy(str, s.str);               // ④ 深拷贝内容

    return *this;                     // ⑤ 返回当前对象本身
}
```

1. **漏自赋值检查：`if (this == &s) return *this;`**

   可能错误写法：
   ```cpp
   String& operator=(const String &s) {
       delete[] str;
       str = new char[s.len + 1];
       strcpy(str, s.str);
       len = s.len;
       return *this;
   }
   ```

   错误原因：如果出现 `a = a;`，此时 `this` 和 `&s` 指向同一个对象，`str` 和 `s.str` 其实也是同一块内存。执行 `delete[] str;` 后，`s.str` 也变成了已经被释放的悬空指针，后面再 `strcpy(str, s.str);` 就是在读取已释放内存，结果未定义，可能乱码、崩溃。

   正确改法：
   ```cpp
   if (this == &s) return *this;
   ```

   正确原因：如果是自己给自己赋值，内容本来就不需要改变，直接返回当前对象，避免先释放再读取自己的数据。

2. **漏 `delete[] str;`**

   可能错误写法：
   ```cpp
   String& operator=(const String &s) {
       if (this == &s) return *this;
       len = s.len;
       str = new char[len + 1];
       strcpy(str, s.str);
       return *this;
   }
   ```

   错误原因：赋值对象左边原来已经有一块动态内存，例如：
   ```cpp
   String a("hello");
   String b("cpp");
   b = a;
   ```
   `b` 原来的 `"cpp"` 空间还没有释放，就直接让 `b.str` 指向新申请的空间，原来的那块内存再也找不到了，造成**内存泄漏**。

   正确改法：
   ```cpp
   delete[] str;
   ```

   正确原因：赋值前，左操作数对象已经存在，里面可能已经持有资源。重新申请新空间之前，必须先释放旧空间，防止内存泄漏。

3. **漏 `return *this;`**

   可能错误写法：
   ```cpp
   String& operator=(const String &s) {
       if (this == &s) return *this;
       delete[] str;
       len = s.len;
       str = new char[len + 1];
       strcpy(str, s.str);
       // 忘了 return *this;
   }
   ```

   错误原因：函数声明返回类型是 `String&`，表示必须返回一个 `String` 对象的引用。如果没有返回值，编译器可能报警或报错；即使侥幸通过，也会导致未定义行为。更重要的是，赋值表达式本身应该有结果，才能支持链式赋值：
   ```cpp
   a = b = c;
   ```
   它实际等价于：
   ```cpp
   a = (b = c);
   ```
   如果 `b = c` 没有返回 `b` 本身，外层的 `a = ...` 就无法正确继续。

   正确改法：
   ```cpp
   return *this;
   ```

   正确原因：`*this` 表示当前对象本身，返回 `String&` 可以避免多余拷贝，并且符合内置赋值运算符的习惯，使 `a = b = c;` 这种连续赋值成立。

4. **顺序也很重要：先判自赋值，再释放旧空间，再深拷贝**

   推荐顺序：
   ```cpp
   if (this == &s) return *this;
   delete[] str;
   len = s.len;
   str = new char[len + 1];
   strcpy(str, s.str);
   return *this;
   ```

   记忆口诀：**判自己 → 删旧的 → 申请新的 → 拷内容 → 返回自己**。

**答题步骤（分析题）**：① 标出每次"初始化/传值/返回"是否触发拷贝；② 标出每个对象的创建点与销毁点；③ 析构按构造的逆序；④ 写出完整输出序列。

#### 【程序分析题 1-1】写出下面程序的输出
```cpp
#include <iostream>
#include <cstring>
using namespace std;

class String {
    int len;
    char *str;
public:
    String(const char *s) {
        len = strlen(s);
        str = new char[len + 1];
        strcpy(str, s);
        cout << "ctor " << str << endl;
    }
    String(const String &s) {
        len = s.len;
        str = new char[len + 1];
        strcpy(str, s.str);
        cout << "copy " << str << endl;
    }
    ~String() {
        cout << "dtor " << str << endl;
        delete[] str;
    }
    void print() const { cout << str << endl; }
};

void show(String s) {   // 对象作值参数 → 触发拷贝构造
    s.print();
}

int main() {
    String a("abc");
    show(a);
    return 0;
}
```

**标准答案**
```
ctor abc
copy abc
abc
dtor abc
dtor abc
```

**逐步解析**
1. `String a("abc");` 调普通构造 → 输出 `ctor abc`。
2. `show(a);` 形参 `s` 是值参数，用实参 `a` 拷贝构造 → 输出 `copy abc`。
3. 进入 `show` 体内 `s.print();` → 输出 `abc`。
4. `show` 返回，形参 `s` 消亡 → 调析构 → 输出 `dtor abc`。
5. `main` 返回，局部对象 `a` 消亡 → 调析构 → 输出 `dtor abc`。
   （考点：值参数触发拷贝构造；深拷贝下两次析构各自释放自己的 `str`，不会重复释放。）

#### 【程序纠错题 1-2】
**目标**：为含动态字符串的类实现深拷贝，保证拷贝、赋值后两对象互不影响，且析构不重复释放内存。请找出并改正错误。
```cpp
class String {
    int len;
    char *str;
public:
    String(const char *s) {
        len = strlen(s);
        str = new char[len];          // 错误①
        strcpy(str, s);
    }
    String(const String &s) {
        str = s.str;                  // 错误②
        len = s.len;
    }
    String& operator=(const String &s) {
        delete[] str;
        str = new char[s.len + 1];
        strcpy(str, s.str);
        len = s.len;
        // 错误③
    }
    ~String() { delete[] str; }
};
```

**标准答案（错误与改正）**
```cpp
str = new char[len + 1];              // 改正①：要为结尾 '\0' 多留一字节

String(const String &s) {             // 改正②：必须深拷贝，重新分配并复制内容
    len = s.len;
    str = new char[len + 1];
    strcpy(str, s.str);
}

String& operator=(const String &s) {  // 改正③：补自赋值检查与返回 *this
    if (&s == this) return *this;     // 防自赋值（否则先 delete 再用已删内容）
    delete[] str;
    str = new char[s.len + 1];
    strcpy(str, s.str);
    len = s.len;
    return *this;                     // 必须返回，否则连续赋值 a=b=c 出错
}
```

**为什么错 / 考试怎么答**
- 错误①：`strcpy` 会写入 `len+1` 个字节（含结尾 `'\0'`），只分配 `len` 会越界写（缓冲区溢出）。答："少分配 1 字节，写入 `'\0'` 越界，应为 `new char[len+1]`。"
- 错误②：`str = s.str;` 是浅拷贝，两对象指向同一块内存 → 一方修改影响另一方，且析构时同一块被释放两次（double free）。答："拷贝构造做了浅拷贝，应改为重新分配并 `strcpy` 实现深拷贝。"
- 错误③：`operator=` 缺自赋值检查与 `return *this`。答："`a=a` 时会先 `delete[] str` 再读取已释放的 `s.str`；且无返回值无法支持链式赋值，应加 `if(&s==this) return *this;` 与 `return *this;`。"

#### 【手写代码题 1-3】
**题干**：定义一个管理动态字符数组的类 `MyString`，内部用 `char* str` 和 `int len` 表示。要求完整写出能正确深拷贝的"四件套"：带 `const char*` 参数的构造函数、拷贝构造函数、赋值运算符、析构函数。

**参考答案**
```cpp
#include <cstring>

class MyString {
    int len;
    char *str;
public:
    MyString(const char *s) {                 // 构造
        len = strlen(s);
        str = new char[len + 1];
        strcpy(str, s);
    }
    MyString(const MyString &s) {             // 拷贝构造（深拷贝）
        len = s.len;
        str = new char[len + 1];
        strcpy(str, s.str);
    }
    MyString& operator=(const MyString &s) {  // 赋值运算符（深拷贝）
        if (&s == this) return *this;         // 防自赋值
        delete[] str;
        str = new char[s.len + 1];
        strcpy(str, s.str);
        len = s.len;
        return *this;
    }
    ~MyString() {                             // 析构
        delete[] str;
        str = NULL;
        len = 0;
    }
};
```

**关键得分点**
- 构造与拷贝构造都 `new char[len+1]`（+1 留给 `'\0'`）。
- 拷贝构造重新分配内存并 `strcpy`（深拷贝），不能直接复制指针。
- `operator=` 三要素：**自赋值检查**、**先 `delete[]` 旧空间再分配新空间**、**`return *this`**。
- 析构 `delete[]`（不是 `delete`）。

---

### 模块 2：构造/析构函数调用顺序 🔴🔴🔴

**这个模块必须会什么**
- 含成员对象：先构造成员对象（按**声明顺序**），再执行本类构造体；析构相反。
- 继承 + 成员对象：构造顺序 `基类 → 成员对象 → 派生类`；析构顺序 `派生类 → 成员对象 → 基类`。
- 成员/基类的非默认构造必须写在初始化表：`D(int i,int j): A(i), m(j) {...}`。
- 成员初始化顺序只看声明顺序，与初始化表书写顺序无关。

**最可能怎样改编 PPT 代码**：在每个构造/析构里加 `cout`，让你预测输出顺序；或加一层继承/多个成员对象增加复杂度。

**应该手写哪段代码**：能正确把参数传到各基类/成员对象的构造函数（见手写题 2-3）。

**应该练哪类分析题**：多层继承 + 成员对象的构造/析构输出序列。

**最容易出错的地方**：把基类/成员的非默认构造写进函数体（变成"先默认构造再赋值"）；把析构顺序写反；`const`/引用成员未在初始化表初始化。

**答题步骤**：① 画出"基类 → 成员对象（按声明序）→ 本类"的构造链；② 析构严格逆序；③ 注意初始化表里指定的是哪个重载构造。

#### 【程序分析题 2-1】写出下面程序的输出
```cpp
#include <iostream>
using namespace std;

class A {
public:
    A()      { cout << "A()" << endl; }
    A(int i) { cout << "A(int)" << endl; }
    ~A()     { cout << "~A()" << endl; }
};

class M {
public:
    M()  { cout << "M()" << endl; }
    ~M() { cout << "~M()" << endl; }
};

class D : public A {
    M m;                       // 成员对象
public:
    D(int i) : A(i) {          // 显式调用基类的 A(int)
        cout << "D(int)" << endl;
    }
    ~D() { cout << "~D()" << endl; }
};

int main() {
    D d(5);
    return 0;
}
```

**标准答案**
```
A(int)
M()
D(int)
~D()
~M()
~A()
```

**逐步解析**
1. 创建 `d`：先构造基类部分 → 因 `:A(i)` 调 `A(int)` → `A(int)`。
2. 再构造成员对象 `m` → `M()`。
3. 最后执行 `D` 的构造体 → `D(int)`。
4. `d` 消亡：先执行 `~D` 体 → `~D()`。
5. 再析构成员对象 `m` → `~M()`。
6. 最后析构基类 → `~A()`。
   （考点：构造 `基类→成员对象→派生类`，析构严格逆序。）

#### 【程序纠错题 2-2】
**目标**：让 `D` 在构造时用基类的 `A(int)`、成员对象用 `M(int)` 初始化。请找出并改正错误。
```cpp
class A {
    int x;
public:
    A() { x = 0; }
    A(int i) { x = i; }
};
class M {
    int v;
public:
    M() { v = 0; }
    M(int i) { v = i; }
};
class D : public A {
    M m;
    const int id;
public:
    D(int i, int j) {       // 错误①②③
        A(i);               // 想初始化基类
        m = M(j);           // 想初始化成员对象
        id = i;             // 想初始化常量成员
    }
};
```

**标准答案（改正）**
```cpp
D(int i, int j) : A(i), m(j), id(i) {   // 全部放进初始化表
    // 函数体可为空
}
```

**为什么错 / 考试怎么答**
- 错误①：`A(i);` 在函数体里写，只是创建了一个**临时 A 对象**，并未初始化基类子对象（基类已用默认 `A()` 构造过了）。应写在初始化表 `: A(i)`。
- 错误②：`m = M(j);` 是**先默认构造 `m` 再赋值**，不是用 `M(int)` 初始化；应写 `: m(j)`。
- 错误③：`const int id;` 是常量成员，**只能在初始化表初始化**，函数体内赋值非法（且基类构造也必须在初始化表）。应写 `: id(i)`。
- 答题要点："基类、成员对象的非默认构造，以及 `const`/引用成员，都必须在构造函数初始化表中完成，不能在函数体内赋值。"

#### 【手写代码题 2-3】
**题干**：已知类 `Engine` 有构造函数 `Engine(int power)`，类 `Wheel` 有默认构造函数。设计类 `Car`，包含一个 `Engine` 成员对象和一个 `Wheel` 成员对象，并提供构造函数 `Car(int power)`，用 `power` 初始化 `Engine`。写出 `Car` 的定义（成员对象声明 + 构造函数）。

**参考答案**
```cpp
class Engine {
    int power;
public:
    Engine(int p) { power = p; }
};

class Wheel {
public:
    Wheel() { }
};

class Car {
    Engine engine;     // 成员对象：无默认构造，必须在初始化表初始化
    Wheel  wheel;
public:
    Car(int power) : engine(power) {   // 用 power 初始化 Engine
        // wheel 自动用默认构造
    }
};
```

**关键得分点**
- `Engine` 无默认构造，`Car` 必须在初始化表 `: engine(power)` 显式调用其有参构造，否则编译报错。
- `Wheel` 有默认构造，可不写（自动调用）。
- 知道成员对象按声明顺序构造。

---

### 模块 3：虚函数、动态绑定与基类指针调用派生类函数 🔴🔴🔴

**这个模块必须会什么**
- 默认静态绑定；只有**通过指针或引用**调用**虚函数**才发生动态绑定。
- 重写关系：基类某函数为虚函数时，派生类同签名函数即使不写 `virtual` 也仍是虚函数（见第三节勘误 1）。
- **构造函数与析构函数中调用虚函数 → 不进行动态绑定**（绑到当前正在构造/析构的那个类）。
- 析构函数通常应设为虚函数（否则通过基类指针 `delete` 派生类对象时派生类析构不被调用，见勘误 3）。
- 非虚函数即使同名也按静态类型绑定；基类指针访问派生类**新增**成员需 `dynamic_cast`。

**最可能怎样改编 PPT 代码**：给一组 `A a; B b; A* p` 后的若干 `p->f()/g()/h()`，逐行问调用谁；或在构造/析构里调虚函数考"为何不动态绑定"。

**应该手写哪段代码**：用抽象基类 + 派生类实现多态（见手写题 3-3）。

**应该练哪类分析题**：虚/非虚混合调用的输出（本模块分析题 3-1）。

**最容易出错的地方**：误以为构造/析构里的虚调用会动态绑定；忘记 `delete` 基类指针时析构是否虚函数；把非虚函数当虚函数。

**答题步骤**：① 先看调用是否"通过指针/引用"；② 再看被调函数是否虚函数；③ 二者都满足才看动态类型，否则按静态类型；④ 构造/析构内的虚调用一律按当前类。

#### 【程序分析题 3-1】写出下面程序的输出
```cpp
#include <iostream>
using namespace std;

class A {
public:
    A() { f(); }                 // 构造中调用虚函数
    virtual ~A() { f(); }        // 析构中调用虚函数（且析构为虚）
    virtual void f() { cout << "A::f" << endl; }
    void g() { cout << "A::g" << endl; }
    void h() { f(); g(); }       // h 是 A 的非虚成员
};

class B : public A {
public:
    void f() { cout << "B::f" << endl; }   // 重写虚函数 f
    void g() { cout << "B::g" << endl; }   // 隐藏非虚函数 g
};

int main() {
    A *p = new B;
    p->f();
    p->g();
    p->h();
    delete p;
    return 0;
}
```

**标准答案**
```
A::f
B::f
A::g
B::f
A::g
A::f
```

**逐步解析**
1. `new B`：先调基类构造 `A()`，其中调 `f()`——构造中**不动态绑定**，绑到 `A::f` → `A::f`。（B 的隐式构造体无输出。）
2. `p->f();`：通过指针调虚函数 `f`，动态类型是 B → `B::f`。
3. `p->g();`：`g` 非虚，按静态类型 `A*` → `A::g`。
4. `p->h();`：`h` 是 A 的非虚成员，正常调用 A::h；体内 `f()` 是虚调用（经 this 指针），动态类型 B → `B::f`；`g()` 非虚，绑到 `A::g` → 输出 `B::f` 再 `A::g`。
5. `delete p;`：`~A` 是虚函数，动态绑定 → 先调 `B::~B()`（隐式，无输出），再调 `A::~A()`；`~A` 体内 `f()`——析构中**不动态绑定**，此时对象已退化为 A，绑到 `A::f` → `A::f`。

#### 【程序纠错题 3-2】
**目标**：通过基类指针管理派生类对象，并在 `delete` 时正确释放派生类自己申请的资源。请找出并改正错误。
```cpp
class Base {
public:
    Base() { }
    ~Base() { }                 // 错误所在
    virtual void work() { }
};
class Derived : public Base {
    int *data;
public:
    Derived() { data = new int[100]; }
    ~Derived() { delete[] data; }
    void work() { }
};
int main() {
    Base *p = new Derived;
    // ... 使用 p ...
    delete p;                   // 期望释放 data
    return 0;
}
```

**标准答案（改正）**
```cpp
virtual ~Base() { }             // 将基类析构函数声明为虚函数
```

**为什么错 / 考试怎么答**
- 错误：`Base` 的析构函数不是虚函数。`delete p;`（`p` 静态类型 `Base*`）时，按课程口径**只会调用 `Base::~Base()`，不会调用 `Derived::~Derived()`，导致 `data` 指向的内存泄漏**。
- 改正：把基类析构声明为 `virtual ~Base()`，使 `delete` 动态绑定到 `Derived::~Derived()`，再自动调用基类析构。
- 注释（勘误 3）：从标准 C++ 角度，通过基类指针 `delete` 没有虚析构的派生类对象属于**未定义行为**；考试按"派生类析构不被调用、可能资源泄漏"作答即可，但表述上避免绝对化。
- 答题要点："凡是可能通过基类指针删除派生类对象的类，基类析构函数都应设为虚函数。"

#### 【手写代码题 3-3】
**题干**：用抽象基类 `Shape` 定义统一接口 `area()`（纯虚函数），派生出 `Circle`（半径 `r`）和 `Rectangle`（宽 `w`、高 `h`）并各自实现 `area()`。再写一段代码：用一个 `Shape*` 数组存放若干图形，通过动态绑定输出每个图形的面积。

**参考答案**
```cpp
#include <iostream>
using namespace std;

const double PI = 3.1416;

class Shape {                          // 抽象基类
public:
    virtual double area() const = 0;   // 纯虚函数
    virtual ~Shape() { }               // 虚析构（基类应有）
};

class Circle : public Shape {
    double r;
public:
    Circle(double radius) { r = radius; }
    double area() const { return PI * r * r; }
};

class Rectangle : public Shape {
    double w, h;
public:
    Rectangle(double width, double height) { w = width; h = height; }
    double area() const { return w * h; }
};

int main() {
    Shape *shapes[2];
    shapes[0] = new Circle(2.0);
    shapes[1] = new Rectangle(3.0, 4.0);

    for (int i = 0; i < 2; i++)
        cout << shapes[i]->area() << endl;   // 动态绑定到各自的 area

    for (int i = 0; i < 2; i++)
        delete shapes[i];                    // 因有虚析构，能正确析构
    return 0;
}
```

**关键得分点**
- `Shape` 含纯虚函数 `virtual double area() const = 0;` → 抽象类，不能创建对象。
- 派生类必须各自实现 `area()`，签名（含 `const`）与基类一致。
- 通过 `Shape*` 调用 `area()` 实现动态绑定；高层循环代码不随图形种类增加而改动。
- 基类提供虚析构函数，保证 `delete` 时正确释放。

---

### 模块 4：派生类的初始化、拷贝构造与赋值运算符 🔴🔴

**这个模块必须会什么**
- 派生类**隐式**拷贝构造会自动调用基类拷贝构造；派生类**自定义**拷贝构造默认调用基类**默认**构造，需要在初始化表写 `: A(b)` 才调基类拷贝构造。
- 派生类**自定义** `operator=` 不会自动调用基类赋值，须显式：`*(A*)this = b;` 或 `this->A::operator=(b);`，并先做自赋值检查。

**最可能怎样改编 PPT 代码**：给一个派生类的自定义拷贝构造/赋值，故意漏掉对基类的调用，让你找错或分析后果。

**应该手写哪段代码**：派生类的拷贝构造（`:A(b)`）与赋值运算符（`*(A*)this=b`）（见手写题 4-3）。

**应该练哪类分析题**：对比"隐式 vs 自定义"拷贝构造时基类部分的差异。

**最容易出错的地方**：自定义拷贝构造漏 `:A(b)` → 基类部分被默认构造、数据丢失；`operator=` 漏基类赋值与自赋值检查。

**答题步骤**：① 判断是隐式还是自定义；② 自定义则检查是否显式处理了基类部分；③ 检查自赋值与 `return *this`。

#### 【程序分析题 4-1】写出下面程序的输出
```cpp
#include <iostream>
using namespace std;

class A {
    int x;
public:
    A() { x = 0; }
    A(const A &a) { x = a.x; }
    int getx() const { return x; }
    void setx(int v) { x = v; }
};

class B : public A {
    int y;
public:
    B() { y = 0; }
    B(const B &b) { y = b.y; }   // 自定义拷贝构造，未写 :A(b)
    int gety() const { return y; }
};

int main() {
    B b1;
    b1.setx(10);                 // 基类成员 x = 10
    B b2(b1);                    // 用 b1 拷贝构造 b2
    cout << b2.getx() << " " << b2.gety() << endl;
    return 0;
}
```

**标准答案**
```
0 0
```

**逐步解析**
1. `B b1;` → `b1.x=0, b1.y=0`；`b1.setx(10)` → `b1.x=10`。
2. `B b2(b1);` 调用**自定义**拷贝构造 `B(const B&)`，它只写了 `y=b.y`，**没有 `:A(b)`**，所以基类部分用**默认构造** `A()` 初始化 → `b2.x=0`；`b2.y = b1.y = 0`。
3. 输出 `b2.getx()=0`、`b2.gety()=0` → `0 0`。
   （考点：自定义派生类拷贝构造默认调基类**默认**构造，基类数据 `x=10` 丢失。若想保留应写 `B(const B &b) : A(b) { y = b.y; }`，则输出 `10 0`。）

#### 【程序纠错题 4-2】
**目标**：让派生类 `B` 的赋值运算符既正确赋值派生类成员，又正确赋值从基类继承的成员，并能防自赋值、支持链式赋值。请找出并改正错误。
```cpp
class A {
    int x;
public:
    A() { x = 0; }
    A& operator=(const A &a) { x = a.x; return *this; }
};
class B : public A {
    int y;
public:
    B() { y = 0; }
    B& operator=(const B &b) {
        y = b.y;                 // 错误①：只赋值了派生类成员
        // 错误②：没有自赋值检查
        // 错误③：没有返回 *this
    }
};
```

**标准答案（改正）**
```cpp
B& operator=(const B &b) {
    if (&b == this) return *this;     // 改正②：自赋值检查
    *(A*)this = b;                    // 改正①：显式调用基类赋值，赋值继承来的 x
    // 也可写成：this->A::operator=(b);
    y = b.y;
    return *this;                     // 改正③：返回 *this
}
```

**为什么错 / 考试怎么答**
- 错误①：派生类自定义 `operator=` 不会自动调用基类赋值，基类成员 `x` 不会被赋值。应显式 `*(A*)this = b;`（把 `this` 当作 `A*` 来调用基类赋值），或 `this->A::operator=(b);`。
- 错误②：缺自赋值检查。虽然此例无动态资源，但养成习惯且课程要求；含资源时 `a=a` 不检查会出错。
- 错误③：无 `return *this;`，无法支持 `b1=b2=b3` 链式赋值。
- 答题要点："派生类自定义赋值运算符必须显式调用基类赋值、加自赋值检查、返回 `*this`。"

#### 【手写代码题 4-3】
**题干**：已有基类 `Person`（含拷贝构造和赋值运算符）。派生类 `Student` 增加一个 `int score` 成员。请为 `Student` 写出**自定义拷贝构造函数**和**赋值运算符**，要求正确处理从 `Person` 继承的部分。

**参考答案**
```cpp
class Person {
    // ... 数据成员 ...
public:
    Person() { }
    Person(const Person &p) { /* 拷贝基类成员 */ }
    Person& operator=(const Person &p) {
        if (&p == this) return *this;
        /* 赋值基类成员 */
        return *this;
    }
};

class Student : public Person {
    int score;
public:
    Student() { score = 0; }

    Student(const Student &s) : Person(s) {   // 显式调用基类拷贝构造
        score = s.score;
    }

    Student& operator=(const Student &s) {
        if (&s == this) return *this;          // 自赋值检查
        Person::operator=(s);                  // 显式调用基类赋值（或 *(Person*)this = s;）
        score = s.score;
        return *this;
    }
};
```

**关键得分点**
- 拷贝构造在初始化表写 `: Person(s)`，调用基类拷贝构造处理继承部分。
- 赋值运算符显式 `Person::operator=(s)`（或 `*(Person*)this = s;`）。
- 自赋值检查 + `return *this`。

---

### 模块 5：`new` / `delete` 操作符重载 🔴🔴

**这个模块必须会什么**
- `new` 两功能：分配空间 + 调用构造函数；`delete` 两功能：调用析构函数 + 释放空间。重载只改"分配/释放"部分，不影响构造/析构调用。
- 重载格式（可省 `static`，但本质是静态成员）：
  `void* operator new(size_t size);`（返回类型必须 `void*`）
  `void operator delete(void* p);`（返回类型必须 `void`）
- 定位 new（带额外参数）：`void* operator new(size_t, void* p){ return p; }`，用法 `new(buf) A(...)`，需手动 `p->~A();`。
- 自由空间链表思想：首次分配一大块，切成小块用 `next` 串成链表，从链表取/还。
- `new[]`/`delete[]`：有析构函数时分配的 size 会多 4 字节存元素个数；`delete[]` 的 `[]` 不能漏。

**最可能怎样改编 PPT 代码**：给定位 new / 自由空间链表的骨架挖空或改错；考分配/释放与构造/析构的关系。

**应该手写哪段代码**：把动态对象初始化为全 0 的 `new`/`delete` 重载（见手写题 5-3）。

**应该练哪类分析题**：定位 new 把对象建在哪、为何不能用系统 `delete`。

**最容易出错的地方**：`operator new` 返回类型写错、漏 `static` 含义、`delete` 释放后未维护链表、`delete[]` 写成 `delete`。

**答题步骤**：① 分清"分配/释放"与"构造/析构"是两件事；② 定位 new 的对象空间来自传入指针；③ 自由链表只负责切块与回收。

#### 【程序分析题 5-1】阅读下面使用定位 new 的程序，回答问题
```cpp
#include <iostream>
#include <cstring>
using namespace std;

class A {
    int x, y;
public:
    A(int i, int j) { x = i; y = j; cout << "A ctor" << endl; }
    ~A() { cout << "A dtor" << endl; }
    void *operator new(size_t size, void *p) { return p; }  // 定位 new
    void show() { cout << x << "," << y << endl; }
};

int main() {
    char buf[sizeof(A)];
    A *p = new (buf) A(1, 2);   // 在 buf 上构造对象
    p->show();
    p->~A();                    // 手动调用析构
    return 0;
}
```
**问**：① 程序输出是什么？② 对象 `p` 的空间在哪里？③ 为什么这里用 `p->~A()` 而不是 `delete p`？

**标准答案**
- ① 输出：
```
A ctor
1,2
A dtor
```
- ② 对象建立在栈数组 `buf` 上（定位 new 直接返回传入的 `buf` 地址，不另外申请堆空间）。
- ③ 因为对象空间是 `buf`（栈），不是系统 `new` 从堆申请的，用系统 `delete p` 会去释放一块并非由系统堆分配的内存，行为错误；正确做法是只手动调用析构函数 `p->~A()` 完成清理，空间随 `buf` 出作用域自动回收。

**逐步解析**
`new(buf) A(1,2)` 调用 `operator new(size, buf)` 返回 `buf` 地址（仅"定位"，不分配），随后在该地址上调用构造函数 `A(1,2)` → 输出 `A ctor`。`show()` 输出 `1,2`。`p->~A()` 显式调析构 → `A dtor`。

#### 【程序纠错题 5-2】
**目标**：为类 `A` 重载 `new`/`delete`，使其从系统堆申请空间并在分配时把对象内存清零，释放时归还系统堆。请找出并改正错误。
```cpp
#include <cstdlib>
#include <cstring>
class A {
    int x, y;
public:
    void operator new(size_t size) {     // 错误①
        void *p = malloc(size);
        memset(p, 0, size);
        return p;                         // 错误②（与①相关）
    }
    void operator delete(void *p, int n) {   // 错误③
        free(p);
    }
};
```

**标准答案（改正）**
```cpp
void *operator new(size_t size) {        // 改正①：返回类型必须是 void*
    void *p = malloc(size);
    memset(p, 0, size);
    return p;                            // 现在合法
}
void operator delete(void *p) {          // 改正③：参数应为 void*（可选第二参数 size_t）
    free(p);
}
```

**为什么错 / 考试怎么答**
- 错误①②：`operator new` 的返回类型**必须是 `void*`**，原代码写 `void` 导致无法 `return p`。答："`operator new` 必须返回 `void*`。"
- 错误③：`operator delete` 的第一个参数必须是 `void*`；若带第二参数，类型必须是 `size_t`，不能是 `int`。应为 `void operator delete(void *p)` 或 `void operator delete(void *p, size_t size)`。答："`delete` 重载首参 `void*`，可选第二参数须为 `size_t`。"

#### 【手写代码题 5-3】
**题干**：为类 `A`（含两个 `int` 成员，但**没有**定义任何构造函数）重载 `operator new` 与 `operator delete`，使得用 `new A` 创建的动态对象内存被初始化为全 0，用 `delete` 时归还系统堆。

**参考答案**
```cpp
#include <cstdlib>     // malloc / free
#include <cstring>     // memset

class A {
    int x, y;
public:
    void *operator new(size_t size) {     // 重载 new：分配 + 清零
        void *p = malloc(size);
        memset(p, 0, size);               // 把对象空间初始化为全 0
        return p;
    }
    void operator delete(void *p) {       // 重载 delete：归还系统堆
        free(p);
    }
    int getx() const { return x; }
    int gety() const { return y; }
};

// 用法：
// A *p = new A;     // 调用重载的 new，x、y 被清零
// ... p->getx() == 0, p->gety() == 0 ...
// delete p;         // 调用重载的 delete
```

**关键得分点**
- `operator new` 返回 `void*`，参数 `size_t size`；用 `malloc` 申请并 `memset` 清零。
- `operator delete` 返回 `void`，首参 `void*`；用 `free` 释放。
- 理解：即使类没有构造函数，重载的 `new` 也能为对象提供初始化（清零）。

---

### 模块 6：结构化异常处理与异常嵌套 🔴🔴

**这个模块必须会什么**
- `try { 可能出错的代码 }`；`throw 表达式;` 抛出任意类型对象（`void` 除外）；`catch(类型 变量) { 处理 }` 按**类型精确匹配**捕获。
- `throw` 后其后语句不再执行，沿**函数调用链**退栈，查找匹配的 `catch`。
- 一个 `try` 可跟多个 `catch`，按书写顺序匹配第一个类型兼容者。
- 嵌套：内层 `try` 无匹配则向外层（含调用者）查找；整条调用链都无匹配 → 调用 `terminate()`（默认再调 `abort()`）。

**最可能怎样改编 PPT 代码**：给嵌套的 `f/g/h`，每层不同 `catch`，问某个 `throw` 由谁捕获 / 输出什么。

**应该手写哪段代码**：除零异常的循环重试程序（见手写题 6-3）。

**应该练哪类分析题**：多层调用链 + 多 `catch` 的匹配追踪。

**最容易出错的地方**：`catch` 类型与 `throw` 不匹配（如抛 `int` 却只有 `catch(double)`，不会被捕获）；字符串字面量类型是 `const char*`（见勘误 2）。

**答题步骤**：① 找到 `throw` 的对象类型；② 在最内层 `try` 的 `catch` 列表按顺序找类型匹配；③ 不匹配则退栈到外层/调用者继续找；④ 找到则执行该 `catch` 后继续其后非 catch 语句。

#### 【程序分析题 6-1】写出下面程序的输出
```cpp
#include <iostream>
using namespace std;

void h(int sel) {
    if (sel == 1) throw 1;          // int 异常
    else          throw "err";      // 字符串字面量，类型为 const char*
}

void g(int sel) {
    try {
        h(sel);
    }
    catch (int) {
        cout << "g caught int" << endl;
    }
}

void f(int sel) {
    try {
        g(sel);
    }
    catch (int) {
        cout << "f caught int" << endl;
    }
    catch (const char *) {
        cout << "f caught char*" << endl;
    }
}

int main() {
    f(1);
    f(2);
    return 0;
}
```

**标准答案**
```
g caught int
f caught char*
```

**逐步解析**
- `f(1)`：`h` 抛 `int(1)` → 在 `g` 的 `try` 后 `catch(int)` 匹配成功 → `g caught int`。`g` 正常返回，`f` 不抛异常。
- `f(2)`：`h` 抛字符串 `"err"`（类型 `const char*`） → `g` 只有 `catch(int)`，**不匹配** → 退栈到调用者 `f`；`f` 的 `catch(const char*)` 匹配 → `f caught char*`。
- 口径提示：PPT 常写 `catch(char*)`，本题按规范用 `catch(const char*)`；考试若题目用 `catch(char*)` 就按其匹配。

#### 【程序纠错题 6-2】
**目标**：`safeDivide` 在除数为 0 时抛出异常，`main` 捕获并提示。请找出并改正错误。
```cpp
#include <iostream>
using namespace std;

int safeDivide(int x, int y) {
    if (y == 0) throw 0;
    return x / y;
    cout << "done" << endl;        // 错误①
}

int main() {
    try {
        int r = safeDivide(10, 0);
        cout << r << endl;
    }
    catch (double) {               // 错误②
        cout << "divide by zero" << endl;
    }
    return 0;
}
```

**标准答案（改正）**
```cpp
int safeDivide(int x, int y) {
    if (y == 0) throw 0;           // 抛出 int 类型
    return x / y;
    // 删除 throw/return 之后不可达的语句
}

int main() {
    try {
        int r = safeDivide(10, 0);
        cout << r << endl;
    }
    catch (int) {                  // 改正②：与 throw 0 的 int 类型匹配
        cout << "divide by zero" << endl;
    }
    return 0;
}
```

**为什么错 / 考试怎么答**
- 错误①：`return` 之后的 `cout` 是**不可达代码**，永远不会执行（`throw` 之后也是同理——`throw` 后语句不再执行）。答："`return`/`throw` 之后的语句不可达，应删除。"
- 错误②：`throw 0` 抛出的是 `int`，而 `catch(double)` 只捕获 `double`，**类型不匹配，异常不会被捕获**，最终会触发 `terminate`。应改为 `catch(int)`。答："catch 的类型必须与 throw 的对象类型匹配；`throw 0` 是 `int`，应 `catch(int)`。"

#### 【手写代码题 6-3】
**题干**：写一个程序，反复读入两个整数并相除。用异常处理实现：当除数为 0 时不让程序崩溃，而是提示"除数不能为 0"并要求重新输入，直到得到合法结果为止，输出商后结束。要求用 `throw`/`try`/`catch`。

**参考答案**
```cpp
#include <iostream>
using namespace std;

int divide(int x, int y) {
    if (y == 0) throw 0;        // 除数为 0 时抛出 int 异常
    return x / y;
}

int main() {
    int a, b;
    bool done = false;
    while (!done) {
        cout << "请输入两个整数：";
        cin >> a >> b;
        try {
            int r = divide(a, b);
            cout << a << " / " << b << " = " << r << endl;
            done = true;        // 成功则结束循环
        }
        catch (int) {
            cout << "除数不能为 0，请重新输入" << endl;
        }
    }
    return 0;
}
```

**关键得分点**
- `divide` 中 `if (y==0) throw 0;`，正常时返回商。
- `try` 包住可能抛异常的调用；`catch(int)` 类型与 `throw 0` 匹配。
- 用循环 + 标志位实现"重试直到成功"。

---

### 模块 7：内存安全、RAII 与智能指针 🔴🔴🔴

**这个模块必须会什么**
- 时间类内存问题：释放后使用（use-after-free）、重复释放（double free）、悬垂指针、内存泄漏；空间类：缓冲区溢出、空指针解引用、访问未初始化内存。
- **RAII**：构造函数获取资源、析构函数释放资源，利用对象生命周期自动管理资源。
- `unique_ptr`：独占所有权，**拷贝构造与赋值被禁用**（编译错误），只能用 `std::move` 转移；也可用 `release()`（交出裸指针并置空自身）、`reset()`（删除当前指针并接管新指针）。
- `shared_ptr`：引用计数共享所有权，拷贝/赋值 +1，析构 -1，计数归 0 时自动 `delete`。
- `weak_ptr`：不增加引用计数，用于打破 `shared_ptr` 循环引用；`lock()` 升级为 `shared_ptr`，`use_count()`、`expired()`。
- 两个典型 bug：**同一裸指针构造两个 `shared_ptr`** → 各自计数为 1，重复释放；**循环引用** → 计数无法归 0，内存泄漏。

**最可能怎样改编 PPT 代码**：给 `shared_ptr` 嵌套作用域代码，逐行问引用计数；或给 `unique_ptr` 拷贝、同裸指针双管理、循环引用让你找错。

**应该手写哪段代码**：`ToyPtr` 智能指针模板；RAII 资源包装类（见手写题 7-3）。

**应该练哪类分析题**：`shared_ptr` 引用计数随作用域的变化（本模块分析题 7-1）。

**最容易出错的地方**：以为 `unique_ptr` 可拷贝；同裸指针构造两个 `shared_ptr`；循环引用未用 `weak_ptr`。

**答题步骤（引用计数题）**：① 每个 `shared_ptr` 的构造/拷贝/赋值使计数 +1；② 每个 `shared_ptr` 析构（出作用域）使计数 -1；③ 在每行后标出当前计数；④ 归 0 处对象被释放。

#### 【程序分析题 7-1】写出下面程序的输出（每行 `use_count()`）
```cpp
#include <iostream>
#include <memory>
using namespace std;

int main() {
    shared_ptr<int> x(new int(10));        // (1)
    cout << x.use_count() << endl;
    {
        shared_ptr<int> y = x;             // (2)
        cout << x.use_count() << endl;
        {
            shared_ptr<int> z(y);          // (3)
            cout << x.use_count() << endl;
        }                                  // z 离开作用域
        cout << x.use_count() << endl;
    }                                      // y 离开作用域
    cout << x.use_count() << endl;
    return 0;
}                                          // x 离开作用域，对象释放
```

**标准答案**
```
1
2
3
2
1
```

**逐步解析**
1. `x(new int(10))`：指向新对象，引用计数 = 1 → 输出 `1`。
2. `y = x`：拷贝，计数 +1 = 2 → 输出 `2`。
3. `z(y)`：再拷贝，计数 +1 = 3 → 输出 `3`。
4. 内层块结束，`z` 析构，计数 -1 = 2 → 输出 `2`。
5. 外层块结束，`y` 析构，计数 -1 = 1 → 输出 `1`。
6. `main` 结束，`x` 析构，计数 = 0，对象被自动释放。

#### 【程序纠错题 7-2】
**目标**：用智能指针管理堆对象，避免泄漏与重复释放。下面代码有多处误用，请找出并改正。
```cpp
#include <memory>
#include <iostream>
using namespace std;

int main() {
    // 片段 A：独占指针的误用
    unique_ptr<int> x(new int(5));
    unique_ptr<int> y(x);        // 错误①
    unique_ptr<int> z;
    z = x;                       // 错误②

    // 片段 B：同一裸指针被两个 shared_ptr 接管
    int *p = new int(7);
    shared_ptr<int> a(p);
    shared_ptr<int> b(p);        // 错误③
    return 0;
}
```

**标准答案（改正）**
```cpp
// 片段 A：用 move 转移所有权
unique_ptr<int> x(new int(5));
unique_ptr<int> y(std::move(x));   // 改正①：转移所有权，x 变空
unique_ptr<int> z;
z = std::move(y);                  // 改正②：转移所有权，y 变空

// 片段 B：让两个 shared_ptr 共享同一个智能指针，而不是同一裸指针
shared_ptr<int> a(new int(7));
shared_ptr<int> b = a;             // 改正③：通过拷贝共享，引用计数正确为 2
```

**为什么错 / 考试怎么答**
- 错误①②：`unique_ptr` 独占所有权，**拷贝构造与赋值被禁用**，`unique_ptr<int> y(x);` 和 `z = x;` 都编译报错。应用 `std::move` 转移所有权。答："unique_ptr 不可拷贝/赋值，只能 `std::move` 转移。"
- 错误③：`a(p)` 和 `b(p)` 各自把 `p` 当独立对象管理，**各自引用计数都是 1**；`main` 结束时两者各 `delete` 一次 → **重复释放（double free）**。应让 `b` 由 `a` 拷贝得到（`b = a`），共享同一控制块，计数为 2，只释放一次。答："不能用同一个裸指针构造多个 shared_ptr，应通过拷贝共享。"

#### 【手写代码题 7-3】
**题干**：
(1) 写一个简易智能指针类模板 `ToyPtr<T>`，要求：构造时接管一个堆指针，析构时自动 `delete`，并重载 `*` 和 `->`，使其能像普通指针一样使用。
(2) 用 RAII 思想写一个文件包装类 `FileGuard`，构造时 `fopen` 打开文件，析构时 `fclose` 关闭，保证函数退出（含异常）时文件被关闭。

**参考答案**
```cpp
// (1) 简易智能指针模板
template <typename T>
class ToyPtr {
    T *ptr_;
public:
    explicit ToyPtr(T *p) : ptr_(p) { }   // 构造：接管堆指针
    ~ToyPtr() { delete ptr_; }            // 析构：自动释放
    T& operator*()  { return *ptr_; }     // 重载 *
    T* operator->() { return ptr_; }      // 重载 ->
};

// 用法：
// ToyPtr<int> p(new int(8));   // 离开作用域时自动 delete，无需手动释放
// cout << *p << endl;          // 输出 8
```

```cpp
// (2) RAII 文件包装类
#include <cstdio>

class FileGuard {
    FILE *fp;
public:
    FileGuard(const char *name, const char *mode) {   // 构造获取资源
        fp = fopen(name, mode);
    }
    ~FileGuard() {                                    // 析构释放资源
        if (fp != NULL) fclose(fp);
    }
    FILE *get() const { return fp; }
};

// 用法：
// void printFile(const char *name) {
//     FileGuard f(name, "r");        // 打开
//     // ... 使用 f.get() 读文件；即使中途 return 或抛异常 ...
// }                                  // 离开作用域，析构自动 fclose
```

**关键得分点**
- `ToyPtr`：模板参数 `T`；析构 `delete ptr_`；重载 `T& operator*()` 与 `T* operator->()`；构造建议 `explicit`。
- `FileGuard`：**构造函数获取资源**（`fopen`）、**析构函数释放资源**（`fclose`），体现 RAII；析构前判空更稳妥。
- 能说明 RAII 的价值：无论正常返回还是异常退出，对象析构都会被调用，资源不泄漏。

---

### 模块 8：聚合与组合 🔴

**这个模块必须会什么**
- 聚合（aggregation）：部分可独立于整体存在；成员一般用**指针**，由外部创建后传入，整体析构时**不删除**成员（只置空）。例：公司与员工。
- 组合（composition）：部分随整体生灭；成员是**对象**，或在整体内部 `new`、析构时 `delete` 的指针。例：人与四肢。
- 继承 vs 组合：继承可形成子类型、对派生类暴露 `public+protected`；组合只暴露 `public`，无子类型关系。`private` 继承基本退化为组合。

**最可能怎样改编 PPT 代码**：给两个类的关系代码，问是聚合还是组合、成员何时创建销毁；或把组合类析构的 `delete` 删掉/把聚合类析构误加 `delete`。

**应该手写哪段代码**：用组合（持有线性表）实现队列（见手写题 8-3）。

**应该练哪类分析题**：判断关系类型 + 成员对象生命周期。

**最容易出错的地方**：组合类析构漏 `delete`（泄漏）；聚合类析构里 `delete` 外部对象（误删）。

**答题步骤**：① 看成员是指针还是对象、由谁创建；② 整体消亡时成员是否随之消亡 → 组合；能独立存在 → 聚合。

#### 【程序分析题 8-1】判断关系并分析对象生命周期
```cpp
#include <iostream>
using namespace std;

class A {
public:
    A()  { cout << "A()" << endl; }
    ~A() { cout << "~A()" << endl; }
};

class B {            // 关系一
    A *pm;
public:
    B(A *p) { pm = p; }
    ~B() { p = NULL; }
};m

class C {            // 关系二
    A *pm;
public:
    C()  { pm = new A; }
    ~C() { delete pm; }
};

int main() {
    A *pa = new A;       // (1)
    B b(pa);             // (2)
    cout << "--- B 区结束前 ---" << endl;
    {
        C c;             // (3)
    }                    // (4) c 析构
    delete pa;           // (5)
    return 0;
}
```
**问**：① 输出是什么？② `B` 与 `A`、`C` 与 `A` 各是什么关系？

**标准答案**
- ① 输出：
```
A()
--- B 区结束前 ---
A()
~A()
~A()
```
- ② `B` 与 `A` 是**聚合**关系（成员对象在外部创建、传入，`B` 析构时不删除它）；`C` 与 `A` 是**组合**关系（成员对象在 `C` 内部 `new`、`C` 析构时 `delete`）。

**逐步解析**
1. `(1) new A` → `A()`。
2. `(2)` `b` 接管 `pa` 指向的对象（不新建），无输出。
3. 打印分隔行。
4. `(3)` `C c;` 内部 `new A` → `A()`；`(4)` `c` 析构 → `delete pm` → `~A()`。
5. `(5)` `delete pa;` → 释放最初的对象 → `~A()`。
   （注意：`b` 析构时只 `pm=NULL`，不删除对象，所以最初那个 A 由 `delete pa` 释放，不会重复释放。）

#### 【程序纠错题 8-2】
**目标**：`Holder` 与 `Resource` 是组合关系——`Resource` 应随 `Holder` 内部创建、随 `Holder` 析构而销毁。请找出并改正错误。
```cpp
class Resource {
public:
    Resource()  { /* 申请资源 */ }
    ~Resource() { /* 释放资源 */ }
};
class Holder {
    Resource *pr;
public:
    Holder(Resource *r) { pr = r; }   // 错误①：成员从外部传入
    ~Holder() { }                     // 错误②：未释放成员
};
```

**标准答案（改正）**
```cpp
class Holder {
    Resource *pr;
public:
    Holder()  { pr = new Resource; }  // 改正①：组合关系，成员在内部创建
    ~Holder() { delete pr; }          // 改正②：随整体析构而销毁
};
```

**为什么错 / 考试怎么答**
- 错误①：组合要求被包含对象随整体在内部创建、随整体消亡。原代码从外部传入指针，是聚合的写法，不符合"组合"目标。应在构造函数内部 `new Resource`。
- 错误②：组合类析构必须 `delete` 成员，否则内部创建的 `Resource` 泄漏。
- 答题要点："组合关系下，成员对象在整体内部创建、整体析构时销毁；聚合则相反——这是区分二者的关键，也是 `delete` 该不该出现在析构里的依据。"

#### 【手写代码题 8-3】
**题干**：已有线性表类 `LinearList`，提供 `bool insert(int x, int pos);`、`bool remove(int &x, int pos);`、`int length() const;`。请用**组合**方式（`Queue` 内部持有一个 `LinearList` 成员对象）实现队列类 `Queue`，提供 `en_queue`（入队，加到尾部）和 `de_queue`（出队，从头部取出）。

**参考答案**
```cpp
class LinearList {
public:
    bool insert(int x, int pos);
    bool remove(int &x, int pos);
    int  length() const;
};

class Queue {
    LinearList list;                       // 组合：成员对象
public:
    bool en_queue(int x) {                 // 入队：插到表尾
        return list.insert(x, list.length());
    }
    bool de_queue(int &x) {                // 出队：从表头取
        return list.remove(x, 1);
    }
};
```

**关键得分点**
- `Queue` 以 `LinearList` 为**成员对象**（组合），而非继承。
- `en_queue` 用 `insert` 加到尾部（位置为当前长度）；`de_queue` 用 `remove` 从头部（位置 1）取出。
- 能说明：用组合而非 `public` 继承，是因为队列只想复用线性表的实现，而不希望对外暴露线性表的全部接口（也不需要子类型关系）。

---

### 模块 9：并行程序设计 🔴

**这个模块必须会什么**
- `std::thread t(线程函数, 参数...);` 创建即开始运行。
- `t.join();` 主线程阻塞等待子线程结束；`t.detach();` 主线程放弃对子线程的控制权。
- 数据竞争（data race）：多个线程同时访问共享数据且至少有一个写。临界区（访问共享数据的代码段）需保护。
- `std::mutex` + `lock()/unlock()` 互斥；`std::lock_guard<std::mutex>` 构造时加锁、析构时解锁（RAII 思想，与模块 7 呼应）。
- 经典 bug：多个线程对共享变量做 `sum++`（读-改-写，非原子）未加锁 → 结果不确定。

**最可能怎样改编 PPT 代码**：给未加锁的多线程累加，问"为什么结果不确定"；或漏 `join`、临界区未加锁让你找错。

**应该手写哪段代码**：用 `thread` + `lock_guard` 写线程安全累加（见手写题 9-3）。

**应该练哪类分析题**：数据竞争为何导致结果不确定。

**最容易出错的地方**：忘记 `join`（主线程退出销毁资源，子线程悬空）；临界区未加锁。

**答题步骤**：① 找共享可写数据；② 看访问是否在锁保护下；③ 无保护即数据竞争，结果不确定。

#### 【程序分析题 9-1】分析下面程序的行为
```cpp
#include <iostream>
#include <thread>
using namespace std;

int sum = 0;                 // 共享变量

void add() {
    for (int i = 0; i < 100000; i++)
        sum++;               // 读-改-写，非原子操作
}

int main() {
    thread t1(add);
    thread t2(add);
    t1.join();
    t2.join();
    cout << sum << endl;
    return 0;
}
```
**问**：输出一定是 200000 吗？为什么？

**标准答案**
不一定。理论期望是 200000，但实际结果通常**小于** 200000 且**每次运行可能不同**。

**逐步解析**
- `sum++` 不是原子操作，实际分为三步：读 `sum`、加 1、写回 `sum`。
- 两个线程并发执行时，可能发生交错：例如 t1 和 t2 都读到 `sum` 的同一个旧值，各自加 1 后写回，导致两次自增只生效一次（丢失更新）。
- 这就是**数据竞争**：多线程同时读写共享变量 `sum` 而未加保护，结果不确定。
- 解决：用 `mutex`/`lock_guard` 把 `sum++` 放进临界区保护（见手写题 9-3）。

#### 【程序纠错题 9-2】
**目标**：用两个线程并发地对共享计数器累加，结果应正确且确定；主线程需等待子线程结束。请找出并改正错误。
```cpp
#include <iostream>
#include <thread>
#include <mutex>
using namespace std;

int counter = 0;
mutex mtx;

void work() {
    for (int i = 0; i < 100000; i++) {
        counter++;                 // 错误①：临界区未加锁
    }
}

int main() {
    thread t1(work);
    thread t2(work);
    // 错误②：缺少 join
    cout << counter << endl;
    return 0;
}
```

**标准答案（改正）**
```cpp
void work() {
    for (int i = 0; i < 100000; i++) {
        lock_guard<mutex> lk(mtx);   // 改正①：加锁保护临界区（出作用域自动解锁）
        counter++;
    }
}

int main() {
    thread t1(work);
    thread t2(work);
    t1.join();                       // 改正②：等待子线程结束
    t2.join();
    cout << counter << endl;         // 现在确定为 200000
    return 0;
}
```

**为什么错 / 考试怎么答**
- 错误①：`counter++` 是共享数据的读-改-写，多线程并发会数据竞争。应在访问前加锁（`lock_guard` 构造加锁、析构解锁）。
- 错误②：没有 `join`，主线程可能在子线程还没做完时就输出甚至退出，导致结果错误或子线程引用已销毁资源。应 `t1.join(); t2.join();`。
- 答题要点："共享可写数据的访问必须放入受锁保护的临界区；主线程须 `join` 等待子线程结束。"

#### 【手写代码题 9-3】
**题干**：用两个 `std::thread` 并发计算：每个线程把全局变量 `total` 累加 `n` 次（每次加 1）。要求用 `std::mutex` 配合 `std::lock_guard` 保证线程安全，主线程等待两个子线程结束后输出 `total`。

**参考答案**
```cpp
#include <iostream>
#include <thread>
#include <mutex>
using namespace std;

int total = 0;
mutex mtx;

void add(int n) {
    for (int i = 0; i < n; i++) {
        lock_guard<mutex> lk(mtx);   // 加锁：进入临界区
        total++;
    }                                // lk 析构自动解锁
}

int main() {
    int n = 100000;
    thread t1(add, n);               // 创建并启动线程，传参 n
    thread t2(add, n);
    t1.join();                       // 等待子线程结束
    t2.join();
    cout << total << endl;           // 输出 200000
    return 0;
}
```

**关键得分点**
- `thread t1(add, n);` 创建线程并传参。
- 用 `lock_guard<mutex>` 在临界区自动加锁/解锁（也可手动 `mtx.lock()/unlock()`，但 `lock_guard` 更安全）。
- 主线程 `join` 两个子线程后再读取结果。

---

### 模块 10：访问控制与子类型 🔴

**这个模块必须会什么**
- `public`：处处可访问；`private`：仅本类与友元；`protected`：本类、派生类与友元。
- 继承方式（`public`/`protected`/`private`）× 基类成员访问控制 → 派生类对外的访问控制（记住那张组合表）。
- 子类型：`public` 派生类对象可赋给基类对象（切片，丢派生成员）、可传给需基类的函数、基类指针/引用可指向派生类对象；**反向不行**（基类对象不能赋给派生类、基类对象地址不能赋给派生类指针）。

**最可能怎样改编 PPT 代码**：给一组赋值/取址/调用，逐行判断合法性；或给定继承方式判断成员可见性。

**应该手写哪段代码**：本模块以判断/纠错为主，手写较少。

**应该练哪类分析题**：向上/向下转换合法性逐行判断。

**最容易出错的地方**：派生类直接访问基类 `private` 成员；把基类对象/地址赋给派生类对象/指针。

**答题步骤**：① "派生类对象当基类用"通常合法（向上）；② "基类对象当派生类用"通常非法（向下）；③ 成员可见性看声明处访问控制 + 访问位置。

#### 【程序分析题 10-1】逐行判断合法性（标注 OK / Error 并说明）
```cpp
class A {
public:
    void f() { }
};
class B : public A {     // public 继承
public:
    void g() { }
};

int main() {
    A a;
    B b;

    b.f();          // (1)
    a = b;          // (2)
    A *p = &b;      // (3)
    a.g();          // (4)
    b = a;          // (5)
    B *q = &a;      // (6)
    return 0;
}
```

**标准答案**
```
(1) OK      (2) OK      (3) OK
(4) Error   (5) Error   (6) Error
```

**逐步解析**
- (1) `b.f();`：基类的 `public` 操作可作用于派生类对象 → OK。
- (2) `a = b;`：派生类对象赋给基类对象（向上，发生切片，派生成员被忽略）→ OK。
- (3) `A *p = &b;`：基类指针指向派生类对象（向上）→ OK。
- (4) `a.g();`：`g` 是 `B` 新增成员，基类对象 `a` 没有 → Error。
- (5) `b = a;`：基类对象赋给派生类对象（向下，`a` 缺派生成员的数据）→ Error。
- (6) `B *q = &a;`：派生类指针指向基类对象（向下，`q->g()` 会访问不存在的数据）→ Error。

#### 【程序纠错题 10-2】
**目标**：派生类需要在自己的成员函数里访问并修改基类的数据成员 `value`。请找出并改正错误。
```cpp
class Base {
private:                  // 错误所在
    int value;
public:
    Base() { value = 0; }
};
class Derived : public Base {
public:
    void setValue(int v) {
        value = v;        // 想访问基类数据成员
    }
};
```

**标准答案（改正）**
```cpp
class Base {
protected:                // 改正：private → protected
    int value;
public:
    Base() { value = 0; }
};
// Derived::setValue 中即可直接访问 value
```

**为什么错 / 考试怎么答**
- 错误：`value` 是 `private`，派生类**不能直接访问**基类的私有成员，`value = v;` 编译报错。
- 改正：把 `value` 改为 `protected`，使其可在派生类中访问（`protected` 正是为缓解封装与继承的矛盾而设）。也可保留 `private` 而通过基类的 `public`/`protected` 成员函数间接访问。
- 答题要点："派生类不能直接访问基类的 `private` 成员；需被派生类访问的成员应声明为 `protected`。"

---

### 第二梯队速记（用于纠错/小题/概念题）

| 主题 | 必记点 | 易错/可改编代码方向 |
|------|--------|---------------------|
| 常成员函数 / 静态成员 | `const` 成员函数不能改数据成员（但能改其所指向的内容）；静态成员所有对象共享，须类外定义 `int A::x=0;`；静态成员函数无 `this`、只能访问静态成员 | 对象计数器：构造 `count++`、析构 `count--`、`static int get_num()` |
| 抽象类 / 纯虚函数 | `virtual f()=0;`，含纯虚 → 抽象类 → 不能创建对象，派生类须实现 | Figure 抽象基类框架 |
| 基本操作符重载 | 成员 vs 友元；"实数+复数"只能用全局（友元）函数；`++` 前置返 `Counter&`、后置 `const Counter operator++(int)` 返旧值 | Complex 的 `+`/`==`/取负；Counter 的 `++` |
| `[]`/`()`/`->` 重载 | `[]` 常/非常两版本；`()` 重载得到函数对象（functor），lambda 本质是 functor；`->` 可做指针类（如访问计数） | Vector 的 `[]`；RandomNum 的 `()` |
| 友元 | 不是成员、不对称、不传递；`friend ostream& operator<<(ostream&, const A&)` | Matrix×Vector 的友元乘法 |
| 模板 | 函数模板/类模板语法、非类型参数 `<class T,int size>`、显式实例化 `max<double>(...)`、**模板定义须放头文件**（否则链接错误） | Stack<T> 类模板；sort 函数模板 |
| STL | 容器/迭代器/算法三件套；`vector/list/map/set`；`sort/accumulate/for_each(v.begin(), v.end(), ...)` | 用 vector + 算法求最大值/求和/排序 |
| this 指针 | 成员函数隐含 `A* const this`；需把当前对象整体传出时显式用 `this` | 成员函数中 `func(this)` |

---

## 五、高频陷阱清单（纠错题命中率高，建议逐条记忆）

1. 含裸指针的类只写析构，**漏拷贝构造或漏赋值** → 浅拷贝灾难（共享、重复释放、互相干扰）。
2. `operator=` **漏自赋值检查**、漏 `delete[]`、漏 `return *this`。
3. `new char[len]` **少 `+1`**（没给结尾 `'\0'` 留位）。
4. 基类析构函数**未加 `virtual`** → 通过基类指针 `delete` 派生类对象时派生类析构不被调用，可能资源泄漏（标准 C++ 视为未定义行为）。
5. 派生类自定义拷贝构造/赋值**漏调基类**（`:A(b)` / `*(A*)this=b`）。
6. **构造/析构函数里调用虚函数**误以为会动态绑定（实际绑到当前类）。
7. `unique_ptr` 被**拷贝/赋值**（应 `std::move`）。
8. **同一裸指针构造两个 `shared_ptr`**（各自计数 1，重复释放）。
9. **`shared_ptr` 循环引用**未用 `weak_ptr`（计数不归 0，泄漏）。
10. `delete[]` 写成 `delete`；组合类析构**漏 `delete`**；聚合类析构**误 `delete`** 外部对象。
11. 成员初始化按**声明顺序**而非初始化表书写顺序；`const`/引用成员必须在初始化表初始化。
12. `catch` **类型与 `throw` 不匹配**或顺序不当；`throw`/`return` 之后写多余（不可达）代码。
13. 多线程**忘 `join`** / 临界区**未加锁**。
14. 模板实现放 `.cpp` 导致**链接错误**（应放 `.h`）。
15. 派生类**直接访问基类 `private` 成员**（应改 `protected` 或经成员函数）。

---

## 六、手写代码"默写清单"（建议每条脱稿写一遍）

按出题概率排序：
1. **MyString / String 四件套**：构造（深拷贝资源）+ 拷贝构造 + `operator=`（自赋值检查/`delete[]`/`return *this`）+ 析构。
2. **ToyPtr 智能指针模板**（构造接管、析构 `delete`、重载 `*` 与 `->`）。
3. **RAII 资源包装类**（文件/内存/锁：构造获取、析构释放）。
4. **链表实现的 Stack 类**（含归还结点的析构函数）。
5. **派生类的拷贝构造 + 赋值运算符**（显式调用基类 `:A(b)` / `*(A*)this=b`）。
6. **重载 `new`/`delete`**（清零初始化或自由空间链表骨架）。
7. **Complex 复数类**：`+`/`==`/`!=`/取负，含友元版"实数+复数"。
8. **Counter 类**：`++` 前置（返 `Counter&`）/后置（`operator++(int)` 返旧值）。
9. **类模板 Stack&lt;T&gt;**（含成员函数类外实现写法）。
10. **抽象类 Shape/Figure + 派生 + 多态循环**。
11. **线程安全累加**（`thread` + `lock_guard`/`mutex` + `join`）。

---

## 七、复习时间分配建议

| 时段 | 模块 | 建议动作 |
|------|------|----------|
| 第 1 天 | 拷贝构造/深浅拷贝 + 构造析构调用顺序 | 反复手写 String 四件套；画构造/析构调用链并默写输出 |
| 第 2 天 | 虚函数动态绑定 + 派生类初始化/拷贝/赋值 | 把"虚/非虚混合调用"分析题练熟；练 `:A(b)` 与 `*(A*)this=b` |
| 第 3 天 | 内存安全 + RAII + 智能指针 + 并行 | 引用计数逐行推导；默写 ToyPtr / RAII；写线程安全累加 |
| 第 4 天 | `new`/`delete` 重载 + 异常处理 + 聚合组合 | 默写清零版 new/delete；练嵌套异常匹配；判断聚合/组合 |
| 第 5 天 | 第二梯队（操作符/友元/模板/STL/static/const）+ 全套陷阱清单 | 以纠错和概念题为主，过一遍即可 |
| 考前一天 | 见下一节"考前最后一天必过清单" | 形成肌肉记忆 |

---

## 八、考前最后一天必过清单

> 只看这一节也能稳住基本盘。分三块：**能默写的代码、能脑中跑出来的程序、能背熟的纠错陷阱。**

### 8.1 必须能默写的代码

- [ ] **String / MyString 四件套**：构造（`new char[len+1]` + `strcpy`）、拷贝构造（深拷贝）、`operator=`（自赋值检查 + `delete[]` + 重新分配 + `return *this`）、析构（`delete[]`）。
- [ ] **派生类拷贝构造 + 赋值**：`Derived(const Derived& d): Base(d) {...}`；`operator=` 中 `if(&d==this) return *this; Base::operator=(d); ...; return *this;`。
- [ ] **`new`/`delete` 重载**：`void* operator new(size_t size){ void* p=malloc(size); memset(p,0,size); return p; }`、`void operator delete(void* p){ free(p); }`。
- [ ] **ToyPtr 智能指针模板**：构造接管、析构 `delete`、`T& operator*()`、`T* operator->()`。
- [ ] **RAII 包装类**：构造 `fopen`/获取资源，析构 `fclose`/释放资源。
- [ ] **线程安全累加**：`thread t(add,n)` → `lock_guard<mutex> lk(mtx)` 保护 `total++` → `t.join()`。
- [ ] **Counter 的 `++`**：前置 `Counter& operator++(){ value++; return *this; }`；后置 `const Counter operator++(int){ Counter t=*this; value++; return t; }`。

### 8.2 必须能在脑中"跑出来"的程序

- [ ] **构造/析构调用顺序**：含成员对象 + 继承时，构造 `基类 → 成员对象（按声明序）→ 派生类`，析构严格逆序。能写出带 `cout` 程序的完整输出。
- [ ] **虚函数调用判定**：`A* p = new B;` 后，`p->虚函数` → 派生类版本；`p->非虚函数` → 基类版本；**构造/析构中调虚函数** → 当前类版本。能逐行写出调用谁。
- [ ] **`shared_ptr` 引用计数**：拷贝/赋值 +1、出作用域 -1，逐行标注计数，归 0 释放。能写出每行 `use_count()`。
- [ ] **异常匹配顺序**：`throw` 类型 → 最内层 `try` 的 `catch` 按序匹配 → 不匹配则退栈到调用者继续找。能判断某 `throw` 由哪层捕获（注意 `"abc"` 是 `const char*`）。
- [ ] **拷贝 vs 赋值**：`A b=a;`/`A b(a);` 调拷贝构造；`b=a;` 调 `operator=`。
- [ ] **向上/向下转换**：派生→基类（赋值、指针指向）合法；基类→派生通常非法。

### 8.3 必须背熟的纠错陷阱（口诀式）

- [ ] **浅拷贝**：有裸指针就要"拷贝构造 + 赋值 + 析构"配套深拷贝。
- [ ] **`+1`**：`new char[len+1]` 给 `'\0'` 留位。
- [ ] **`delete` vs `delete[]`**：`new[]` 必配 `delete[]`。
- [ ] **虚析构**：可能被基类指针删除的类，基类析构设 `virtual`。
- [ ] **派生类自定义拷贝/赋值漏调基类**：拷贝 `:Base(d)`、赋值 `Base::operator=(d)`。
- [ ] **构造/析构里虚调用不动态绑定**。
- [ ] **`unique_ptr` 不可拷贝/赋值**：用 `std::move`。
- [ ] **同一裸指针别构造两个 `shared_ptr`**：会重复释放；要通过拷贝共享。
- [ ] **循环引用用 `weak_ptr` 打破**。
- [ ] **组合析构要 `delete`，聚合析构不要 `delete`**。
- [ ] **成员初始化按声明顺序**；`const`/引用成员必须初始化表初始化。
- [ ] **`catch` 类型要与 `throw` 匹配**；`throw`/`return` 后无多余代码。
- [ ] **多线程要 `join`，临界区要加锁**。
- [ ] **模板定义放头文件**，否则链接错误。

---

### 一句话总结
红色考点决定大题，黑色考点决定小题与纠错点。三种题型的素材大多来自 PPT 现成代码的"换皮、挖空、改错、补全"。把第一梯队的几段经典代码练到能脱稿手写、能逐行跑程序、能一眼挑错，就能覆盖绝大多数考点。

---

### 第二梯队展开版：基础知识框架与易错点

> 这一部分主要服务于**小题、概念题、判断题、纠错题**。不需要像第一梯队那样重点练三道完整大题，但要能做到：看见代码知道考点，看见错误能说出原因和改法。

#### 1. 常成员函数与 `const` 相关

**基础框架**

- `const` 数据成员必须在**初始化列表**中初始化，不能在构造函数体内赋值。
  ```cpp
  class A {
      const int x;
  public:
      A(int a) : x(a) {}   // 正确
  };
  ```
- 构造函数体内的语句是“赋值”，不是“初始化”。
  ```cpp
  A(int a) {
      x = a;               // 错，const 成员不能被赋值
  }
  ```
- 不修改对象内容的成员函数应写成 `const` 成员函数。
  ```cpp
  int getX() const { return x; }
  void print() const { cout << x; }
  ```
- `const` 成员函数中不能修改普通数据成员。
  ```cpp
  void f() const {
      // x = 10;           // 错
  }
  ```
- `const` 对象只能调用 `const` 成员函数。
  ```cpp
  const A a;
  a.print();               // print 是 const 成员函数才可以
  ```
- 拷贝构造和赋值运算符参数一般写成 `const 引用`：
  ```cpp
  A(const A &a);
  A& operator=(const A &a);
  ```

**易错点**

- 把 `const` 成员放到构造函数体内赋值。
- 忘记给查询函数加 `const`，导致 `const` 对象不能调用。
- 以为 `const` 成员函数里什么都不能做。其实可以读数据，也可以修改指针指向的内容，但不能修改指针成员本身。
  ```cpp
  class A {
      char *p;
  public:
      void f() const {
          p[0] = 'x';      // 可能可以：改的是 p 指向的内容
          // p = nullptr;  // 错：改的是成员 p 本身
      }
  };
  ```
- 含 `const` 数据成员的类，默认赋值运算符可能不可用，因为对象构造完成后 `const` 成员不能再改。

#### 2. 静态成员与静态成员函数

**基础框架**

- `static` 数据成员属于**类本身**，所有对象共享一份。
  ```cpp
  class A {
      static int count;
  public:
      A() { count++; }
      ~A() { count--; }
      static int getCount() { return count; }
  };
  ```
- 静态数据成员通常要在类外定义一次：
  ```cpp
  int A::count = 0;
  ```
- 静态成员函数没有 `this` 指针，只能直接访问静态成员。
  ```cpp
  static int getCount() {
      return count;        // 可以
      // return x;         // 错，x 若是普通成员则不能直接访问
  }
  ```
- 静态成员可以通过类名访问：
  ```cpp
  A::getCount();
  ```

**易错点**

- 只在类内声明 `static int count;`，忘记类外定义，导致链接错误。
- 在静态成员函数里直接访问普通成员变量。
- 以为每个对象都有一份静态成员。实际上所有对象共享一份。
- 对象计数器题中，构造函数 `count++`，析构函数 `count--`，要注意临时对象、拷贝对象也会影响计数。

#### 3. 抽象类与纯虚函数

**基础框架**

- 纯虚函数写法：
  ```cpp
  virtual void draw() = 0;
  ```
- 含有纯虚函数的类是抽象类，不能直接创建对象。
  ```cpp
  class Shape {
  public:
      virtual double area() = 0;
  };

  // Shape s;              // 错，抽象类不能实例化
  ```
- 派生类必须实现所有纯虚函数，才可以创建对象。
  ```cpp
  class Circle : public Shape {
  public:
      double area() { return 3.14; }
  };
  ```
- 抽象类常用来提供统一接口，配合基类指针/引用实现多态。
  ```cpp
  Shape *p = new Circle;
  p->area();               // 调 Circle::area
  ```

**易错点**

- 抽象类不能创建对象，但可以定义抽象类指针或引用。
  ```cpp
  Shape *p;                // 可以
  Shape &r = obj;          // 可以，前提 obj 是具体派生类对象
  ```
- 派生类只要还有一个纯虚函数没实现，它仍然是抽象类。
- 作为多态基类时，析构函数最好写成虚析构函数。
  ```cpp
  virtual ~Shape() {}
  ```

#### 4. 基本操作符重载

**基础框架**

- 操作符重载本质是函数调用。
  ```cpp
  c1 + c2
  ```
  可以理解为：
  ```cpp
  c1.operator+(c2)
  ```
  或：
  ```cpp
  operator+(c1, c2)
  ```
- 成员函数重载时，左操作数是当前对象 `*this`。
  ```cpp
  Complex operator+(const Complex &c) const;
  ```
- 全局/友元函数重载时，左右操作数都作为参数传入。
  ```cpp
  friend Complex operator+(double x, const Complex &c);
  ```
- 如果左操作数不是本类对象，通常不能用成员函数，只能用全局函数。
  ```cpp
  3.0 + c;                 // 左边是 double，不能调用 c 的成员函数
  ```
- `operator=`、`operator[]`、`operator()`、`operator->` 必须或通常作为成员函数实现。

**易错点**

- `c + 3.0` 和 `3.0 + c` 不一样。前者可以靠成员函数，后者通常需要全局/友元函数。
- `operator+` 一般不修改原对象，常返回新对象。
  ```cpp
  Complex operator+(const Complex &c) const;
  ```
- `operator==` 返回 `bool`，不要返回对象。
- 赋值运算符 `operator=` 返回 `A&`，并且返回 `*this`，支持连续赋值。
- 不要滥用操作符重载，含义应符合直觉。

#### 5. 前置 `++` 与后置 `++`

**基础框架**

- 前置 `++a`：先加，再返回当前对象。
  ```cpp
  Counter& operator++() {
      value++;
      return *this;
  }
  ```
- 后置 `a++`：先保存旧值，再加，返回旧值。
  ```cpp
  const Counter operator++(int) {
      Counter old = *this;
      value++;
      return old;
  }
  ```
- 后置 `++` 的 `int` 参数只是占位，用来区分前置和后置，调用时不用传。

**易错点**

- 前置 `++` 应返回引用 `Counter&`，因为返回的是当前对象本身。
- 后置 `++` 应返回旧值，不能返回加完后的对象引用。
- 后置 `++` 多一次临时对象拷贝，效率通常低于前置 `++`。
- `++(++a)` 通常可以；`(a++)++` 通常不应该允许，所以后置常返回 `const Counter`。

#### 6. `[]`、`()`、`->` 重载

**基础框架**

- `operator[]` 常用于数组、向量、字符串等类。
  ```cpp
  int& operator[](int i) { return data[i]; }
  const int& operator[](int i) const { return data[i]; }
  ```
- 非 `const` 版本返回引用，允许修改：
  ```cpp
  v[0] = 10;
  ```
- `const` 版本用于 `const` 对象，只允许读取。
- `operator()` 让对象像函数一样调用，形成函数对象 functor。
  ```cpp
  class Add {
  public:
      int operator()(int a, int b) { return a + b; }
  };
  ```
- `operator->` 常用于智能指针类，让对象像指针一样访问成员。
  ```cpp
  T* operator->() { return ptr; }
  ```

**易错点**

- `operator[]` 如果返回普通值，则 `v[0] = 10;` 不能正常修改原数组元素。
- 忘记写 `const` 版本，导致 `const` 容器对象不能下标访问。
- `operator()` 不是构造函数，它只是函数调用运算符。
- `operator->` 返回值通常应是指针或另一个重载了 `->` 的对象。

#### 7. 友元

**基础框架**

- 友元函数不是成员函数，但可以访问类的 `private` 和 `protected` 成员。
  ```cpp
  class A {
      int x;
      friend void show(const A &a);
  };
  ```
- 友元常用于需要访问私有成员的全局操作符重载。
  ```cpp
  friend ostream& operator<<(ostream &out, const A &a);
  ```
- 友元关系由类主动声明。

**易错点**

- 友元不是成员函数，没有 `this` 指针。
- 友元不受 `public/private/protected` 区域影响，写在哪个区域效果一样。
- 友元关系不对称：A 是 B 的友元，不代表 B 是 A 的友元。
- 友元关系不传递：A 友元 B，B 友元 C，不代表 A 友元 C。
- `operator<<` 通常不能写成普通成员函数，因为左操作数是 `ostream`，不是本类对象。

#### 8. 模板

**基础框架**

- 函数模板：
  ```cpp
  template <class T>
  T maxValue(T a, T b) {
      return a > b ? a : b;
  }
  ```
- 类模板：
  ```cpp
  template <class T>
  class Stack {
      T data[100];
  public:
      void push(T x);
  };
  ```
- 类模板成员函数类外实现要带模板头：
  ```cpp
  template <class T>
  void Stack<T>::push(T x) { }
  ```
- 非类型模板参数：
  ```cpp
  template <class T, int size>
  class Array {
      T data[size];
  };
  ```
- 显式指定模板参数：
  ```cpp
  maxValue<double>(1, 2.5);
  ```

**易错点**

- 模板不是具体函数/类，只有实例化后才生成具体代码。
- 模板定义通常要放在头文件中，不能只把声明放 `.h`、实现放 `.cpp`，否则可能链接错误。
- 类模板使用时必须给出模板参数：
  ```cpp
  Stack<int> s;
  ```
- 类外实现时容易漏写 `template<class T>` 或 `Stack<T>::`。
- 函数模板实参类型推导要求类型能匹配；`maxValue(1, 2.5)` 可能推导失败，需要显式写 `maxValue<double>(1, 2.5)`。

#### 9. STL：容器、迭代器、算法

**基础框架**

- STL 三件套：容器、迭代器、算法。
  ```cpp
  vector<int> v;
  sort(v.begin(), v.end());
  ```
- 常见容器：
  - `vector`：动态数组，支持下标，尾部插入快。
  - `list`：双向链表，不支持随机下标访问。
  - `map`：键值对，按 key 查找。
  - `set`：集合，元素不重复。
- 常见算法：
  ```cpp
  sort(v.begin(), v.end());
  accumulate(v.begin(), v.end(), 0);
  for_each(v.begin(), v.end(), func);
  ```
- 迭代器类似泛化指针：
  ```cpp
  for (auto it = v.begin(); it != v.end(); ++it) {
      cout << *it;
  }
  ```

**易错点**

- `sort` 需要随机访问迭代器，常用于 `vector`，不能直接用于 `list`。
- `v.end()` 指向最后一个元素的后一个位置，不能解引用。
- 容器下标从 0 开始。
- `map` 中 `m[key]` 如果 key 不存在，会插入默认值。
- 算法通常不直接知道容器，只通过迭代器区间工作。

#### 10. `this` 指针

**基础框架**

- 非静态成员函数内部隐含一个 `this` 指针，指向当前对象。
  ```cpp
  class A {
      int x;
  public:
      void set(int x) {
          this->x = x;
      }
  };
  ```
- 普通成员函数中，`this` 类型可理解为：
  ```cpp
  A* const this
  ```
  即 `this` 指针本身不能改，但可以通过它修改对象。
- `const` 成员函数中，`this` 类型可理解为：
  ```cpp
  const A* const this
  ```
  即不能通过 `this` 修改对象。
- 需要返回当前对象时常用：
  ```cpp
  return *this;
  ```
- 需要把当前对象地址传出去时用：
  ```cpp
  func(this);
  ```

**易错点**

- 静态成员函数没有 `this` 指针。
- `this` 是指针，`*this` 才是当前对象本身。
- `return this;` 返回的是当前对象地址，类型是 `A*`；`return *this;` 返回当前对象本身，常用于返回 `A&`。
- 自赋值检查应写：
  ```cpp
  if (this == &other) return *this;
  ```
  不是比较内容是否相等。

#### 第二梯队总口诀

> `const` 看能不能改，`static` 看有没有 `this`；抽象类看纯虚，操作符看左操作数；友元不是成员，模板定义放头文件；STL 看容器-迭代器-算法，`this` 是当前对象地址。第二梯队不一定出大题，但很容易以“判断合法性、填空、改错、解释原因”的形式出现。
