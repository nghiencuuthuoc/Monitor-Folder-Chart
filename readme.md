# 📈 Patent Batch Monitor GUI

A lightweight Tkinter-based monitoring tool for tracking PDF file growth and folder size over time — designed for pharmaceutical and regulatory document management such as the Orange Book or patent batch collections.

---

## 🧩 Features

- 📂 Monitor a folder for new `.pdf` files
- 📊 Real-time charts: file count & folder size over time
- 📋 Display the 10 most recent files with size info
- 🖼️ Logo and visual branding (PharmApp themed)
- 📝 Log data saved in `./log/monitor_data.csv`
- 📄 Custom window title from `title.txt` or CLI `-t`
- ✅ Cross-platform (Windows/Linux)

---

## 🛠 Installation

```bash
git clone https://github.com/nghiencuuthuoc/PatentBatchMonitor.git
cd PatentBatchMonitor
pip install -r requirements.txt
