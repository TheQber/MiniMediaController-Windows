import tkinter as tk
from tkinter import ttk
import asyncio
import os
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as SessionManager
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER

class VerticalMediaController:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)
        self.root.geometry("240x180") 
        self.root.configure(bg='#121212')
        
        self.x = self.y = None

        # Audio Setup
        try:
            device_enumerator = AudioUtilities.GetDeviceEnumerator()
            devices = device_enumerator.GetDefaultAudioEndpoint(0, 0) 
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            self.volume_ctrl = cast(interface, POINTER(IAudioEndpointVolume))
        except: self.volume_ctrl = None

        # --- UI LAYOUT ---

        # 1. TOP ROW: Fixed Layout
        self.top_row = tk.Frame(root, bg='#121212')
        self.top_row.pack(fill="x", padx=10, pady=(10, 2))

        # We set a 'width' here (in characters) to prevent it from expanding
        self.title_label = tk.Label(self.top_row, text="Loading...", fg="white", bg="#121212", 
                                    font=("Segoe UI", 9, "bold"), anchor="w", width=15)
        self.title_label.pack(side=tk.LEFT, fill="x", expand=True)

        self.ctrl_frame = tk.Frame(self.top_row, bg='#121212')
        self.ctrl_frame.pack(side=tk.RIGHT) # This stays pinned to the right
        
        btn_style = {"bg": "#121212", "fg": "white", "borderwidth": 0, "activebackground": "#333", "font": ("Arial", 10)}
        tk.Button(self.ctrl_frame, text="⏮", command=lambda: self.run_cmd("prev"), **btn_style).pack(side=tk.LEFT, padx=1)
        tk.Button(self.ctrl_frame, text="⏯", command=lambda: self.run_cmd("playpause"), **btn_style).pack(side=tk.LEFT, padx=1)
        tk.Button(self.ctrl_frame, text="⏭", command=lambda: self.run_cmd("next"), **btn_style).pack(side=tk.LEFT, padx=1)
        tk.Button(self.ctrl_frame, text="✕", command=self.shutdown, bg="#121212", fg="#ff4444", borderwidth=0).pack(side=tk.LEFT, padx=(5, 0))

        # 2. SECOND ROW: Singer Name (Also truncated)
        self.artist_label = tk.Label(root, text="", fg="#aaaaaa", bg="#121212", font=("Segoe UI", 8), anchor="w")
        self.artist_label.pack(fill="x", padx=10, pady=(0, 10))

        # 3. THIRD ROW: Progress Bar
        self.progress = ttk.Progressbar(root, orient="horizontal", mode="determinate")
        self.progress.pack(fill="x", padx=10, pady=5)

        # 4. FOURTH ROW: Volume
        vol_frame = tk.Frame(root, bg='#121212')
        vol_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(vol_frame, text="V", fg="#666", bg="#121212", font=("Arial", 6, "bold")).pack(side=tk.LEFT)
        self.vol_s = ttk.Scale(vol_frame, from_=0, to=1, orient="horizontal", command=self.set_volume)
        if self.volume_ctrl: self.vol_s.set(self.volume_ctrl.GetMasterVolumeLevelScalar())
        self.vol_s.pack(side=tk.RIGHT, fill="x", expand=True, padx=(5, 0))

        # 5. FIFTH ROW: Opacity
        opac_frame = tk.Frame(root, bg='#121212')
        opac_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(opac_frame, text="O", fg="#666", bg="#121212", font=("Arial", 6, "bold")).pack(side=tk.LEFT)
        self.opac_s = ttk.Scale(opac_frame, from_=0.1, to=1.0, orient="horizontal", command=self.set_opacity)
        self.opac_s.set(1.0)
        self.opac_s.pack(side=tk.RIGHT, fill="x", expand=True, padx=(5, 0))

        # Bindings
        draggable_widgets = [root, self.top_row, self.artist_label, vol_frame, opac_frame, self.title_label]
        for widget in draggable_widgets:
            widget.bind("<Button-1>", self.start_move)
            widget.bind("<B1-Motion>", self.do_move)

        self.update_loop()

    def shutdown(self):
        self.root.destroy()
        os._exit(0)

    def start_move(self, event):
        if event.widget.winfo_class() == "TScale":
            self.x = None
            return
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        if self.x is not None:
            self.root.geometry(f"+{self.root.winfo_x() + event.x - self.x}+{self.root.winfo_y() + event.y - self.y}")

    def set_volume(self, val):
        if self.volume_ctrl:
            try: self.volume_ctrl.SetMasterVolumeLevelScalar(float(val), None)
            except: pass
            
    def set_opacity(self, val):
        self.root.attributes('-alpha', float(val))

    def update_loop(self):
        async def fetch():
            try:
                manager = await SessionManager.request_async()
                session = manager.get_current_session()
                if session:
                    props = await session.try_get_media_properties_async()
                    timeline = session.get_timeline_properties()
                    
                    # Truncate Title if longer than 18 chars
                    clean_title = props.title if props.title else "Unknown"
                    if len(clean_title) > 18:
                        clean_title = clean_title[:15] + "..."
                    
                    # Truncate Artist if longer than 25 chars
                    clean_artist = props.artist if props.artist else "Unknown Artist"
                    if len(clean_artist) > 28:
                        clean_artist = clean_artist[:25] + "..."

                    self.title_label.config(text=clean_title)
                    self.artist_label.config(text=clean_artist)
                    
                    if timeline and timeline.end_time.total_seconds() > 0:
                        self.progress['value'] = (timeline.position.total_seconds() / timeline.end_time.total_seconds()) * 100
                else:
                    self.title_label.config(text="Inactive")
                    self.artist_label.config(text="No media detected")
                    self.progress['value'] = 0
            except: pass

        try:
            loop = asyncio.new_event_loop()
            loop.run_until_complete(fetch())
        except: pass
        self.root.after(1000, self.update_loop)

    def run_cmd(self, cmd):
        async def execute():
            try:
                manager = await SessionManager.request_async()
                session = manager.get_current_session()
                if session:
                    if cmd == "playpause": await session.try_toggle_play_pause_async()
                    elif cmd == "next": await session.try_skip_next_async()
                    elif cmd == "prev": await session.try_skip_previous_async()
            except: pass
        asyncio.run(execute())

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TProgressbar", thickness=4, background="#1DB954", troughcolor="#333", borderwidth=0)
    style.configure("TScale", background="#121212", troughcolor="#333", borderwidth=0)
    app = VerticalMediaController(root)
    root.mainloop()