import streamlit as st
import csv
import matplotlib.pyplot as plt
import math
import japanize_matplotlib

st.title("⏳ 私の24時間スケジュール")

plt.rcParams['font.family'] = 'Meiryo'  

#CSVから「すべてのデータ」と「存在する日付」を読み込む
all_data = []
unique_dates = []

with open("schedule.csv", mode="r", encoding="utf-8-sig") as file:
    reader = csv.reader(file)
    next(reader) 
    for line in reader:
        if not line:
            continue
        all_data.append(line)
        # まだリストにない日付なら追加する
        if line[0] not in unique_dates:
            unique_dates.append(line[0])


# プルダウンメニューを作成
target_date = st.selectbox("📅 見たい日付を選んでください", unique_dates)

# プルダウンで選ばれた日付のタスクだけを抽出する
all_tasks = []
for line in all_data:
    if line[0] == target_date:
        all_tasks.append(line)

# デバッグ（確認）用：Web画面に直接リストの中身を表示させる！
#st.write(f"【確認用】{target_date} のタスクデータ:", all_tasks)

# グラフの描画
fig, ax = plt.subplots(subplot_kw={'polar': True})
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)
ax.set_xticks([i / 24 * 2 * math.pi for i in range(0, 24, 3)])
ax.set_xticklabels([f"{i}:00" for i in range(0, 24, 3)])
ax.set_yticks([])  

for task in all_tasks:
    task_name = task[1]
    start_hour = float(task[2])     
    duration_hour = float(task[3])  
    
    start_angle = (start_hour / 24) * 2 * math.pi
    width_angle = (duration_hour / 24) * 2 * math.pi
    
    ax.bar(x=start_angle, height=1, width=width_angle, bottom=0, align='edge', edgecolor="white")
    mid_angle = start_angle + (width_angle / 2)
    ax.text(mid_angle, 0.6, task_name, ha='center', va='center', fontsize=12)

# Web画面にグラフを表示
st.pyplot(fig)
