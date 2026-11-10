# phase1-practice — 第一阶段练习项目

基于模拟传感器数据的数据清洗、统计分析与可视化练习，对应《新生进组前学习计划》第一阶段（第 1–5 周）。

## 项目内容

| 周次 | 主题 | 产出 |
|------|------|------|
| 第 1–2 周 | Python 基础语法、文件读写、Jupyter | 语法练习脚本 |
| 第 3 周 | NumPy / Pandas 数据清洗与统计 | `task3.py` → `data/cleaned_data.csv` |
| 第 4 周 | Matplotlib / Seaborn 可视化 | `week4_plot.py` → `figures/*.png` |
| 第 5 周 | Git 版本管理、项目整合 | 本仓库 |

## 目录结构

```
phase1-practice/
├── README.md
├── requirements.txt          # 依赖清单
├── .gitignore
├── make_sample_data.py       # 生成模拟传感器数据（含缺失/重复/异常值）
├── task3.py                  # 第 3 周：数据清洗与分析
├── week4_plot.py             # 第 4 周：绘制 6 张单图 + 1 张组合图
├── data/
│   ├── sensor_data.csv       # 原始数据（205 行 × 6 列，故意含脏数据）
│   └── cleaned_data.csv      # 清洗后数据（196 行 × 6 列）
└── figures/
    ├── fig1_line.png         # 折线图：温度随时间变化
    ├── fig2_scatter.png      # 散点图：温度-湿度关系
    ├── fig3_bar.png          # 柱状图：各类传感器记录数
    ├── fig4_hist.png         # 直方图 + KDE：温度分布
    ├── fig5_box.png          # 箱线图：分类别温度分布
    ├── fig6_heatmap.png      # 热力图：三指标相关系数
    └── report_figure.png     # 汇总图（2×3 子图，300 dpi）
```

## 运行环境

- Python 3.12（Anaconda3）
- 依赖安装：

```bash
pip install -r requirements.txt
```

## 如何运行

```bash
# 1. 生成练习数据（可选，仓库已包含 data/sensor_data.csv）
python make_sample_data.py

# 2. 数据清洗与分析
python task3.py

# 3. 生成全部图表（输出到 figures/）
python week4_plot.py
```

## 数据处理要点

- 原始数据 205 行，含 44 个缺失值、5 条完全重复行、4 个异常温度（-20.3 / 87.1 / 98.5 / 120.0 ℃）
- 清洗流程：删高缺失列 → 缺失填充 → 去重 → 类型转换 → 阈值过滤异常 → 导出
- 清洗结果 196 行，缺失值为 0，温度标准差由 10.93 降至 2.85
- 三类传感器告警率：S-C3 15.07% > S-B2 13.33% > S-A1 7.94%

## 作者

王易然 · 3389875156@qq.com
## 更新记录

- 2026-11：完成第 1–4 周练习，项目结构整理完毕