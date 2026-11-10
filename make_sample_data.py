# -*- coding: utf-8 -*-
"""
make_sample_data.py
生成第一阶段配套练习数据：模拟传感器数据 sensor_data.csv

数据特点（供第 3 周清洗练习）：
- 约 200 行，包含时间戳、传感器类别、温度、湿度、电压、设备状态等列
- 故意混入：缺失值、完全重复行、异常值（离群点）
- 使用 numpy 生成 + pandas 导出，本身也是一份 NumPy/Pandas 代码示例

运行方式（在 VS Code 终端中）：
    python make_sample_data.py
"""

import numpy as np
import pandas as pd
import os

# 固定随机种子，保证每次生成的数据一致（可复现）
np.random.seed(42)

N = 200  # 行数

# ---------- 1. 生成时间戳列：从 2026-10-01 08:00 开始，每小时一条 ----------
start = pd.Timestamp("2026-10-01 08:00:00")
timestamps = [start + pd.Timedelta(hours=i) for i in range(N)]

# ---------- 2. 传感器类别：三种传感器随机分配 ----------
sensor_types = np.random.choice(["S-A1", "S-B2", "S-C3"], size=N)

# ---------- 3. 数值列：正态分布生成 ----------
temperature = np.round(np.random.normal(loc=25.0, scale=3.0, size=N), 2)   # 温度 ℃
humidity = np.round(np.random.normal(loc=55.0, scale=10.0, size=N), 2)     # 湿度 %
vibration = np.round(np.random.normal(loc=0.5, scale=0.2, size=N), 3)      # 振动 g

# ---------- 4. 状态列：正常/告警，90% 为正常 ----------
status = np.random.choice(["正常", "告警"], size=N, p=[0.9, 0.1])

# ---------- 5. 组装为 DataFrame ----------
df = pd.DataFrame({
    "timestamp": timestamps,
    "sensor_type": sensor_types,
    "temperature": temperature,
    "humidity": humidity,
    "vibration": vibration,
    "status": status,
})

# ---------- 6. 故意注入"脏数据"（练习用） ----------
# 6.1 随机挖掉约 8% 的数值（制造缺失值）
for col in ["temperature", "humidity", "vibration"]:
    mask = np.random.rand(N) < 0.08
    df.loc[mask, col] = np.nan

# 6.2 制造 5 条完全重复的行
dup_idx = np.random.choice(df.index, size=5, replace=False)
df = pd.concat([df, df.loc[dup_idx]], ignore_index=True)

# 6.3 制造异常值（离群点）
outlier_idx = np.random.choice(df.index, size=4, replace=False)
df.loc[outlier_idx, "temperature"] = [98.5, -20.3, 120.0, 87.1]  # 远超正常范围

# ---------- 7. 打乱行顺序并保存 ----------
df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)

os.makedirs("data", exist_ok=True)
df.to_csv("data/sensor_data.csv", index=False, encoding="utf-8-sig")

print("已生成 data/sensor_data.csv")
print(f"总行数: {len(df)}")
print(df.head(8))
