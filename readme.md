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

## 🖼️ Screenshot

> Sample GUI view:

![Screenshot](./assets/screenshot.2025-08-02%20(8).png)

---

## 🛠 Installation

```bash
git clone https://github.com/yourusername/PatentBatchMonitor.git
cd PatentBatchMonitor
pip install -r requirements.txt
```

> Required packages:
> - `tkinter`
> - `matplotlib`
> - `pillow`
> - `pandas`

---

## 🚀 Usage

```bash
python Monitor_Folder_Gui.py [-i INPUT_FOLDER] [-t WINDOW_TITLE]
```

### Optional arguments:

| Flag | Description |
|------|-------------|
| `-i` | Folder to monitor (e.g. `-i "D:\PharmApp"`) |
| `-t` | Custom window title (e.g. `-t "📦 Patent Monitor"`) |

If `-t` is not provided, the program will try to read the first line of `title.txt`.  
If `-i` is not provided, it defaults to: `D:\PharmApp`.

---

## 📁 Folder Structure

```bash
.
├── Monitor_Folder_Gui.py
├── title.txt                          # Optional: custom window title
├── ./log/
│   └── monitor_data.csv               # Auto-created log file
├── ./assets/
│   ├── nct_logo_3000x3000_20250606.png  # Auto-downloaded if missing
│   └── screenshot.2025-08-02 (8).png     # Manual GUI screenshot
```

---

## 📦 Example

```bash
python Monitor_Folder_Gui.py -i "D:\Pharmacopoeia" -t "📦 SmPC PDF Tracker"
```

---

## 📢 Credits

- Developed by [Nghiên Cứu Thuốc](https://www.nghiencuuthuoc.com)
- Part of the [PharmApp v2025.03](https://www.pharmapp.vn) ecosystem

---

## 📜 License

MIT License – free for academic & research use.
