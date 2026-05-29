# 1.构造函数顺序
- **虚基类->普通基类->成员变量->自己

| **内容** | **顺序由什么决定**        |
| ------ | ------------------ |
| 虚基类    | 由继承结构决定，最先构造，只构造一次 |
| 普通直接基类 | 由继承列表顺序决定          |
| 成员变量   | 由类中声明顺序决定          |
| 构造函数体  | 最后执行               |
- 注意：如果出现菱形继承问题，没有虚继承的情况下最终派生类中会有多份基类，有虚继承的话只有一份基类
```cpp
#include <iostream>
using namespace std;

class A {
public:
    A(int x) {
        cout << "A: " << x << endl;
    }
};

class B : virtual public A {
public:
    B() : A(1) {
        cout << "B\n";
    }
};

class C : virtual public A {
public:
    C() : A(2) {
        cout << "C\n";
    }
};

class D : public B, public C {
public:
    D() : A(100), B(), C() {
        cout << "D\n";
    }
};

int main() {
    D d;
}

```
 - 分析：首先看到main函数里，D是最终派生类，然后由于BC虚继承A **<font color="#ff0000">所以A是虚基类，由D最终构造A(100),BC构造函数列表中的A(1),A(2)被忽略</font>**，然后根据D继承顺序public B,public C,调用B,C的构造函数，所以最终输出
 ```cpp
 A:100
 B
 C
 D
 ```
 