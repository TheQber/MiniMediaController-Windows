# 🎵 MiniMediaController

A lightweight, persistent, "Always-on-Top" media controller for Windows. This app allows you to monitor and control your music or videos through a tiny, customizable widget that stays above all other windows.



---

## ✨ Features

* **Always on Top:** Never lose your controls behind your browser or IDE.
* **Universal Media Support:** Automatically hooks into any active Windows media session (Spotify, YouTube/Chrome, VLC, Apple Music, etc.).
* **Vertical Compact UI:** A slim, stacked design that fits perfectly in the corner of your screen.
* **Intelligent Truncation:** Long song titles or artist names are automatically shortened to keep the layout clean.
* **Ghost Mode (Opacity):** Use the "O" slider to make the controller semi-transparent so it doesn't block your work.
* **System Volume Control:** Integrated "V" slider to adjust your master Windows volume.
* **Live Progress Bar:** High-visibility green bar to track your playback position.

---

## 🚀 How to Get the App

### Option 1: Download the EXE (Easiest)
1.  Navigate to the **[Releases](https://github.com/YOUR_USERNAME/YOUR_REPO/releases)** tab.
2.  Download the `MiniMediaController.exe` file.
3.  **Note:** Because this is an unsigned community tool, Windows Defender may show a "Windows protected your PC" popup. Click **More Info** -> **Run Anyway**.

### Option 2: Run from Source
If you prefer to run the script directly, ensure you have **Python 3.10+** installed.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPO.git](https://github.com/YOUR_USERNAME/YOUR_REPO.git)
    cd YOUR_REPO
    ```
2.  **Install the required libraries:**
    ```bash
    pip install winsdk pycaw comtypes
    ```
3.  **Launch the app:**
    ```bash
    python media_controller.py
    ```

---

## 🛠️ Compiling it yourself

If you want to modify the code and package your own executable:

1.  Install **PyInstaller**:
    ```bash
    pip install pyinstaller
    ```
2.  Run the build command:
    ```bash
    pyinstaller --noconsole --onefile --name "MiniMediaController" media_controller.py
    ```
3.  Your standalone app will be waiting in the `dist/` folder.

---

## 🖱️ How to Use

* **Move the Window:** Click and drag the **Song Title**, **Artist Name**, or any **Dark Background** area.
* **Adjust Volume (V):** Slide to change your system's master volume.
* **Adjust Opacity (O):** Slide to make the window "ghostly" (transparent).
* **Close (✕):** Terminate the app and all background media-listening processes.

---

## ⚙️ Run on Startup

To have your MiniMediaController ready every time you boot your PC:
1.  Press `Win + R`, type `shell:startup`, and hit Enter.
2.  Right-click your `MiniMediaController.exe` and select **Create Shortcut**.
3.  Paste that shortcut into the Startup folder.

---

## 📝 License
This project is open-source. Feel free to fork, modify, and use it however you like!
