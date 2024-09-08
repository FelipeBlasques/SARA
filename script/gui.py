import tkinter as tk
from tkinter import scrolledtext, messagebox
from script.email_handler import connect_and_fetch_emails
from script.logger import log
from script.config import email_user
from threading import Thread
import os

emails = []

def run_app():
    root = tk.Tk()
    root.title("SARA")
    root.geometry("1000x700")
    root.configure(bg="#e0e0e0")

    # Cabeçalho
    header_frame = tk.Frame(root, bg="#0078d4", pady=10)
    header_frame.pack(fill=tk.X)
    header_label = tk.Label(header_frame, text="Smart Automated Receive Application", 
                            font=("Arial", 16, "bold"), fg="white", bg="#0078d4")
    header_label.pack()

    # Área de lista de e-mails
    email_list_frame = tk.Frame(root, bg="#e0e0e0")
    email_list_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    email_list = tk.Listbox(email_list_frame, width=40, height=5, bg="white", selectmode=tk.SINGLE, font=("Arial", 12))
    email_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Barra de rolagem
    scrollbar = tk.Scrollbar(email_list_frame, orient=tk.VERTICAL, command=email_list.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    email_list.config(yscrollcommand=scrollbar.set)

    # Área de exibição de e-mails
    email_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=15, state=tk.DISABLED, bg="white", font=("Arial", 12))
    email_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Funções da interface
    def update_email_list(emails):
        email_list.delete(0, tk.END)
        for i, (subject, destinatario, date_, _) in enumerate(emails):
            email_list.insert(tk.END, f"{i + 1}. {subject} - {date_.strftime('%Y-%m-%d %H:%M:%S')}")

    def show_email_content(event):
        try:
            index = email_list.curselection()[0]
            subject, destinatario, date_, body = emails[index]
            email_display.config(state=tk.NORMAL)
            email_display.delete(1.0, tk.END)
            email_display.insert(tk.END, f"Assunto: {subject}\nData: {date_.strftime('%Y-%m-%d %H:%M:%S')}\nConteúdo:\n{body}\n")
            email_display.config(state=tk.DISABLED)
        except IndexError:
            pass

    email_list.bind("<ButtonRelease-1>", show_email_content)

    def clear_email_content():
        email_display.config(state=tk.NORMAL)
        email_display.delete(1.0, tk.END)
        email_display.config(state=tk.DISABLED)

    def check_emails():
        global emails
        try:
            emails = connect_and_fetch_emails(email_user)
            update_email_list(emails)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # Função para atualizar o log na interface gráfica
    def update_log():
        log_text.config(state=tk.NORMAL)
        log_text.delete(1.0, tk.END)
        try:
            with open('email_checker.log', 'r') as file:
                log_text.insert(tk.END, file.read())
            log_text.config(state=tk.DISABLED)
            log_text.yview(tk.END)
        except FileNotFoundError:
            log_text.insert(tk.END, "Log ainda não criado.\n")
        finally:
            # Atualiza o log a cada 2 segundos
            root.after(2000, update_log)

    # Botões
    button_frame = tk.Frame(root, bg="#e0e0e0", pady=10)
    button_frame.pack(fill=tk.X)
    start_button = tk.Button(button_frame, text="Verificar E-mails", command=lambda: Thread(target=check_emails).start(), 
                             bg="#0078d4", fg="white", font=("Arial", 12))
    start_button.pack(side=tk.LEFT, padx=5)

    clear_button = tk.Button(button_frame, text="Limpar Conteúdo", command=clear_email_content, 
                             bg="#0078d4", fg="white", font=("Arial", 12))
    clear_button.pack(side=tk.LEFT, padx=5)

    # Área de log
    log_frame = tk.Frame(root, bg="#e0e0e0", pady=10)
    log_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    log_label = tk.Label(log_frame, text="Log", font=("Arial", 12, "bold"), bg="#e0e0e0")
    log_label.pack()
    log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, width=70, height=8, state=tk.DISABLED, bg="white", font=("Arial", 10))
    log_text.pack(fill=tk.BOTH, expand=True)

    # Iniciar atualização periódica do log
    update_log()

    root.mainloop()
