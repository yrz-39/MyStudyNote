# 完成PA必要的QT语法学习
## 1.QGraphicsView / QGraphicsScene / QGraphicsObject
- 棋盘、单位、装备、商店卡牌、血条蓝条
```cpp
QGraphicsView   // 视图，像摄像机 / 窗口
QGraphicsScene  // 场景，管理所有图元
QGraphicsItem   // 图元，棋盘格、单位、装备、按钮都可以是图元
```
### 自定义图元
```cpp
class MyItem: public QGraphicsObject{
	QRectF boundingRect() const override;//图元占多大范围
	void paint(QPainter* painter,const QStyleOptionGraphicsItem* option,
	QWidget* widget) override;//绘制函数
};
然后通过 my_scene->addItem(自定义图元对象)加入到场景中
```

## 2.信号槽 signals / slots / connect
- **在这个项目中信号槽的作用就是接收用户操作->自动通知相关程序来处理 如鼠标拖拽操作，点击操作等
```cpp
// ① 声明信号（在 .h 的 signals: 区）
signals:
    void somethingHappened(int data);

// ② 发射信号（在 .cpp 里）
emit somethingHappened(42);

// ③ 连接信号和槽
connect(sender, &Sender::signal, receiver, &Receiver::slot);
```

## 3.鼠标操作
- 备战区 ↔ 棋盘拖拽
- 装备栏 -> 单位拖拽
- 商店点击购买
- 单位点击显示属性面板
```cpp
event->pos();       // 图元自身坐标
event->scenePos();  // 场景坐标
event->screenPos(); // 屏幕坐标
```

## 4.坐标类 QPoint / QPointF / QRectF / QPolygonF
### 1.QPoint 整数坐标，适合表示棋盘格
```cpp
QPoint pos(2, 5);
pos.x(); // 列
pos.y(); // 行
```
### 2.QPointF 浮点坐标，适合表示屏幕/场景位置
```cpp
QPointF center(100.5, 230.0);
//把棋盘格转成场景坐标。
QPointF Game::gridToWorld(int row, int col) const
```
### 3.QRectF 矩形区域 用于图元边界，血条，蓝条，按钮背景，属性面板
```cpp
QRectF(x, y, width, height)
painter->drawRect(QRectF(-30, -45, 60, 6));
```

## 5.QPainter绘制语法
```cpp
painter->setPen(QPen(Qt::white, 2));   // 线条
painter->setBrush(QBrush(Qt::gray));   // 填充
painter->drawRect(...);                // 矩形
painter->drawEllipse(...);             // 圆/椭圆
painter->drawText(...);                // 文字
painter->drawPixmap(...);              // 图片
//画完后，只要单位属性变化，调用
unitItem->update();
```
## 6.QTimer
- 自动战斗 移动 攻击 施法，每隔一小段时间调用Game::updateFrame()
## 7.按钮，标签，布局 QWidget / QLabel / QPushButton / QLayout
```cpp
m_resetButton = new QPushButton("Reset", this);
connect(m_resetButton, &QPushButton::clicked,
        this, &GameWindow::onResetButtonClicked);
```
- 按钮用QPushButton 显示标签用QLabel
### 1.QLabel 显示状态
```cpp
QLabel* goldlabel;
m_goldLabel->setText(QString("Gold:%1").arg(m_game->gold()));
//QString("Gold:%1").arg(value)类似C++的格式化字符串
```
### 2.布局
```cpp
QVBoxLayout：竖着排
QHBoxLayout：横着排
//例如底边加控制栏
QWidget* controlBar = new QWidget(this);
QHBoxLayout* controlLayout = new QHBoxLayout(controlBar);

controlLayout->addWidget(m_resetButton);
controlLayout->addWidget(m_startButton);
controlLayout->addWidget(m_goldLabel);
controlLayout->addStretch();
```
