# modules/PatentBatchMonitor.py

import os
import time
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

LOG_PATH = "../database/orange_book/patent_ob_batchs_log.csv"
WATCH_FOLDER = "../database/orange_book/patent_ob_batchs"

def get_folder_stats(folder):
    total_size = 0
    file_count = 0
    for root, _, files in os.walk(folder):
        for f in files:
            if f.lower().endswith(".pdf"):
                fp = os.path.join(root, f)
                try:
                    total_size += os.path.getsize(fp)
                    file_count += 1
                except:
                    continue
    return total_size / (1024 * 1024), file_count  # MB

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

def plot_graph(df, y_column, ylabel):
    fig, ax = plt.subplots()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    ax.plot(df["timestamp"], df[y_column], marker='o')

    ax.set_xlabel("Time")
    ax.set_ylabel(ylabel)
    ax.set_title(f"{ylabel} Over Time")
    ax.grid(True)

    # ✅ Sửa lỗi chữ dính: xoay nhãn trục x và giãn khoảng
    fig.autofmt_xdate(rotation=30)  # xoay 30 độ, tự động căn lề

    return fig

def run():
    st.set_page_config(page_title="📈 Patent Batch Monitor", layout="wide")
    st.title("📈 Patent Batch Folder Monitor")
    st.markdown("⏱️ This module scans the folder every 10 minutes and logs the number and size of PDF files.")

    if st.button("📥 Trigger Scan Now"):
        append_log()
        st.success("✅ Manual scan completed and log updated.")

    df = load_log()
    if df.empty:
        st.warning("⚠️ No log data available yet.")
    else:
        st.markdown("### 📊 Real-time Monitoring")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📁 Number of Files")
            fig1 = plot_graph(df, "file_count", "PDF File Count")
            st.pyplot(fig1)

        with col2:
            st.subheader("💾 Folder Size (MB)")
            fig2 = plot_graph(df, "size_mb", "Folder Size (MB)")
            st.pyplot(fig2)

        with st.expander("🧾 View Raw Log Data"):
            st.dataframe(df.tail(20))

    st.markdown("---")
    st.info("🛠 To automate logging every 10 minutes, run `append_log()` via scheduled task (cron or Task Scheduler).")


    # --- Footer ---
    st.markdown("""<br><hr><div style='text-align:center; font-size: 12px'>
    | Copyright 2025 | 🥣 Nghiên Cứu Thuốc | 🧠 PharmApp |<br>
    | Discover | Design | Optimize | Create | Deliver | <br>
    | <a href='https://www.nghiencuuthuoc.com'>www.nghiencuuthuoc.com</a> | <a href='https://www.pharmapp.vn'>www.pharmapp.vn</a> |
    </div>""", unsafe_allow_html=True)

if __name__ == "__main__":
    run()
