---
tags: [DLCO, CPU, 习题, 期末考试]
aliases: [多周期CPU习题, 多周期练习题]
---

# 多周期CPU设计 — 典型习题集

> ⚠️ **先通读 [[多周期CPU设计复习]]**，再做习题检验理解。

---

## 题型1：状态转移与控制信号

### 题1.1 

多周期 CPU 当前处于 **State 1 (RFetch/ID)**，opcode 为 `0110011`（R-type）。

1. 下一状态是什么？
2. 在 State 1 中，以下控制信号的值是什么？
   - MARWr =
   - Add1MUX =
   - Add2MUX =
   - IRWr =

<details>
<summary>💡 答案</summary>

1. 下一状态 = **State 4 (RExec, 0100)**
2. 
   - MARWr = **1**（RFetch 阶段需要计算地址）
   - Add1MUX = **1**（选 rs1）
   - Add2MUX = **0**（选 0）
   - IRWr = **0**（IFetch 阶段才写 IR）
</details>

---

### 题1.2

假设多周期 CPU 正在执行 `lw x10, 24(x11)`，当前处于 **State 8 (lwExec)**。

1. 下一状态是什么？
2. 此时以下控制信号如何设置？
   - MARout =
   - MDRMUX =
   - MDRWr =
   - MemWr =

<details>
<summary>💡 答案</summary>

1. 下一状态 = **State 9 (lwFinish, 1001)**
2. 
   - MARout = **1**（将 MAR 地址送到地址总线）
   - MDRMUX = **0**（数据来自数据存储器输出，非 B 总线）
   - MDRWr = **1**（读内存结果存入 MDR）
   - MemWr = **0**（读操作）
</details>

---

### 题1.3

比较 `sw` 指令的 swExec (State 6) 和 swFinish (State 7) 两个状态的控制信号差异。

<details>
<summary>💡 答案</summary>

| 信号 | State 6 (swExec) | State 7 (swFinish) |
|-----|-----------------|-------------------|
| **MDRMUX** | 1 (选B总线) | × |
| **MDRWr** | 1 (B→MDR) | 0 |
| **MARout** | 0 | 1 (地址送总线) |
| **MemWr** | 0 | 1 (写内存) |

**解释**：swExec 将 B 的数据暂存到 MDR，swFinish 将 MDR 写回内存。
</details>

---

## 题型2：RTL 微操作写出

### 题2.1

写出 R-type 指令 `add x5, x6, x7` 在多周期 CPU 中每个时钟周期的完整 RTL 操作。

<details>
<summary>💡 答案</summary>

```
状态0 (IFetch):  IR ← M[PC]
                 PC ← PC + 4

状态1 (RFetch):  A ← R[x6]         // rs1
                 B ← R[x7]         // rs2
                 MAR ← A + SEXT(imm)

状态4 (RExec):   ALUout ← A + B    // add 操作
                 CC ← ALU flags

状态5 (RFinish): R[x5] ← ALUout    // rd 写回
                 → 回 State 0
```
</details>

---

### 题2.2

写出 `jal x1, label` 指令在多周期 CPU 中的完整 RTL 操作。（PC 已提前到 PC+4）

<details>
<summary>💡 答案</summary>

```
状态0 (IFetch):  IR ← M[PC]
                 PC ← PC + 4

状态1 (RFetch):  A ← R[x1]  (rs1, 虽然没用)
                 B ← R[0]   (rs2, 惯例)
                 MAR ← A + SEXT(imm)

状态2 (JFinish): R[x1] ← PC          // 保存 PC+4 作为返回地址
                 PC ← PC + SEXT(immJ) // 跳转目标
                 → 回 State 0
```
</details>

---

### 题2.3

`sw x8, 40(x9)` — 写出完整 RTL。

<details>
<summary>💡 答案</summary>

```
状态0 (IFetch):  IR ← M[PC]
                 PC ← PC + 4

状态1 (RFetch):  A ← R[x9]
                 B ← R[x8]
                 MAR ← A + SEXT(40)

状态6 (swExec):  MDR ← B

状态7 (swFinish): M[MAR] ← MDR
                  → 回 State 0
```
</details>

---

## 题型3：FSM 状态图设计

### 题3.1

画出多周期 CPU 的有限状态机状态转移图，要求：
1. 标注每个状态的编码（4位二进制）
2. 标注转移条件
3. 标注每种指令的路径

> 参考 [[多周期CPU设计复习#5.2 完整状态转移图]]

---

### 题3.2

**扩展题**：假如需要增加一条新指令 `mul rd, rs1, rs2`（乘法），需要 2 个周期完成乘法运算。如何扩展 FSM？

<details>
<summary>💡 思路</summary>

**方案**：在 RExec 后增加一个状态 State_10 (MulExec2)
```
原 R-type: 0→1→4→5→0
新 mul:    0→1→4→10→5→0（5周期）
```

或者修改控制逻辑，在 RExec 中根据 funct7 判断是否为 mul，如果是则下一状态指向新状态。

新增状态 State_10 的控制信号：
- ALUoutWr = 1（第二次乘法结果写入）
- 下一状态 → S5
</details>

---

## 题型4：性能计算

### 题4.1

某多周期 CPU 的各部件延迟如下：

| 部件 | 延迟 |
|------|------|
| IM | 150ps |
| ALU | 80ps |
| DM | 150ps |
| RegFile (读+写) | 80ps |
| PC+4 加法器 | 40ps |
| MUX/控制逻辑 | 30ps |
| 寄存器 clk-to-Q | 40ps |
| 寄存器 setup | 30ps |

指令混合比及 CPI：

| 指令 | 比例 | 多周期 CPI |
|------|------|-----------|
| R-type | 40% | 4 |
| I-type | 15% | 4 |
| lw | 20% | 5 |
| sw | 10% | 4 |
| beq | 10% | 3 |
| jal | 5% | 3 |

**求**：
1. 多周期 CPU 的时钟周期
2. 平均 CPI
3. 单周期 CPU 的时钟周期
4. 两种设计每指令执行时间之比

<details>
<summary>💡 答案</summary>

**1. 多周期时钟周期 = 最长单步延迟**

各步骤可能延迟：
- IM读 = 150 + 控制延迟 ≈ 180ps
- ALU = 80 + 30 + 40 + 30 ≈ 180ps
- DM读 = 150 + 40 + 30 = 220ps
- Reg读 = 80 + 30 = 110ps

最长 = **DM 访问** 或 **IM 访问**（哪个大取哪个）
T_multi = max(IM, ALU, DM, Reg) + clk-to-Q + setup

T_multi = **150 + 40 + 30 = 220ps**（取最长部件+寄存器开销）
或更精细：控制延迟可以重叠，实际考试中看给定方法。

**2. 平均 CPI**

CPI_avg = 40%×4 + 15%×4 + 20%×5 + 10%×4 + 10%×3 + 5%×3
        = 1.6 + 0.6 + 1.0 + 0.4 + 0.3 + 0.15
        = **4.05**

**3. 单周期时钟周期**

lw 路径：
  PC(clk-to-Q=40) → IM(150) → RegRead(80) → MUX(30) → ALU(80) → DM(150) → MUX(30) → RegSetup(30)
  = 40 + 150 + 80 + 30 + 80 + 150 + 30 + 30 = **590ps**

**4. 性能比较**

单周期: 1 × 590 = 590 ps/指令
多周期: 4.05 × 220 = 891 ps/指令

多周期/单周期 = 891/590 = **1.51x**（多周期慢 51%）
</details>

---

### 题4.2

假设工艺进步，IM 和 DM 的延迟从 200ps 降到了 80ps，其他不变。重新分析上题的性能对比（定性分析即可）。

<details>
<summary>💡 答案</summary>

**定性分析**：
- 单周期的时钟周期**大幅缩短**（因为 IM 和 DM 不再是最长的瓶颈）
- 多周期的时钟周期也缩短但**收益较小**（因为其他部件 ALU/MUX 可能成为新瓶颈）
- **结论**：当 IM/DM 加速时，单周期比多周期受益更大，单周期的性能优势更明显。

定量：
- 新 T_multi = max(80, 80, 80, 80) + 70 = **150ps**
- 新 T_single = 40 + 80 + 80 + 30 + 80 + 80 + 30 + 30 = **450ps**
- 多周期: 4.05 × 150 = 607.5 ps/指令
- 单周期: 1 × 450 = 450 ps/指令
- 多周期/单周期 = 607.5/450 = 1.35x

> 相比之前 1.51x，差距缩小了！因为 IM/DM 不再是最大瓶颈。
</details>

---

## 题型5：概念对比

### 题5.1

比较单周期 CPU 和多周期 CPU 在以下方面的异同：
1. CPI
2. 时钟周期
3. 硬件资源利用率
4. 设计复杂度

<details>
<summary>💡 答案</summary>

| 方面 | 单周期 | 多周期 |
|------|--------|--------|
| **CPI** | 固定为 1 | 3~5（不同指令不同） |
| **时钟周期** | 长（由最慢指令决定） | 短（由最长微步决定） |
| **硬件利用率** | 低（每周期大量闲置） | 高（部件多次复用） |
| **设计复杂度** | 低（简单控制） | 高（需要 FSM/微程序） |
| **面积** | 大（需独立加法器） | 小（共享 ALU 做 PC+4） |
</details>

---

### 题5.2

硬连线控制（PLA）和微程序控制（ROM）各有何优缺点？RV32I 适合用哪种？

<details>
<summary>💡 答案</summary>

| 方面 | 硬连线(PLA) | 微程序(ROM) |
|------|------------|-------------|
| 速度 | 快 | 慢 |
| 修改难度 | 需重新综合逻辑 | 只需改 ROM 内容 |
| 面积 | 小 | 大 |
| 易于扩展 | 难 | 易 |

**RV32I 适合硬连线控制**，因为：
- 指令集规整，状态数少
- 追求性能和面积效率
- 不需要频繁修改指令集

而 CISC（如 x86）适合微程序控制，因为指令复杂且需要兼容旧指令。
</details>

---

### 题5.3

为什么多周期 CPU 需要 IR、MAR、MDR、ALUout 等寄存器？它们分别在第几周期被写入和读取？

<details>
<summary>💡 答案</summary>

因为这些寄存器用于在**不同时钟周期之间保存中间结果**。单周期中组合逻辑的输出在同一周期内直接使用，而多周期中需要跨周期保存。

| 寄存器 | 写入周期 | 读取周期 | 作用 |
|-------|---------|---------|------|
| **IR** | S0 (IFetch) | S1~S9 | 指令译码 |
| **MAR** | S1 (RFetch) | S7/S8 (swFin/lwExec) | 访存地址 |
| **MDR** | S6(swExec)/S8(lwExec) | S7(swFin)/S9(lwFin) | 访存数据中转 |
| **ALUout** | S3(IExec)/S4(RExec) | S5(RFin/IFin) | ALU结果暂存 |
| **CC** | S3/S4 | 异常检测 | 条件标志 |
</details>

---

## 题型6：异常处理

### 题6.1

描述多周期 CPU 检测到**算术溢出**后的处理流程，包括 RTL 操作和控制信号。

<details>
<summary>💡 答案</summary>

**检测**：在 IExec 或 RExec 阶段，ALU 运算后 CC（条件码）寄存器中的溢出标志 OF 置 1。

**处理流程**：

```
假设在 S4 (RExec) 检测到溢出:

S_Exception (新增状态):
  EPC ← PC - 4          // 保存当前指令地址（PC已在IFetch加了4）
  Cause ← 2             // 溢出异常编码
  PC ← 0x10000          // 跳转到异常处理程序入口
  → 回 S0 (IFetch)
```

**控制信号**：
```
EPCWr   = 1
CauseWr = 1
CauseMUX = 1（选 Cause=2）
PCMUX   = 0（入口地址）
Add1MUX = 0
Add2MUX = 10（选 0x10000）
PCWr    = 1
```
</details>

---

### 题6.2

当 CPU 发现 opcode 不可识别时，应该如何处理？与溢出处理有何不同？

<details>
<summary>💡 答案</summary>

**检测时机**：在 S1 (RFetch/ID) 阶段，控制逻辑对 opcode 译码时发现没有匹配的指令。

**不同点**：
1. **检测阶段不同**：未定义在译码阶段（S1），溢出在执行阶段（S3/S4）
2. **Cause 编码不同**：未定义指令 → Cause=1，溢出 → Cause=2
3. **EPC 值保持一致**：两者都是 PC-4（PC 已经在 IFetch 阶段加了 4）

**处理流程**（控制信号与溢出类似，仅 CauseMUX 不同）：
```
EPCWr   = 1
CauseWr = 1
CauseMUX = 0（选 Cause=1）
PCMUX   = 0
Add1MUX = 0
Add2MUX = 10（选 0x10000）
PCWr    = 1
```
</details>

---

## 题型7：综合设计题

### 题7.1

某多周期 CPU 在执行 `beq x5, x6, offset` 时，当前状态为 **State 0**（即将进入 State 1），请：

1. 说明 beq 的完整执行过程（各周期 RTL）
2. 在哪个周期完成分支判断？
3. 如果分支判断结果为"跳转"，PC 如何更新？如果"不跳转"呢？

<details>
<summary>💡 答案</summary>

**1. RTL：**
```
S0 (IFetch):    IR ← M[PC]
                PC ← PC + 4

S1 (RFetch):    A ← R[x5]
                B ← R[x6]
                MAR ← A + SEXT(offset)

S? (BExec):     ALUout ← A - B      // sub 比较
                CC ← ALU flags
                if (Zero == 1):     // 相等
                    PC ← PC + SEXT(immB) 
                // 否则 PC ← PC (保持 PC+4)
                
(有些设计中 BExec 和 S1 合并)
→ 回 S0
```

**2. 分支判断**在**执行阶段**完成（State 4 或专用状态），通过 ALU sub 操作和 Zero 标志。

**3. PC 更新逻辑**：
- **跳转 (相等)**：PC ← (PC+4) + SEXT(immB)，即相对 PC+4 的偏移
- **不跳转 (不等)**：PC 保持 PC+4（IFetch 阶段已经加了 4）
</details>

---

### 题7.2

设计题：请设计一个简化的多周期 CPU 控制器 FSM，支持以下 3 种指令：
- `add rd, rs1, rs2`（R-type, op=000000）
- `lw rd, imm(rs1)`（op=100011）
- `beq rs1, rs2, imm`（op=000100）

要求给出：
1. 状态转移图
2. 控制信号表达式（PCWr, IRWr, RegWr, MemWr, ALUctr）

<details>
<summary>💡 答案</summary>

**1. 状态转移图：**

```
        ┌──────────────────────────┐
        │                          │
        ↓                          │
     ┌──────┐      ┌──────────┐    │
     │  S0  │─────→│    S1    │    │
     │IFetch│      │RFetch/ID │    │
     └──────┘      └──┬───────┘    │
        ↑             │    │   │   │
        │     op=000100 │    │   │  │
        │       (beq)   │    │   │  │
        │              ↓    │   │  │
        │         ┌─────┐   │   │  │
        │         │S_Br │   │   │  │
        │         │Exec │   │   │  │
        │         └──┬──┘   │   │  │
        │            │      │   │  │
        │      op=000000 │  │   │  │
        │       (add)   ↓  │   │  │
        │         ┌─────┐  │   │  │
        │         │S_Exe│  │   │  │
        │         │RExec│  │   │  │
        │         └──┬──┘  │   │  │
        │            │     │   │  │
        │         ┌──┴──┐  │   │  │
        │         │S_WB │←┘   │  │
        │         │WrBk │     │  │
        │         └──┬──┘     │  │
        │  op=100011 │        │  │
        │   (lw)    ↓        │  │
        │         ┌────┐     │  │
        │         │S_lw│     │  │
        │         │Exec│     │  │
        │         └─┬──┘     │  │
        │           ↓       │  │
        │         ┌────┐    │  │
        │         │S_lw│    │  │
        │         │ WB │    │  │
        └─────────┴────┘    └──┘
```

**2. 控制信号表达式：**

```
PCWr     = S0 + S_Br (分支判断后更新 PC)
IRWr     = S0
RegWr    = S_WB + S_lwWB
MemWr    = 0 (简化模型无 sw)
ALUctr   = add 在大多数状态
           sub 在 S_Br（beq 比较）
```
</details>

---

## 复习自检清单

完成所有题目后，逐一确认：

- [ ] 能画出 FSM 完整状态转移图
- [ ] 能写出每种指令的 RTL 微操作
- [ ] 能填写任意状态的控制信号表
- [ ] 能计算 CPI 和性能对比
- [ ] 能说明硬连线 vs 微程序的区别
- [ ] 能描述异常处理流程
- [ ] 能设计简单 FSM 扩展新指令

> **关联笔记**：[[多周期CPU设计复习]] | [[DLCO笔记]] | [[02-学习/有限状态机]]
