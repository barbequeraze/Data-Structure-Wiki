import tkinter as tk

import customtkinter as ctk

from ds_wiki import TOPICS, SECTIONS

ctk.set_appearance_mode("dark")

BG, PANEL, CARD = "#0f1020", "#16172b", "#1d1f3a"
TEXT, MUTED = "#e6e9ff", "#8a8fb8"

META = {
    "Array": ("▦", "#3b82f6", "Contiguous memory. Instant access by index.",
              [("Access", "O(1)"), ("Insert", "O(n)"), ("Delete", "O(n)"), ("Search", "O(n)")]),
    "LinkedList": ("🔗", "#a855f7", "Nodes chained together by pointers.",
                   [("Access", "O(n)"), ("Insert", "O(1)*"), ("Delete", "O(1)*"), ("Search", "O(n)")]),
    "Stack": ("📚", "#f97316", "Last In, First Out. Only the top matters.",
              [("Push", "O(1)"), ("Pop", "O(1)"), ("Peek", "O(1)"), ("Search", "O(n)")]),
    "Queue": ("🚶", "#14b8a6", "First In, First Out. Wait your turn.",
              [("Enqueue", "O(1)"), ("Dequeue", "O(1)"), ("Peek", "O(1)"), ("Search", "O(n)")]),
    "Trees": ("🌳", "#22c55e", "Hierarchical nodes: root, parents, children.",
              [("Insert", "O(n)"), ("Delete", "O(n)"), ("Search", "O(n)"), ("Traverse", "O(n)")]),
    "Binary Trees": ("🌲", "#ec4899", "Two children max. Left < Root < Right.",
                     [("Insert", "O(log n)"), ("Delete", "O(log n)"), ("Search", "O(log n)"), ("Worst", "O(n)")]),
}

META = {k: ("",) + v[1:] for k, v in META.items()}

KEYWORDS = (r"\b(class|def|return|if|elif|else|while|for|in|not|and|or|is|"
            r"None|True|False|import|from|self|break|print)\b")


def hex_rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def rgb_hex(c):
    return "#%02x%02x%02x" % tuple(int(v) for v in c)


def mix(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


class WikiApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Data Structures Wiki")
        self.geometry("1180x740")
        self.minsize(960, 620)
        self.configure(fg_color=BG)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.buttons, self.texts, self.hits = {}, {}, []
        self.visited = set()
        self.current = None
        self.rgb = hex_rgb(META["Array"][1])
        self.anim_token = 0
        self.code_font = ctk.CTkFont(family="Consolas", size=14)

        self._sidebar()
        self._content()
        self.bind("<Control-f>", lambda e: self.entry.focus_set())
        self.select_topic("Array")

    def _sidebar(self):
        side = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color=PANEL)
        side.grid(row=0, column=0, sticky="nsew")
        side.grid_propagate(False)

        ctk.CTkLabel(side, text="✦ DS WIKI", text_color="#ffffff",
                     font=ctk.CTkFont(size=26, weight="bold")).pack(pady=(26, 0))
        ctk.CTkLabel(side, text="DATA STRUCTURES PROJECT", text_color=MUTED,
                     font=ctk.CTkFont(size=10)).pack(pady=(0, 18))

        for name, (icon, accent, _, _) in META.items():
            b = ctk.CTkButton(side, text=f"{icon}   {name}", anchor="w",
                              height=42, corner_radius=12,
                              fg_color="transparent", text_color=TEXT,
                              hover_color=CARD, font=ctk.CTkFont(size=15),
                              command=lambda n=name: self.select_topic(n))
            b.pack(fill="x", padx=14, pady=2)
            self.buttons[name] = b

        ctk.CTkLabel(side, text="SEARCH  (Ctrl+F)", text_color=MUTED,
                     font=ctk.CTkFont(size=10), anchor="w"
                     ).pack(fill="x", padx=20, pady=(22, 3))
        self.entry = ctk.CTkEntry(side, placeholder_text="shift, LIFO, pointer...",
                                  corner_radius=12, height=36, fg_color=CARD,
                                  border_width=0)
        self.entry.pack(fill="x", padx=14)
        self.entry.bind("<Return>", lambda e: self.search())

        self.results = ctk.CTkScrollableFrame(side, fg_color="transparent")
        self.results.pack(fill="both", expand=True, padx=6, pady=8)

    def _content(self):
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.grid(row=0, column=1, sticky="nsew", padx=18, pady=16)
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(2, weight=1)

        self.banner = tk.Canvas(main, height=120, highlightthickness=0, bg=BG)
        self.banner.grid(row=0, column=0, sticky="ew")
        self.banner.bind("<Configure>", lambda e: self.draw_banner())

        self.chips = ctk.CTkFrame(main, fg_color="transparent")
        self.chips.grid(row=1, column=0, sticky="w", pady=12)

        self.tabs = ctk.CTkTabview(
            main, corner_radius=16, fg_color=CARD, text_color="#ffffff",
            segmented_button_fg_color=PANEL,
            segmented_button_unselected_color=PANEL,
            segmented_button_unselected_hover_color="#2a2d52")
        self.tabs.grid(row=2, column=0, sticky="nsew")

        for section in SECTIONS:
            tab = self.tabs.add(section)
            tab.grid_columnconfigure(0, weight=1)
            tab.grid_rowconfigure(0, weight=1)
            box = ctk.CTkTextbox(tab, font=self.code_font, wrap="word",
                                 fg_color=CARD, text_color=TEXT, border_width=0,
                                 state="disabled")
            box.grid(row=0, column=0, sticky="nsew")
            tb = box._textbox
            tb.configure(padx=16, pady=12, spacing1=3)

            tb.tag_config("kw", foreground="#ff79c6")
            tb.tag_config("num", foreground="#f1fa8c")
            tb.tag_config("str", foreground="#50fa7b")
            tb.tag_config("cmt", foreground="#6272a4")
            tb.tag_config("bigo", foreground="#ffb86c")
            tb.tag_config("step", foreground="#ffffff")
            tb.tag_config("hit", background="#f9e2af", foreground="#11111b")
            self.texts[section] = box

        self.status = ctk.CTkLabel(main, text="", text_color=MUTED, anchor="w",
                                   font=ctk.CTkFont(size=11))
        self.status.grid(row=3, column=0, sticky="ew", pady=(8, 0))

    def draw_banner(self):
        c, w = self.banner, max(self.banner.winfo_width(), 200)
        c.delete("all")
        left, right = mix((0, 0, 0), self.rgb, 0.85), hex_rgb(BG)
        for x in range(0, w, 4):
            c.create_rectangle(x, 0, x + 4, 120,
                               fill=rgb_hex(mix(left, right, x / w)), width=0)
        accent = rgb_hex(self.rgb)
        for r, wd in ((90, 2), (60, 2), (30, 3)):         
            c.create_oval(w - 110 - r, 60 - r, w - 110 + r, 60 + r,
                          outline=accent, width=wd)
        if self.current:
            icon, _, tagline, _ = META[self.current]
            c.create_text(28, 46, anchor="w", text=self.current.upper(),
                          font=("Segoe UI", 30, "bold"), fill="#ffffff")
            c.create_text(30, 90, anchor="w", text=tagline,
                          font=("Segoe UI", 12), fill="#dfe3ff")

    def animate_to(self, target_hex):
        self.anim_token += 1
        token, start, end = self.anim_token, self.rgb, hex_rgb(target_hex)

        def tick(i):
            if token != self.anim_token:
                return
            self.rgb = mix(start, end, i / 12)
            self.draw_banner()
            if i < 12:
                self.after(16, tick, i + 1)
        tick(1)

    def paint(self, tb, tag, pattern):
        count, start = tk.IntVar(), "1.0"
        while True:
            pos = tb.search(pattern, start, stopindex="end", regexp=True,
                            count=count)
            if not pos:
                return
            n = count.get()
            if n == 0:
                start = f"{pos}+1c"
                continue
            end = f"{pos}+{n}c"
            tb.tag_add(tag, pos, end)
            start = end

    def select_topic(self, name, section=None):
        icon, accent, _, chips = META[name]
        self.current = name
        self.visited.add(name)
        self.animate_to(accent)

        for n, b in self.buttons.items():
            mark = "" if n in self.visited else ""
            b.configure(text=f"{META[n][0]}   {n}{mark}",
                        fg_color=accent if n == name else "transparent",
                        text_color="#ffffff" if n == name else TEXT,
                        hover_color=accent if n == name else CARD)

        self.tabs.configure(segmented_button_selected_color=accent,
                            segmented_button_selected_hover_color=accent)

        for w in self.chips.winfo_children():
            w.destroy()
        for label, bigo in chips:
            ctk.CTkLabel(self.chips, text=f"{label}  {bigo}", corner_radius=14,
                         fg_color=CARD, text_color=accent, height=30,
                         font=ctk.CTkFont(size=12, weight="bold"), padx=14
                         ).pack(side="left", padx=(0, 8))

        for sec, box in self.texts.items():
            tb = box._textbox
            box.configure(state="normal")
            box.delete("1.0", "end")
            box.insert("1.0", TOPICS[name][sec].strip("\n"))
            tb.tag_config("step", foreground=accent)
            if sec == "Sample code":
                self.paint(tb, "kw", KEYWORDS)
                self.paint(tb, "num", r"\b\d+\b")
                self.paint(tb, "str", r"(\"[^\"\n]*\"|'[^'\n]*')")
                self.paint(tb, "cmt", r"#[^\n]*")
            else:
                self.paint(tb, "step", r"^\s*(\d+\.|Case \d)")
                self.paint(tb, "bigo", r"O\([^)]*\)")
            box.configure(state="disabled")

        self.tabs.set(section or SECTIONS[0])
        self.status.configure(
            text=f"{len(self.visited)}/{len(META)} modules explored  •  "
                 f"Ctrl+F to search")

    def search(self):
        for w in self.results.winfo_children():
            w.destroy()
        term = self.entry.get().strip()
        self.hits = []
        if not term:
            return
        for topic, secs in TOPICS.items():
            for sec, body in secs.items():
                if term.lower() in body.lower():
                    self.hits.append((topic, sec))
        if not self.hits:
            ctk.CTkLabel(self.results, text="No matches found.",
                         text_color=MUTED).pack(pady=8)
            return
        for topic, sec in self.hits:
            ctk.CTkButton(self.results, text=f"{META[topic][0]} {topic} › {sec}",
                          anchor="w", height=30, corner_radius=8,
                          fg_color="transparent", text_color=TEXT,
                          hover_color=CARD,
                          command=lambda t=topic, s=sec: self.open_result(t, s)
                          ).pack(fill="x", pady=1)

    def open_result(self, topic, section):
        self.select_topic(topic, section)
        tb = self.texts[section]._textbox
        tb.tag_remove("hit", "1.0", "end")
        term, start = self.entry.get().strip(), "1.0"
        while term:
            pos = tb.search(term, start, stopindex="end", nocase=True)
            if not pos:
                break
            end = f"{pos}+{len(term)}c"
            tb.tag_add("hit", pos, end)
            start = end


if __name__ == "__main__":
    WikiApp().mainloop()
