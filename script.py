import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

# Função para adicionar tarefa
def adicionar_tarefa():
    tarefa = entrada_tarefa.get().strip()
    if tarefa:
        lista_tarefas.insert(tk.END, tarefa.capitalize())
        entrada_tarefa.delete(0, tk.END)
    else:
        messagebox.showwarning("Campo vazio", "Digite uma tarefa!")

# Função para remover tarefa
def remover_tarefa():
    selecionada = lista_tarefas.curselection()
    if selecionada:
        lista_tarefas.delete(selecionada)
    else:
        messagebox.showwarning("Selecione", "Escolha uma tarefa para remover.")

# Função para abrir janela de cronograma se a tarefa for "Estudar"
def checar_duplo_clique(event):
    indice = lista_tarefas.curselection()
    if indice:
        tarefa = lista_tarefas.get(indice[0]).lower()
        if "estudar" in tarefa:
            abrir_cronograma()

# Função para gerar o cronograma de estudo
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

        blocos = [
            (20, 10),
            (30, 20),
            (60, 20),
            (120, 30),
        ]

        bloco_atual = 0

        while atual < fim_dt:
            if bloco_atual < len(blocos):
                estudo_min, descanso_min = blocos[bloco_atual]
            else:
                estudo_min, descanso_min = 120, 30

            fim_estudo = atual + timedelta(minutes=estudo_min)
            if fim_estudo > fim_dt:
                estudo_min = int((fim_dt - atual).total_seconds() // 60)
                fim_estudo = fim_dt

            lista_cronograma.insert(tk.END, f"🧠 Estudo: {atual.strftime('%H:%M')} - {fim_estudo.strftime('%H:%M')}")
            atual = fim_estudo

            if atual >= fim_dt:
                break

            fim_descanso = atual + timedelta(minutes=descanso_min)
            if fim_descanso >= fim_dt:
                lista_cronograma.delete(tk.END)
                lista_cronograma.insert(tk.END, f"🧠 Estudo: {inicio_dt.strftime('%H:%M')} - {fim_dt.strftime('%H:%M')}")
                break

            lista_cronograma.insert(tk.END, f"☕ Descanso: {atual.strftime('%H:%M')} - {fim_descanso.strftime('%H:%M')}")
            atual = fim_descanso

            bloco_atual += 1

    except Exception as e:
        print(e)
        messagebox.showerror("Formato inválido", "Use o formato HH:MM (ex: 14:00)")

# Função para abrir a janela de cronograma
def abrir_cronograma():
    janela = tk.Toplevel(root)
    janela.title("Gerar Cronograma de Estudo")
    janela.geometry("400x500")
    janela.configure(bg="#f9f9f9")

    ttk.Label(janela, text="Horário de Início (HH:MM):", style="TLabel").pack(pady=10)
    global entrada_inicio
    entrada_inicio = ttk.Entry(janela, font=('Segoe UI Light', 11))
    entrada_inicio.pack(pady=10, ipadx=10, ipady=5)

    ttk.Label(janela, text="Horário de Fim (HH:MM):", style="TLabel").pack(pady=10)
    global entrada_fim
    entrada_fim = ttk.Entry(janela, font=('Segoe UI Light', 11))
    entrada_fim.pack(pady=10, ipadx=10, ipady=5)

    ttk.Button(janela, text="Gerar Cronograma", style="RoundedButton.TButton", command=gerar_cronograma).pack(pady=20)

    global lista_cronograma
    lista_cronograma = tk.Listbox(janela, bg="#eeeeee", fg="#333333", font=('Segoe UI', 10), bd=0, highlightthickness=0, selectbackground="#c0c0c0", relief="flat")
    lista_cronograma.pack(padx=20, pady=10, fill="both", expand=True)

# --------------------------- #
# Janela Principal
root = tk.Tk()
root.title("To-Do Minimalista + Estudo")
root.geometry("400x500")
root.configure(bg="#f9f9f9")

# Estilo moderno
style = ttk.Style()
style.theme_use("clam")

style.configure("TButton",
    font=('Segoe UI', 10),
    background="#e0e0e0",
    foreground="#333333",
    borderwidth=0,
    focusthickness=3,
    focuscolor="none",
    padding=10
)

style.configure("RoundedButton.TButton",
    font=('Segoe UI', 10),
    background="#007aff",
    foreground="white",
    borderwidth=0,
    focusthickness=3,
    focuscolor="none",
    padding=10
)

style.map("RoundedButton.TButton",
    background=[('active', '#0051a8')]
)

style.configure("TEntry",
    padding=10,
    relief="flat",
    font=('Segoe UI Light', 11)
)

style.configure("TLabel",
    background="#f9f9f9",
    foreground="#333333",
    font=('Segoe UI Light', 11)
)

# Entrada de tarefas
entrada_tarefa = ttk.Entry(root, font=('Segoe UI Light', 11))
entrada_tarefa.pack(pady=20, padx=20, fill="x", ipadx=10, ipady=5)

# Botões
frame_botoes = ttk.Frame(root, style="TFrame")
frame_botoes.pack(pady=5)

ttk.Button(frame_botoes, text="Adicionar", style="RoundedButton.TButton", command=adicionar_tarefa).pack(side="left", padx=10)
ttk.Button(frame_botoes, text="Remover", style="RoundedButton.TButton", command=remover_tarefa).pack(side="left", padx=10)

# Lista de tarefas
lista_tarefas = tk.Listbox(root, bg="#eeeeee", fg="#333333", font=('Segoe UI', 11), bd=0, highlightthickness=0, selectbackground="#c0c0c0", relief="flat")
lista_tarefas.pack(padx=20, pady=20, fill="both", expand=True)

lista_tarefas.bind("<Double-Button-1>", checar_duplo_clique)

root.mainloop()
