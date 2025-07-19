import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import date

# ==== データ管理 ====
habits = []
habit_checks = {}
achievement_days = set()

FILENAME_HABITS = "habits.json"
FILENAME_CHECKS = "habit_checks.json"
FILENAME_ACHIEVEMENTS = "achievement.json"

def save_habits():
    with open(FILENAME_HABITS, "w", encoding="utf-8") as f:
        json.dump({"habits": habits}, f, indent=2, ensure_ascii=False)

def load_habits():
    global habits
    try:
        with open(FILENAME_HABITS, "r", encoding="utf-8") as f:
            habits = json.load(f).get("habits", [])
    except FileNotFoundError:
        habits = []

def save_checks():
    with open(FILENAME_CHECKS, "w", encoding="utf-8") as f:
        json.dump(habit_checks, f, indent=2, ensure_ascii=False)

def load_checks():
    global habit_checks
    try:
        with open(FILENAME_CHECKS, "r", encoding="utf-8") as f:
            habit_checks = json.load(f)
    except FileNotFoundError:
        habit_checks = {}

def save_achievements():
    with open(FILENAME_ACHIEVEMENTS, "w", encoding="utf-8") as f:
        json.dump({"days": list(achievement_days)}, f, indent=2, ensure_ascii=False)

def load_achievements():
    global achievement_days
    try:
        with open(FILENAME_ACHIEVEMENTS, "r", encoding="utf-8") as f:
            data = json.load(f)
            achievement_days = set(data.get("days", []))
    except FileNotFoundError:
        achievement_days = set()

def all_checked_for_today():
    today = date.today().isoformat()
    today_checks = habit_checks.get(today, {})
    return len(today_checks) == len(habits) and all(today_checks.get(h, False) for h in habits)

# ==== UI構築 ====
ud_font = ("UD デジタル 教科書体 NP-R", 11)
bg_main = "#f0f8ff"       # 優しいブルー
bg_button = "#e6f3e6"     # ペールグリーン
fg_text = "#333333"       # 落ち着いた濃グレー

root = tk.Tk()
root.title("習慣チェッカー")
root.geometry("430x650")
root.configure(bg=bg_main)

habit_input = tk.Entry(root, width=30, font=ud_font, bg="#fffaf0", fg=fg_text)
habit_input.place(x=20, y=20)

message_label = tk.Label(root, text="", font=ud_font, bg=bg_main, fg="darkblue")
message_label.place(x=20, y=600)

def update_message(text, color="darkblue"):
    message_label.config(text=text, fg=color)

def add_habit():
    new_habit = habit_input.get().strip()
    if new_habit and new_habit not in habits:
        habits.append(new_habit)
        save_habits()
        habit_input.delete(0, tk.END)
        draw_habit_widgets()
        update_message(f"習慣「{new_habit}」を追加しました！", "forestgreen")

add_button = tk.Button(root, text="追加", command=add_habit, font=ud_font,
                       bg=bg_button, fg=fg_text)
add_button.place(x=280, y=18)

def show_achievement():
    total = len(achievement_days)
    update_message(f"これまでに {total} 日達成しました！✨", "purple")

achievement_button = tk.Button(root, text="実績", command=show_achievement, font=ud_font,
                               bg=bg_button, fg=fg_text)
achievement_button.place(x=350, y=18)

def toggle_check(habit, var):
    today = date.today().isoformat()
    if today not in habit_checks:
        habit_checks[today] = {}
    habit_checks[today][habit] = bool(var.get())
    save_checks()

    if all_checked_for_today() and habits:
        if today not in achievement_days:
            achievement_days.add(today)
            save_achievements()
        total = len(achievement_days)
        update_message(f"🎉 今日も全部達成！累計{total}日 🎉", "darkorange")
    else:
        update_message("")

def delete_habit(habit):
    if habit in habits:
        habits.remove(habit)
        save_habits()
        for day in list(habit_checks.keys()):
            if habit in habit_checks[day]:
                del habit_checks[day][habit]
        save_checks()
        draw_habit_widgets()
        update_message(f"習慣「{habit}」を削除しました", "red")

habit_widgets = []

def draw_habit_widgets():
    for w in habit_widgets:
        w.destroy()
    habit_widgets.clear()

    today = date.today().isoformat()
    for i, habit in enumerate(habits):
        y = 70 + i * 45

        lbl = tk.Label(root, text=habit, bg=bg_main, font=ud_font, fg=fg_text)
        lbl.place(x=20, y=y)
        habit_widgets.append(lbl)

        var = tk.IntVar()
        var.set(1 if habit_checks.get(today, {}).get(habit, False) else 0)
        chk = tk.Checkbutton(root, variable=var, bg=bg_main,
                             command=lambda h=habit, v=var: toggle_check(h, v))
        chk.place(x=200, y=y)
        habit_widgets.append(chk)

        btn = tk.Button(root, text="削除", command=lambda h=habit: delete_habit(h),
                        font=ud_font, bg="#ffe4e1", fg="brown")
        btn.place(x=260, y=y-2)
        habit_widgets.append(btn)

# ==== 初期化 ====
load_habits()
load_checks()
load_achievements()
draw_habit_widgets()

root.mainloop()