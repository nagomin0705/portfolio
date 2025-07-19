import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import date

FILENAME = "diary_date.json"

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
    else:
        return "毎日少しずつ、自分を記録するって素敵ですね"

def get_same_dates():
    today = date.today()
    dates = [str(today)]
    for i in range(1, 3):
        try:
            prev = date(today.year - i, today.month, today.day)
            dates.insert(0, str(prev))
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

def refresh_diary_display():
    data = load_diary()
    for i, d in enumerate(get_same_dates()):
        past_labels[i].config(text=f"{d}")
        past_boxes[i].config(state="normal")
        past_boxes[i].delete("1.0", tk.END)
        past_boxes[i].insert(tk.END, data.get(d, "記録なし"))
        past_boxes[i].config(state="disabled")

def display_selected_day(d):
    data = load_diary()
    content = data.get(d, "記録なし")
    selected_label.config(text=f"{d}")
    selected_box.config(state="normal")
    selected_box.delete("1.0", tk.END)
    selected_box.insert(tk.END, content)
    selected_box.config(state="disabled")

def show_calendar():
    data = load_diary()
    today = date.today()
    year, month = today.year, today.month
    for day in range(1, 32):
        try:
            d = date(year, month, day)
            d_str = str(d)
            btn = tk.Button(calendar_frame, text=str(day), width=3, bg='lightblue' if d_str in data else 'lightgray',
                            command=lambda ds=d_str: display_selected_day(ds))
            btn.grid(row=(day-1)//7, column=(day-1)%7, padx=2, pady=2)
        except:
            pass

# UI構築
root = tk.Tk()
root.title("三年日記＋カレンダー")
root.geometry("450x700")
root.configure(bg="lightgreen")

# 過去の日付表示
past_labels = []
past_boxes = []

for i, d in enumerate(get_same_dates()):
    label = tk.Label(root, text=d, bg="lightgreen")
    label.pack()
    box = tk.Text(root, height=3, width=50)
    box.pack()
    box.config(state="disabled")
    past_labels.append(label)
    past_boxes.append(box)

# 今日の日記入力
tk.Label(root, text="今日の日記", bg="lightgreen").pack()
input_box = tk.Text(root, height=4, width=50)
input_box.pack()

save_button = tk.Button(root, text="保存", command=save_today)
save_button.pack(pady=5)

comment_label = tk.Label(root, text="", bg="lightgreen")
comment_label.pack()

# カレンダー表示
selected_label = tk.Label(root, text="", bg="lightgreen")
selected_label.pack()
selected_box = tk.Text(root, height=2, width=50)
selected_box.pack()
selected_box.config(state="disabled")

calendar_frame = tk.Frame(root)
calendar_frame.pack(pady=10)
show_calendar()

refresh_diary_display()

root.mainloop()

def save_diary(data):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

#コメント生成
def comment_on_text(text):
    if "疲れ" in text:
        return "今日もお疲れ様です"
    elif "嬉しい" in text or "楽しい" in text:
        return "素敵な1日でしたね!"
    elif "悲しい" in text:
        return "悲しい気持ちも書き残すことで整理できますよ"
    else:
        return "毎日少しずつ、自分を記録するって素敵ですね"

#今日と過去2年の同じ日
def get_same_dates():
    today = date.today()
    dates = [str(today)]
    for i in range(1, 3):
        try:
            prev = date(today.year - i, today.month, today.day)
            dates.insert(0, str(prev))
        except:
            pass
    return dates

#日記保存ボタン
def save_today(sender):
    text = input_box.text.strip()
    if text:
        data = load_diary()
        today_str = str(date.today())
        data[today_str] = text
        save_diary(data)
        comment_label.text = comment_on_text(text)
        input_box.text = ""
        refresh_diary_display()

#過去の日記の表示
def refresh_diary_display():
    data = load_diary()
    for i, d in enumerate(get_same_dates()):
        label = past_labels[i]
        box = past_boxes[i]
        label.text = f"{d}"
        box.text = data.get(d, "記録なし")

#カレンダー風の日付ボタン表示
def show_calendar():
    data = load_diary()
    current = date.today()
    year, month = current.year, current.month
    for day in range(1, 32):
        try:
            d = date(year, month, day)
            d_str = str(d)
            btn = ui.Button(title=str(day), frame=(90 +((day-1)%7)*30, 370 +((day-1)//7)*30, 40,30))
            if d_str in data:
                btn.background_color = 'lightblue'
            else:
                btn.background_color = 'lightgray'
            btn.action = lambda sender, ds=d_str: display_selected_day(ds)
            v.add_subview(btn)
        except:
            pass

#選択された日付の日記を表示
def display_selected_day(date_str):
    data = load_diary()
    content = data.get(date_str, "記録なし")
    selected_label.text = f"{date_str}"
    selected_box.text = content

#UI構築
v = ui.View(frame=(0, 0, 400, 600), name="三年日記+カレンダー")
v.background_color = 'lightgreen'
past_labels = []
past_boxes = []

#過去の同じ日
y = 10
for _ in get_same_dates():
    label = ui.Label(frame=(10, y, 380, 20))
    box = ui.TextView(frame=(10, y+20, 380, 60))
    box.editable = False
    v.add_subview(label)
    v.add_subview(box)
    past_labels.append(label)
    past_boxes.append(box)
    y +=90

#今日の日記入力
input_label = ui.Label(frame=(10, y,380, 20))
input_label.text = "今日の日記"
input_box = ui.TextView(frame=(10, y+20, 380, 60))
save_button = ui.Button(title="保存", frame=(350, 360, 80, 30))
save_button.action = save_today
comment_label = ui.Label(frame=(20, 540, 290, 30))

v.add_subview(input_label)
v.add_subview(input_box)
v.add_subview(save_button)

#カレンダー風日付ボタン＋選択表示
selected_label = ui.Label(frame=(10, 520, 380, 20))
selected_box = ui.TextView(frame=(10, 540, 380, 40))
selected_box.editable = False
v.add_subview(selected_label)
v.add_subview(selected_box)
v.add_subview(comment_label)

refresh_diary_display()
show_calendar()
v.present('sheet')
