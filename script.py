import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

# Função para adicionar tarefa normal
def adicionar_tarefa():
    tarefa = entrada_tarefa.get()
    if tarefa:
        lista_tarefas.insert(tk.END, f"📌 {tarefa}")
        entrada_tarefa.delete(0, tk.END)
    else:
        messagebox.showwarning("Campo vazio", "Digite uma tarefa!")

# Função para remover tarefa
def remover_tarefa():
    try:
        selecionada = lista_tarefas.curselection()
        lista_tarefas.delete(selecionada)
    except:
        messagebox.showwarning("Seleção inválida", "Selecione uma tarefa para remover.")

# Função para criar cronograma de estudo
def gerar_cronograma():
    inicio = entrada_inicio.get()
    fim = entrada_fim.get()

    try:
        inicio_dt = datetime.strptime(inicio, "%H:%M")
        fim_dt = datetime.strptime(fim, "%H:%M")

        if inicio_dt >= fim_dt:
            raise ValueError

        lista_cronograma.delete(0, tk.END)
        atual = inicio_dt

        while atual + timedelta(minutes=30) <= fim_dt:
            lista_cronograma.insert(tk.END, f"📘 Estudo: {atual.strftime('%H:%M')} - {(atual + timedelta(minutes=30)).strftime('%H:%M')}")
            atual += timedelta(minutes=30)

            if atual + timedelta(minutes=10) <= fim_dt:
                pausa = 10 if (atual.minute % 60 == 0 or lista_cronograma.size() == 1) else 20
                lista_cronograma.insert(tk.END, f"☕ Pausa: {atual.strftime('%H:%M')} - {(atual + timedelta(minutes=pausa)).strftime('%H:%M')}")
                atual += timedelta(minutes=pausa)
    except:
        messagebox.showerror("Erro", "Insira os horários no formato HH:MM (ex: 14:00)")

# Criação da janela principal
root = tk.Tk()
root.title("To-Do List + Estudo Planner")
root.geometry("600x700")
root.configure(bg="#1e1e2e")

# Estilo ttk
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", background="#44475a", foreground="white", font=('Segoe UI', 10), padding=6)
style.configure("TEntry", padding=6)
style.configure("TLabel", background="#1e1e2e", foreground="white", font=('Segoe UI', 10))
style.configure("TListbox", background="#282a36", foreground="white")

# ---------------- SEÇÃO DE TAREFAS ---------------- #
frame_tarefas = ttk.LabelFrame(root, text="📋 Tarefas", padding=10)
frame_tarefas.pack(padx=20, pady=20, fill="x")

entrada_tarefa = ttk.Entry(frame_tarefas, width=40)
entrada_tarefa.pack(pady=5)

btn_adicionar = ttk.Button(frame_tarefas, text="Adicionar Tarefa", command=adicionar_tarefa)
btn_adicionar.pack(pady=5)

lista_tarefas = tk.Listbox(frame_tarefas, height=8, bg="#282a36", fg="white", font=("Segoe UI", 10))
lista_tarefas.pack(pady=5, fill="x")

btn_remover = ttk.Button(frame_tarefas, text="Remover Tarefa", command=remover_tarefa)
btn_remover.pack(pady=5)

# ---------------- SEÇÃO DE ESTUDO ---------------- #
frame_estudo = ttk.LabelFrame(root, text="📚 Planejamento de Estudo", padding=10)
frame_estudo.pack(padx=20, pady=20, fill="x")

ttk.Label(frame_estudo, text="Horário de Início (HH:MM):").pack(pady=2)
entrada_inicio = ttk.Entry(frame_estudo)
entrada_inicio.pack(pady=2)

ttk.Label(frame_estudo, text="Horário de Fim (HH:MM):").pack(pady=2)
entrada_fim = ttk.Entry(frame_estudo)
entrada_fim.pack(pady=2)

btn_cronograma = ttk.Button(frame_estudo, text="Gerar Cronograma", command=gerar_cronograma)
btn_cronograma.pack(pady=10)

lista_cronograma = tk.Listbox(frame_estudo, height=10, bg="#282a36", fg="white", font=("Segoe UI", 10))
lista_cronograma.pack(pady=5, fill="x")

root.mainloop()
