# PA历程

## 0.前置 
[[QT语法学习]]
## 1.改动战斗区 将六边形格子改为方形
![[Pasted image 20260511151446.png]]
-  这是格子中心的坐标计算，QQointF是浮点数坐标
 ![[Pasted image 20260516180053.png]]
 ![[Pasted image 20260516180128.png]]
## 2.增加备战区 改动放置逻辑(比较简单 增加isBench()方法)
## 3.基础架构重铸
### 3.1 构建抽象基类UnitBase 
```cpp
// 纯虚接口

    virtual QString race() const = 0;                    // 种族名字

    virtual QString jobClass() const = 0;                // 职业名

    virtual QString skillName() const = 0;               // 技能名

    virtual std::unique_ptr<UnitBase> clone() const = 0; // 深拷贝

  

    virtual void takeDamage(int damage);     // 受到伤害，HP≤0 时自动切 DEAD

    virtual bool isAlive() const;            // HP > 0

    virtual void onAttack(UnitBase *target); // 普攻命中目标（造成 attack 伤害）

    virtual void castSkill(QVector<UnitBase *> &enemies,

                           QVector<UnitBase *> &allies) = 0; // 纯虚：释放技能

  

    virtual void updateState(qreal deltaTime);

  

  protected:

    // ---- 战斗属性（派生类构造函数中初始化）----

    int m_hp;

    int m_maxHp;

    int m_mp;

    int m_maxMp;

    int m_attack;

    int m_defense;

    qreal m_attackSpeed; // 攻击间隔（秒）

    int m_attackRange;   // 攻击距离（格子数）

    qreal m_moveSpeed;   // 移动速度（像素/秒）

  

    // ---- 状态机成员 ----

    UnitState m_state;

    UnitBase *m_currentTarget;

    qreal m_attackTimer; // 普攻冷却计时器（秒）

  

  private:

    static int s_nextId; // 全局自增 ID

  

    int m_id;

    QString m_name;

    int m_cost;

    QPoint m_position;

    int m_starLevel;
```
### 3.2 根据UnitBase 派生出6个种族 每个种族有自己的特性
### 3.3 增加泛型工具和异常处理
```cpp
clamp<T> //将val限制在[min,max]之间
distance(a,b) //计算欧几里得距离
manhattanDistance(a,b) //计算曼哈顿距离
findClosest //查找最近符合要求目标
findEnemiesInRange //查找距离内敌人
UnitFactory //单位工厂

//异常处理
1.棋盘位置非法
2.找不到指定单位
3.金币不足
4.备战区满了
5.非法操作
```
### 3.4 BFS寻路算法
- 基本四路：想象身处一个迷宫中，从(0,0)开始，沿四个方向像波纹一样一层一层扩散，直到波纹碰到终点->沿来路回溯->得到最短路径