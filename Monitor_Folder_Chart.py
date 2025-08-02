import os
import sys
import argparse
import urllib.request
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
from typing import List, Tuple

# Global variables
WATCH_FOLDER = None
LOG_PATH = None
REFRESH_INTERVAL = 180  # seconds

def get_folder_stats(folder):
    total_size = 0
    file_count = 0
    for root, _, files in os.walk(folder):
        for f in files:
            if f.lower().endswith(".pdf"):
                try:
                    total_size += os.path.getsize(os.path.join(root, f))
                    file_count += 1
                except:
                    continue
    return round(total_size / (1024 * 1024), 2), file_count  # in MB

def append_log():
    size_mb, file_count = get_folder_stats(WATCH_FOLDER)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_row = pd.DataFrame([[now, size_mb, file_count]], columns=["timestamp", "size_mb", "file_count"])
    if os.path.exists(LOG_PATH):
        df_old = pd.read_csv(LOG_PATH)
        df = pd.concat([df_old, new_row], ignore_index=True)
    else:
        df = new_row
    df.to_csv(LOG_PATH, index=False)

def load_log():
    if os.path.exists(LOG_PATH):
        return pd.read_csv(LOG_PATH)
    return pd.DataFrame(columns=["timestamp", "size_mb", "file_count"])

def plot_data(frame):
    df = load_log()
    if df.empty:
        return
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    fig1, ax1 = plt.subplots(figsize=(5, 3))
    ax1.plot(df["timestamp"], df["file_count"], marker='o')
    ax1.set_title("Number of PDF Files")
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Files")
    ax1.grid(True)
    fig1.autofmt_xdate(rotation=30)

    fig2, ax2 = plt.subplots(figsize=(5, 3))
    ax2.plot(df["timestamp"], df["size_mb"], marker='o', color="green")
    ax2.set_title("Folder Size (MB)")
    ax2.set_xlabel("Time")
    ax2.set_ylabel("MB")
    ax2.grid(True)
    fig2.autofmt_xdate(rotation=30)

    for widget in frame.winfo_children():
        widget.destroy()

    canvas1 = FigureCanvasTkAgg(fig1, master=frame)
    canvas1.draw()
    canvas1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    canvas2 = FigureCanvasTkAgg(fig2, master=frame)
    canvas2.draw()
    canvas2.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


def get_recent_files(folder: str, limit: int = 10) -> List[Tuple[float, str, float]]:
    """
    Scan the folder and return the most recent files by modification time.

    Args:
        folder (str): Folder path to scan.
        limit (int): Number of most recent files to return.

    Returns:
        List[Tuple[mtime, filename, size_mb]]
    """
    files = []
    for root, _, filenames in os.walk(folder):
        for fname in filenames:
            path = os.path.join(root, fname)
            try:
                size_mb = os.path.getsize(path) / (1024 * 1024)
                mtime = os.path.getmtime(path)
                files.append((mtime, os.path.relpath(path, folder), round(size_mb, 2)))
            except Exception as e:
                continue  # skip unreadable files

    files.sort(reverse=True)  # Sort by mtime descending
    return files[:limit]


def update_recent_files(tree_widget):
    tree_widget.delete(*tree_widget.get_children())
    recent = get_recent_files(WATCH_FOLDER, limit=10)
    for i, (_, fname, size) in enumerate(recent, 1):
        tree_widget.insert("", "end", values=(i, fname, size))

def update_gui(frame, label):
    append_log()
    size_mb, file_count = get_folder_stats(WATCH_FOLDER)
    label.config(text=f"✅ {file_count} files | {size_mb:.2f} MB")
    plot_data(frame)
    update_recent_files(tree)
    frame.after(REFRESH_INTERVAL * 1000, lambda: update_gui(frame, label))

def choose_folder(label, frame):
    global WATCH_FOLDER
    new_folder = filedialog.askdirectory(initialdir=WATCH_FOLDER)
    if new_folder:
        WATCH_FOLDER = new_folder
        label.config(text=f"📁 Monitoring: {WATCH_FOLDER}")
        update_gui(frame, label)

def download_logo_if_needed():
    logo_path = os.path.abspath("./assets/nct_logo_3000x3000_20250606.png")
    if not os.path.exists(logo_path):
        try:
            os.makedirs(os.path.dirname(logo_path), exist_ok=True)
            url = "https://raw.githubusercontent.com/nghiencuuthuoc/PharmApp/refs/heads/master/images/nct_logo_3000x3000_20250606.png"
            urllib.request.urlretrieve(url, logo_path)
        except:
            return None
    return logo_path

def start_gui(window_title):
    global tree

    root = tk.Tk()
    root.title(window_title)
    root.geometry("1100x720")
    root.configure(bg="#fdf5e6")

    style = ttk.Style()
    style.theme_use("default")
    style.configure("TFrame", background="#fdf5e6")
    style.configure("TLabel", background="#fdf5e6", foreground="#2a2a2a", font=("Arial", 11))
    style.configure("TButton", background="#f4a261", foreground="black", font=("Arial", 10, "bold"))
    style.map("TButton", background=[("active", "#e76f51")])
    style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#b5838d", foreground="white")
    style.configure("Treeview", font=("Arial", 10), rowheight=25)
    style.map('Treeview', background=[('selected', '#e9c46a')])

    logo_path = download_logo_if_needed()
    if logo_path:
        try:
            logo_img = Image.open(logo_path).resize((80, 80), Image.ANTIALIAS)
            logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(root, image=logo_photo, bg="#fdf5e6")
            logo_label.image = logo_photo
            logo_label.pack(pady=5)
        except:
            pass

    top_frame = ttk.Frame(root, style="TFrame")
    top_frame.pack(fill=tk.X, pady=5)

    status_label = ttk.Label(top_frame, text=f"📁 Monitoring: {WATCH_FOLDER}", font=("Arial", 12))
    status_label.pack(side=tk.LEFT, padx=10)

    refresh_button = ttk.Button(top_frame, text="🔄 Scan Now", command=lambda: update_gui(main_frame, status_label))
    refresh_button.pack(side=tk.RIGHT, padx=10)

    choose_button = ttk.Button(top_frame, text="📂 Choose Folder", command=lambda: choose_folder(status_label, main_frame))
    choose_button.pack(side=tk.RIGHT, padx=10)

    main_frame = ttk.Frame(root, style="TFrame")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    recent_frame = ttk.Frame(root, style="TFrame")
    recent_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=5)

    columns = ("#", "File Name", "Size (MB)")
    tree = ttk.Treeview(recent_frame, columns=columns, show="headings", height=10)
    for col in columns:
        anchor = tk.W if col == "File Name" else tk.CENTER
        width = 500 if col == "File Name" else 80
        tree.heading(col, text=col)
        tree.column(col, width=width, anchor=anchor)
    tree.pack(fill=tk.BOTH, expand=True)

    update_gui(main_frame, status_label)

    bottom_frame = ttk.Frame(root, style="TFrame")
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
    footer_text = (
        "| Copyright 2025 | 🥣 Nghiên Cứu Thuốc | 🧠 PharmApp |\n"
        "| Discover | Design | Optimize | Create | Deliver |\n"
        "| www.nghiencuuthuoc.com | Zalo: +84888999311 | www.pharmapp.vn |"
    )
    footer_label = tk.Label(bottom_frame, text=footer_text, font=("Arial", 9), justify="center", bg="#fdf5e6")
    footer_label.pack()

    root.mainloop()

def main():
    global WATCH_FOLDER, LOG_PATH

    parser = argparse.ArgumentParser(description="Monitor a folder for PDF files")
    parser.add_argument("-i", "--input", type=str, help="Input folder to monitor")
    parser.add_argument("-t", "--title", type=str, help="Window title")
    args = parser.parse_args()

    # Set monitored folder
    if args.input:
        input_path = os.path.abspath(args.input)
        if not os.path.isdir(input_path):
            print(f"❌ Input folder does not exist: {input_path}")
            sys.exit(1)
        WATCH_FOLDER = input_path
    else:
        WATCH_FOLDER = os.path.abspath("D:/PharmApp")

    # Set log path to ./log/monitor_data.csv
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(script_dir, "log")
    os.makedirs(log_dir, exist_ok=True)
    LOG_PATH = os.path.join(log_dir, "monitor_data.csv")

    # Determine window title
    window_title = args.title
    if not window_title:
        try:
            with open("title.txt", encoding="utf-8") as f:
                window_title = f.readline().strip()
        except:
            window_title = "📈 Patent Batch Monitor GUI"

    start_gui(window_title)

if __name__ == "__main__":
    main()
