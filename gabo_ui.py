import tkinter as tk
from tkinter import scrolledtext
import threading

from gabo_core import think


class GABOUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GABO")
        self.root.geometry("800x600")
        self.root.configure(bg="#111111")

        self.voice_running = False

        # -------------------------
        # Header
        # -------------------------

        header = tk.Frame(
            root,
            bg="#181818",
            height=55
        )
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="GABO",
            font=("Segoe UI", 18, "bold"),
            fg="white",
            bg="#181818"
        )
        title.pack(side="left", padx=20, pady=10)

        self.status = tk.Label(
            header,
            text="● ONLINE",
            font=("Segoe UI", 10),
            fg="#66ff99",
            bg="#181818"
        )
        self.status.pack(side="right", padx=20)

        # -------------------------
        # Conversation
        # -------------------------

        self.chat = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            bg="#101010",
            fg="#eeeeee",
            insertbackground="white",
            font=("Segoe UI", 11),
            relief="flat",
            padx=15,
            pady=15
        )

        self.chat.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(10, 5)
        )

        self.chat.configure(state="disabled")

        # -------------------------
        # Input area
        # -------------------------

        input_frame = tk.Frame(
            root,
            bg="#111111"
        )
        input_frame.pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.entry = tk.Entry(
            input_frame,
            bg="#202020",
            fg="white",
            insertbackground="white",
            font=("Segoe UI", 11),
            relief="flat"
        )

        self.entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=10,
            padx=(0, 8)
        )

        self.entry.bind(
            "<Return>",
            lambda event: self.send_text()
        )

        send_button = tk.Button(
            input_frame,
            text="Send",
            command=self.send_text,
            bg="#303030",
            fg="white",
            activebackground="#404040",
            activeforeground="white",
            relief="flat",
            padx=18
        )

        send_button.pack(side="right")

        # -------------------------
        # Controls
        # -------------------------

        controls = tk.Frame(
            root,
            bg="#181818"
        )
        controls.pack(fill="x")

        self.voice_button = tk.Button(
            controls,
            text="🎤 Voice",
            command=self.toggle_voice,
            bg="#222222",
            fg="white",
            activebackground="#333333",
            activeforeground="white",
            relief="flat",
            padx=15
        )

        self.voice_button.pack(
            side="left",
            padx=10,
            pady=8
        )

        system_button = tk.Button(
            controls,
            text="System",
            command=self.show_system,
            bg="#222222",
            fg="white",
            activebackground="#333333",
            activeforeground="white",
            relief="flat",
            padx=15
        )

        system_button.pack(
            side="right",
            padx=10
        )

        self.add_message(
            "GABO",
            "Text interface initialized."
        )

    # ==================================
    # Chat
    # ==================================

    def add_message(self, sender, message):
        self.chat.configure(state="normal")

        self.chat.insert(
            tk.END,
            f"{sender}\n",
            sender
        )

        self.chat.insert(
            tk.END,
            f"{message}\n\n"
        )

        self.chat.configure(state="disabled")
        self.chat.see(tk.END)

    # ==================================
    # Text interface
    # ==================================

    def send_text(self):
        text = self.entry.get().strip()

        if not text:
            return

        self.entry.delete(0, tk.END)

        self.add_message(
            "YOU",
            text
        )

        self.status.config(
            text="● THINKING",
            fg="#ffff66"
        )

        # Don't freeze Tkinter while GABO thinks.
        threading.Thread(
            target=self.process_text,
            args=(text,),
            daemon=True
        ).start()

    def process_text(self, text):
        try:
            response = think(text)

            self.root.after(
                0,
                lambda: self.finish_response(response)
            )

        except Exception as e:
            self.root.after(
                0,
                lambda: self.finish_response(
                    f"Internal error: {e}"
                )
            )

    def finish_response(self, response):
        self.add_message(
            "GABO",
            response
        )

        self.status.config(
            text="● ONLINE",
            fg="#66ff99"
        )

    # ==================================
    # Voice
    # ==================================

    def toggle_voice(self):

        if not self.voice_running:
            self.start_voice()

        else:
            self.stop_voice()

    def start_voice(self):

        self.voice_running = True

        self.voice_button.config(
            text="🎤 Voice ON"
        )

        self.status.config(
            text="● LISTENING",
            fg="#66ccff"
        )

        # Import only when needed.
        import wake_listen

        threading.Thread(
            target=wake_listen.run,
            daemon=True
        ).start()

    def stop_voice(self):

        self.voice_running = False

        self.voice_button.config(
            text="🎤 Voice"
        )

        self.status.config(
            text="● ONLINE",
            fg="#66ff99"
        )

    # ==================================
    # System
    # ==================================

    def show_system(self):

        self.add_message(
            "SYSTEM",
            "GABO systems nominal."
        )


if __name__ == "__main__":

    root = tk.Tk()

    app = GABOUI(root)

    root.mainloop()