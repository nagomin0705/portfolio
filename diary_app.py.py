import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import date

FILENAME = "diary_date.json"
current_year = date.today().year
current_month = date.today().month

def load_diary():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_diary(data):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def comment_on_text(text):
    if "疲れ" in text:
        return "今日もお疲れ様です"
    elif "嬉しい" in text or "楽しい" in text:
        return "素敵な1日でしたね!"
    elif "悲しい" in text:
        return "悲しい気持ちも書き残すことで整理できますよ"
    elif text.strip() == "":
        return "記録は見つかりませんでした"
    else:
        return "毎日少しずつ、自分を記録するって素敵ですね"

def get_same_dates(base_day=None):
    if base_day is None:
        base_day = date.today()
    dates = []
    for i in range(0, 3):
        try:
            d = date(base_day.year - i, base_day.month, base_day.day)
            dates.insert(0, str(d))
        except:
            pass
    return dates

def save_today():
    text = input_box.get("1.0", tk.END).strip()
    if text:
        data = load_diary()
        today_str = str(date.today())
        data[today_str] = text
        save_diary(data)
        comment_label.config(text=comment_on_text(text))
        input_box.delete("1.0", tk.END)
        refresh_diary_display()
    else:
        messagebox.showwarning("未入力", "日記が空です。")

def refresh_diary_display(base_day=None):
    data = load_diary()
    for i, d in enumerate(get_same_dates(base_day)):
        past_labels[i].config(text=f"{d}")
        past_boxes[i].config(state="normal")
        past_boxes[i].delete("1.0", tk.END)
        past_boxes[i].insert(tk.END, data.get(d, "記録なし"))
        past_boxes[i].config(state="disabled")

def display_selected_day(d):
    data = load_diary()
    content = data.get(d, "")
    comment = comment_on_text(content)
    selected_label.config(text=f"{d} のコメント")
    selected_box.config(state="normal")
    selected_box.delete("1.0", tk.END)
    selected_box.insert(tk.END, f"💬 {comment}")
    selected_box.config(state="disabled")
    base_date = date.fromisoformat(d)
    refresh_diary_display(base_date)

def go_to_previous_month():
    global current_year, current_month
    current_month -= 1
    if current_month < 1:
        current_month = 12
        current_year -= 1
    show_calendar()

def go_to_next_month():
    global current_year, current_month
    current_month += 1
    if current_month > 12:
        current_month = 1
        current_year += 1
    show_calendar()

def show_calendar():
    for widget in calendar_frame.winfo_children():
        widget.destroy()

    data = load_diary()
    for day in range(1, 32):
        try:
            d = date(current_year, current_month, day)
            d_str = str(d)
            btn = tk.Button(calendar_frame, text=str(day), width=3,
                            bg='#d0e8f2' if d_str in data else '#f0f0f0',
                            font=("UD デジタル 教科書体 NP-R", 9),
                            command=lambda ds=d_str: display_selected_day(ds))
            btn.grid(row=(day - 1)//7 + 2, column=(day - 1)%7, padx=2, pady=2)
        except:
            pass

    month_label.config(text=f"{current_year}年{current_month}月")

# 🎨 UI構築
root = tk.Tk()
root.title("三年日記＋カレンダー")
root.geometry("480x760")
root.configure(bg="#f0f8ff")  # 優しいブルー背景

past_labels = []
past_boxes = []

for i, d in enumerate(get_same_dates()):
    label = tk.Label(root, text=d, bg="#f0f8ff", fg="#333333",
                     font=("UD デジタル 教科書体 NP-R", 10))
    label.pack()
    box = tk.Text(root, height=3, width=55, bg="#fffaf0", fg="#333333",
                  font=("UD ゴシック", 10))
    box.pack()
    box.config(state="disabled")
    past_labels.append(label)
    past_boxes.append(box)

tk.Label(root, text="今日の日記", bg="#f0f8ff", fg="#333333",
         font=("UD デジタル 教科書体 NP-R", 11)).pack()
input_box = tk.Text(root, height=4, width=55, bg="#fffaf0", fg="#333333",
                    font=("UD ゴシック", 10))
input_box.pack()

save_button = tk.Button(root, text="保存 📝", command=save_today,
                        font=("UD ゴシック", 10), bg="#e6f3e6")
save_button.pack(pady=5)

comment_label = tk.Label(root, text="", bg="#f0f8ff", fg="#333333",
                         font=("UD ゴシック", 10))
comment_label.pack()

selected_label = tk.Label(root, text="", bg="#f0f8ff", fg="#333333",
                          font=("UD ゴシック", 10))
selected_label.pack()

selected_box = tk.Text(root, height=2, width=55, bg="#fffaf0", fg="#333333",
                       font=("UD ゴシック", 10))
selected_box.pack()
selected_box.config(state="disabled")

navigation_frame = tk.Frame(root, bg="#f0f8ff")
navigation_frame.pack()

prev_button = tk.Button(navigation_frame, text="◀ 前月", command=go_to_previous_month,
                        font=("UD ゴシック", 10), bg="#e6f3e6")
prev_button.pack(side=tk.LEFT, padx=10)

month_label = tk.Label(navigation_frame, text="", bg="#f0f8ff", fg="#333333",
                       font=("UD ゴシック", 11))
month_label.pack(side=tk.LEFT)

next_button = tk.Button(navigation_frame, text="次月 ▶", command=go_to_next_month,
                        font=("UD ゴシック", 10), bg="#e6f3e6")
next_button.pack(side=tk.LEFT, padx=10)

calendar_frame = tk.Frame(root, bg="#f0f8ff")
calendar_frame.pack(pady=10)

show_calendar()
refresh_diary_display()

root.mainloop()