import json
import socket
import threading
import tkinter as tk
from tkinter import messagebox

# Palette de couleurs "Dark Gamer Neon"
BG_DARK = "#0a0a12"
PANEL_BG = "#13131f"
TEXT_COLOR = "#f1f5f9"
ACCENT_VIOLET = "#a855f7"
ACCENT_CYAN = "#06b6d4"
BUTTON_HOVER = "#9333ea"
BTN_BG = "#1e1e30"
SUCCESS_GREEN = "#10b981"
ERROR_RED = "#ef4444"


class GamerQuizClient:

    def __init__(self, root):
        self.root = root
        self.root.title("QCM GAMER ARENA - Client")
        self.root.geometry("750x600")
        self.root.config(bg=BG_DARK)
        self.root.resizable(False, False)

        self.sock = None
        self.participant_name = ""
        self.themes = []
        self.selected_theme = tk.StringVar()
        self.selected_level = tk.IntVar(value=1)

        self.current_q_index = 0
        self.total_questions = 0
        self.score = 0
        self.timer_seconds = 20
        self.timer_job = None

        self.create_connection_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ================= 1. ÉCRAN DE CONNEXION =================
    def create_connection_screen(self):
        self.clear_window()

        container = tk.Frame(self.root, bg=PANEL_BG, padx=40, pady=40)
        container.place(relx=0.5, rely=0.5, anchor="center", width=520, height=450)

        title_lbl = tk.Label(
            container,
            text="⚡ QCM ARENA ⚡",
            font=("Consolas", 24, "bold"),
            bg=PANEL_BG,
            fg=ACCENT_CYAN,
        )
        title_lbl.pack(pady=(0, 20))

        # Nom du participant
        tk.Label(
            container,
            text="PSEUDO DU PARTICIPANT",
            font=("Consolas", 10, "bold"),
            bg=PANEL_BG,
            fg=TEXT_COLOR,
        ).pack(anchor="w")
        self.name_entry = tk.Entry(
            container,
            font=("Consolas", 12),
            bg=BG_DARK,
            fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
            relief="flat",
        )
        self.name_entry.pack(fill="x", pady=(5, 15), ipady=6)
        self.name_entry.insert(0, "Gamer_X")

        # IP Serveur (Support VPN)
        tk.Label(
            container,
            text="IP SERVEUR / VPN",
            font=("Consolas", 10, "bold"),
            bg=PANEL_BG,
            fg=TEXT_COLOR,
        ).pack(anchor="w")
        self.ip_entry = tk.Entry(
            container,
            font=("Consolas", 12),
            bg=BG_DARK,
            fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
            relief="flat",
        )
        self.ip_entry.pack(fill="x", pady=(5, 15), ipady=6)
        self.ip_entry.insert(
            0, "127.0.0.1"
        )  # Mettre l'IP VPN du serveur si distant

        connect_btn = tk.Button(
            container,
            text="CONNEXION AU SERVEUR",
            font=("Consolas", 12, "bold"),
            bg=ACCENT_VIOLET,
            fg="#ffffff",
            activebackground=BUTTON_HOVER,
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            command=self.connect_to_server,
        )
        connect_btn.pack(fill="x", pady=(20, 0), ipady=8)

    def connect_to_server(self):
        self.participant_name = self.name_entry.get().strip()
        server_ip = self.ip_entry.get().strip()

        if not self.participant_name:
            messagebox.showerror("Erreur", "Veuillez entrer un pseudo valide.")
            return

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((server_ip, 5555))

            # Recevoir la liste des thèmes
            themes_raw = self.sock.recv(4096).decode("utf-8")
            self.themes = json.loads(themes_raw)

            self.create_lobby_screen()
        except Exception as e:
            messagebox.showerror(
                "Erreur de connexion",
                f"Impossible de joindre le serveur :\n{e}",
            )

    # ================= 2. ÉCRAN DE LOBBY (THÈMES & NIVEAUX) =================
    def create_lobby_screen(self):
        self.clear_window()

        container = tk.Frame(self.root, bg=PANEL_BG, padx=30, pady=30)
        container.place(relx=0.5, rely=0.5, anchor="center", width=620, height=520)

        tk.Label(
            container,
            text=f"BIENVENUE, {self.participant_name.upper()} !",
            font=("Consolas", 16, "bold"),
            bg=PANEL_BG,
            fg=ACCENT_CYAN,
        ).pack(pady=(0, 15))

        # Choix du thème
        tk.Label(
            container,
            text="CHOISISSEZ UN THÈME DE JEU :",
            font=("Consolas", 11, "bold"),
            bg=PANEL_BG,
            fg=TEXT_COLOR,
        ).pack(anchor="w", pady=(0, 5))

        if self.themes:
            self.selected_theme.set(self.themes[0])

        for theme in self.themes:
            rb = tk.Radiobutton(
                container,
                text=theme,
                variable=self.selected_theme,
                value=theme,
                font=("Consolas", 11),
                bg=PANEL_BG,
                fg=TEXT_COLOR,
                selectcolor=BG_DARK,
                activebackground=PANEL_BG,
                activeforeground=ACCENT_VIOLET,
            )
            rb.pack(anchor="w", pady=2)

        # Choix du niveau
        tk.Label(
            container,
            text="CHOISISSEZ LE NIVEAU :",
            font=("Consolas", 11, "bold"),
            bg=PANEL_BG,
            fg=TEXT_COLOR,
        ).pack(anchor="w", pady=(15, 5))

        levels_frame = tk.Frame(container, bg=PANEL_BG)
        levels_frame.pack(anchor="w", fill="x")

        tk.Radiobutton(
            levels_frame,
            text="Niveau 1 (5 Questions)",
            variable=self.selected_level,
            value=1,
            font=("Consolas", 10),
            bg=PANEL_BG,
            fg=TEXT_COLOR,
            selectcolor=BG_DARK,
            activebackground=PANEL_BG,
            activeforeground=ACCENT_CYAN,
        ).pack(side="left", padx=(0, 15))
        tk.Radiobutton(
            levels_frame,
            text="Niveau 2 (10 Questions)",
            variable=self.selected_level,
            value=2,
            font=("Consolas", 10),
            bg=PANEL_BG,
            fg=TEXT_COLOR,
            selectcolor=BG_DARK,
            activebackground=PANEL_BG,
            activeforeground=ACCENT_CYAN,
        ).pack(side="left", padx=(0, 15))
        tk.Radiobutton(
            levels_frame,
            text="Niveau 3 (15 Questions)",
            variable=self.selected_level,
            value=3,
            font=("Consolas", 10),
            bg=PANEL_BG,
            fg=TEXT_COLOR,
            selectcolor=BG_DARK,
            activebackground=PANEL_BG,
            activeforeground=ACCENT_CYAN,
        ).pack(side="left")

        start_btn = tk.Button(
            container,
            text="LANCER LA PARTIE",
            font=("Consolas", 12, "bold"),
            bg=ACCENT_CYAN,
            fg=BG_DARK,
            activebackground="#0891b2",
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            command=self.start_quiz_session,
        )
        start_btn.pack(fill="x", pady=(30, 0), ipady=8)

    def start_quiz_session(self):
        # Envoyer choix au serveur
        payload = {
            "theme": self.selected_theme.get(),
            "level": self.selected_level.get(),
        }
        self.sock.sendall(json.dumps(payload).encode("utf-8"))

        # Recevoir le total des questions
        total_raw = self.sock.recv(1024).decode("utf-8")
        total_data = json.loads(total_raw)
        self.total_questions = total_data.get("total")

        self.create_quiz_screen()

    # ================= 3. ÉCRAN DU QUIZ =================
    def create_quiz_screen(self):
        self.clear_window()

        self.quiz_container = tk.Frame(self.root, bg=PANEL_BG, padx=30, pady=30)
        self.quiz_container.place(
            relx=0.5, rely=0.5, anchor="center", width=680, height=520
        )

        # En-tête : Progression et Chrono
        top_bar = tk.Frame(self.quiz_container, bg=PANEL_BG)
        top_bar.pack(fill="x", pady=(0, 15))

        self.progress_lbl = tk.Label(
            top_bar,
            text="Question 1 / 5",
            font=("Consolas", 11, "bold"),
            bg=PANEL_BG,
            fg=ACCENT_CYAN,
        )
        self.progress_lbl.pack(side="left")

        self.timer_lbl = tk.Label(
            top_bar,
            text="⏱ 20s",
            font=("Consolas", 12, "bold"),
            bg=PANEL_BG,
            fg=ACCENT_VIOLET,
        )
        self.timer_lbl.pack(side="right")

        # Question Display
        self.q_text_lbl = tk.Label(
            self.quiz_container,
            text="Chargement de la question...",
            font=("Consolas", 13),
            bg=PANEL_BG,
            fg=TEXT_COLOR,
            wraplength=600,
            justify="left",
        )
        self.q_text_lbl.pack(anchor="w", pady=(10, 20))

        # Boutons de choix
        self.choice_buttons = []
        for i in range(4):
            btn = tk.Button(
                self.quiz_container,
                text="",
                font=("Consolas", 11),
                bg=BTN_BG,
                fg=TEXT_COLOR,
                activebackground=ACCENT_VIOLET,
                activeforeground="#ffffff",
                relief="flat",
                anchor="w",
                padx=15,
                command=lambda idx=i: self.submit_answer(idx),
            )
            btn.pack(fill="x", pady=6, ipady=6)
            self.choice_buttons.append(btn)

        # Lancer la réception de la première question en arrière-plan
        threading.Thread(target=self.receive_question_loop, daemon=True).start()

    def receive_question_loop(self):
        try:
            q_raw = self.sock.recv(4096).decode("utf-8")
            if not q_raw:
                return
            q_data = json.loads(q_raw)

            # Vérifier si c'est le message de score final ou une question
            if "final_score" in q_data:
                self.root.after(0, lambda: self.create_result_screen(q_data))
                return

            index = q_data.get("index")
            total = q_data.get("total")
            question = q_data.get("question")
            choices = q_data.get("choices")

            # Mettre à jour l'interface dans le thread principal
            self.root.after(
                0, lambda: self.display_question(index, total, question, choices)
            )

        except Exception as e:
            print(f"Erreur réception : {e}")

    def display_question(self, index, total, question, choices):
        self.progress_lbl.config(text=f"Question {index} / {total}")
        self.q_text_lbl.config(text=question)

        for i, choice_text in enumerate(choices):
            self.choice_buttons[i].config(
                text=f"  {chr(65 + i)} {choice_text}",
                state="normal",
                bg=BTN_BG,
                fg=TEXT_COLOR,
            )

        # Lancer le chronomètre de 20 secondes par question
        self.timer_seconds = 20
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
        self.run_timer()

    def run_timer(self):
        if self.timer_seconds > 0:
            self.timer_lbl.config(text=f"⏱ {self.timer_seconds}s")
            self.timer_seconds -= 1
            self.timer_job = self.root.after(1000, self.run_timer)
        else:
            # Temps écoulé -> envoyer -1 par défaut
            self.submit_answer(-1)

    def submit_answer(self, choice_index):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)

        # Désactiver les boutons pendant la validation
        for btn in self.choice_buttons:
            btn.config(state="disabled")

        # Envoyer la réponse au serveur
        try:
            self.sock.sendall(json.dumps({"answer": choice_index}).encode("utf-8"))

            # Recevoir le feedback
            feedback_raw = self.sock.recv(2048).decode("utf-8")
            feedback = json.loads(feedback_raw)

            if "final_score" in feedback:
                self.create_result_screen(feedback)
                return

            correct_ans = feedback.get("correct_answer")
            is_correct = feedback.get("correct")

            # Colorer les boutons (Vert pour correct, Rouge pour faux choisi)
            if 0 <= choice_index < 4:
                if is_correct:
                    self.choice_buttons[choice_index].config(
                        bg=SUCCESS_GREEN, fg="#ffffff"
                    )
                else:
                    self.choice_buttons[choice_index].config(
                        bg=ERROR_RED, fg="#ffffff"
                    )
                    self.choice_buttons[correct_ans].config(
                        bg=SUCCESS_GREEN, fg="#ffffff"
                    )
            else:
                # Temps écoulé
                self.choice_buttons[correct_ans].config(
                    bg=SUCCESS_GREEN, fg="#ffffff"
                )

            # Passer à la question suivante après 1.5 secondes
            self.root.after(1500, self.fetch_next_or_finish)

        except Exception as e:
            print(f"Erreur soumission : {e}")

    def fetch_next_or_finish(self):
        threading.Thread(target=self.receive_question_loop, daemon=True).start()

    # ================= 4. ÉCRAN DES RÉSULTATS =================
    def create_result_screen(self, result_data):
        self.clear_window()

        container = tk.Frame(self.root, bg=PANEL_BG, padx=40, pady=40)
        container.place(relx=0.5, rely=0.5, anchor="center", width=520, height=420)

        tk.Label(
            container,
            text="🏆 FIN DE LA PARTIE 🏆",
            font=("Consolas", 18, "bold"),
            bg=PANEL_BG,
            fg=ACCENT_CYAN,
        ).pack(pady=(0, 10))

        tk.Label(
            container,
            text=f"Participant : {self.participant_name.upper()}",
            font=("Consolas", 12),
            bg=PANEL_BG,
            fg=TEXT_COLOR,
        ).pack(pady=(0, 20))

        score = result_data.get("final_score")
        max_score = result_data.get("max_score")
        percentage = (score / max_score) * 100 if max_score > 0 else 0

        score_frame = tk.Frame(container, bg=BG_DARK, padx=20, pady=20)
        score_frame.pack(fill="x", pady=10)

        tk.Label(
            score_frame,
            text=f"SCORE TOTAL : {score} / {max_score} pts",
            font=("Consolas", 16, "bold"),
            bg=BG_DARK,
            fg=ACCENT_VIOLET,
        ).pack()

        tk.Label(
            score_frame,
            text=f"Réussite : {percentage:.1f}%",
            font=("Consolas", 12),
            bg=BG_DARK,
            fg=TEXT_COLOR,
        ).pack(pady=(5, 0))

        restart_btn = tk.Button(
            container,
            text="REJOUER UNE PARTIE",
            font=("Consolas", 12, "bold"),
            bg=ACCENT_CYAN,
            fg=BG_DARK,
            activebackground="#0891b2",
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            command=self.create_connection_screen,
        )
        restart_btn.pack(fill="x", pady=(25, 0), ipady=8)

        if self.sock:
            try:
                self.sock.close()
            except:
                pass


if __name__ == "__main__":
    root = tk.Tk()
    app = GamerQuizClient(root)
    root.mainloop()