# -*- coding: utf-8 -*-
"""第四周综合练习参考实现：一次生成 6 张单图 + 1 张 2x3 组合图。
运行方式（在 D:\\phase1-practice 下）：python week4_plot.py
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")            # 脚本模式不弹窗，直接存文件
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

BASE = Path(r"D:\phase1-practice")
DATA, FIG = BASE / "data", BASE / "figures"
FIG.mkdir(parents=True, exist_ok=True)

sns.set_style("whitegrid")          # 先设风格
plt.rcParams["font.sans-serif"] = ["SimHei"]   # 再设字体（顺序不能反）
plt.rcParams["axes.unicode_minus"] = False

df = pd.read_csv(DATA / "cleaned_data.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp").reset_index(drop=True)

daily = df.set_index("timestamp")["temperature"].resample("D").mean()
avg_temp = df.groupby("sensor_type")["temperature"].mean().reindex(["S-A1", "S-B2", "S-C3"])
corr = df[["temperature", "humidity", "vibration"]].corr()
colors = {"S-A1": "tab:blue", "S-B2": "tab:orange", "S-C3": "tab:green"}

# ---------- 单图 1：折线 ----------
fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(df["timestamp"], df["temperature"], color="tomato", linewidth=1.2, label="逐时温度")
ax.plot(daily.index, daily.values, color="black", linewidth=2, marker="o", label="日均温度")
ax.set_title("温度随时间变化趋势（2026-10-01 至 10-09）")
ax.set_xlabel("时间"); ax.set_ylabel("温度 (℃)")
ax.legend(); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(FIG / "fig1_line.png", dpi=300, bbox_inches="tight"); plt.close(fig)

# ---------- 单图 2：散点 ----------
fig, ax = plt.subplots(figsize=(6.5, 5))
for st, c in colors.items():
    sub = df[df["sensor_type"] == st]
    ax.scatter(sub["temperature"], sub["humidity"], s=28, alpha=0.65, color=c,
               label=st, edgecolors="white", linewidths=0.5)
ax.set_title("温度与湿度的关系（按传感器类型着色）")
ax.set_xlabel("温度 (℃)"); ax.set_ylabel("湿度 (%)")
ax.legend(title="传感器")
fig.tight_layout(); fig.savefig(FIG / "fig2_scatter.png", dpi=300, bbox_inches="tight"); plt.close(fig)

# ---------- 单图 3：柱状 ----------
fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(avg_temp.index, avg_temp.values, color=["tab:blue", "tab:orange", "tab:green"], width=0.5)
for i, v in enumerate(avg_temp.values):
    ax.text(i, v + 0.3, f"{v:.2f}", ha="center", fontsize=11)
ax.set_title("各类传感器平均温度对比")
ax.set_xlabel("传感器类型"); ax.set_ylabel("平均温度 (℃)")
ax.set_ylim(0, 30)
fig.tight_layout(); fig.savefig(FIG / "fig3_bar.png", dpi=300, bbox_inches="tight"); plt.close(fig)

# ---------- 单图 4：直方 + KDE ----------
fig, ax = plt.subplots(figsize=(6.5, 4.5))
sns.histplot(data=df, x="temperature", bins=20, kde=True, color="steelblue", edgecolor="black", ax=ax)
ax.axvline(df["temperature"].mean(), color="tomato", linestyle="--", linewidth=1.5,
           label=f"均值 {df['temperature'].mean():.2f}")
ax.set_title("温度分布直方图（带核密度曲线）")
ax.set_xlabel("温度 (℃)"); ax.set_ylabel("频数")
ax.legend()
fig.tight_layout(); fig.savefig(FIG / "fig4_hist.png", dpi=300, bbox_inches="tight"); plt.close(fig)

# ---------- 单图 5：箱线 ----------
fig, ax = plt.subplots(figsize=(6.5, 4.5))
sns.boxplot(data=df, x="sensor_type", y="temperature", order=["S-A1", "S-B2", "S-C3"],
            hue="sensor_type", palette="Set2", legend=False, ax=ax)
sns.stripplot(data=df, x="sensor_type", y="temperature", order=["S-A1", "S-B2", "S-C3"],
              color="black", size=2, alpha=0.35, ax=ax)
ax.set_title("各类传感器温度分布箱线图")
ax.set_xlabel("传感器类型"); ax.set_ylabel("温度 (℃)")
fig.tight_layout(); fig.savefig(FIG / "fig5_box.png", dpi=300, bbox_inches="tight"); plt.close(fig)

# ---------- 单图 6：热力图 ----------
fig, ax = plt.subplots(figsize=(5, 4.2))
sns.heatmap(corr, annot=True, fmt=".3f", cmap="coolwarm", vmin=-1, vmax=1,
            square=True, linewidths=0.5, ax=ax)
ax.set_title("变量相关系数热力图")
fig.tight_layout(); fig.savefig(FIG / "fig6_heatmap.png", dpi=300, bbox_inches="tight"); plt.close(fig)

# ---------- 组合大图 2x3 ----------
fig, axes = plt.subplots(2, 3, figsize=(16, 9))

axes[0, 0].plot(df["timestamp"], df["temperature"], color="tomato", linewidth=1.0, label="逐时温度")
axes[0, 0].plot(daily.index, daily.values, color="black", linewidth=2, marker="o", label="日均温度")
axes[0, 0].legend(fontsize=9)
axes[0, 0].set_title("温度随时间变化")
axes[0, 0].set_xlabel("时间"); axes[0, 0].set_ylabel("温度 (℃)")
axes[0, 0].tick_params(axis="x", rotation=30)

for st, c in colors.items():
    sub = df[df["sensor_type"] == st]
    axes[0, 1].scatter(sub["temperature"], sub["humidity"], s=18, alpha=0.6, color=c, label=st)
axes[0, 1].set_title("温度与湿度关系")
axes[0, 1].set_xlabel("温度 (℃)"); axes[0, 1].set_ylabel("湿度 (%)")
axes[0, 1].legend(fontsize=9)

axes[0, 2].bar(avg_temp.index, avg_temp.values, color=["tab:blue", "tab:orange", "tab:green"], width=0.55)
for i, v in enumerate(avg_temp.values):
    axes[0, 2].text(i, v + 0.2, f"{v:.2f}", ha="center", fontsize=9)
axes[0, 2].set_title("平均温度对比")
axes[0, 2].set_xlabel("传感器类型"); axes[0, 2].set_ylabel("平均温度 (℃)")
axes[0, 2].set_ylim(0, 29)

sns.histplot(data=df, x="temperature", bins=20, kde=True, color="steelblue", ax=axes[1, 0])
axes[1, 0].set_title("温度分布")
axes[1, 0].set_xlabel("温度 (℃)"); axes[1, 0].set_ylabel("频数")

sns.boxplot(data=df, x="sensor_type", y="temperature", order=["S-A1", "S-B2", "S-C3"],
            hue="sensor_type", palette="Set2", legend=False, ax=axes[1, 1])
axes[1, 1].set_title("各类温度分布")
axes[1, 1].set_xlabel("传感器类型"); axes[1, 1].set_ylabel("温度 (℃)")

sns.heatmap(corr, annot=True, fmt=".3f", cmap="coolwarm", vmin=-1, vmax=1,
            square=True, cbar=False, ax=axes[1, 2])
axes[1, 2].set_title("变量相关性")

fig.suptitle("传感器数据可视化报告（196 条记录 / 2026-10-01 至 10-09）", fontsize=15)
fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig(FIG / "report_figure.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print("已保存:", FIG / "report_figure.png")
