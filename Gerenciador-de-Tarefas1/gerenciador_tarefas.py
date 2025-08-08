import tkinter as tk
from tkinter import messagebox
import json
import os

ARQUIVO = "tarefas.json"


def carregar_tarefas():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_tarefas():
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(tarefas, f, indent=4, ensure_ascii=False)

def adicionar_tarefa():
    titulo = entrada.get().strip()
    if titulo == "":
        messagebox.showwarning("Aviso", "Digite uma tarefa!")
        return
    tarefas.append({"titulo": titulo, "concluida": False})
    salvar_tarefas()
    entrada.delete(0, tk.END)
    atualizar_lista()

def alternar_conclusao():
    try:
        index = lista_tarefas.curselection()[0]
        tarefas_filtradas = filtrar_tarefas()
        tarefa_original = tarefas.index(tarefas_filtradas[index])
        tarefas[tarefa_original]["concluida"] = not tarefas[tarefa_original]["concluida"]
        salvar_tarefas()
        atualizar_lista()
    except IndexError:
        messagebox.showwarning("Aviso", "Selecione uma tarefa!")

def remover_tarefa():
    try:
        index = lista_tarefas.curselection()[0]
        tarefas_filtradas = filtrar_tarefas()
        tarefa_original = tarefas.index(tarefas_filtradas[index])
        tarefas.pop(tarefa_original)
        salvar_tarefas()
        atualizar_lista()
    except IndexError:
        messagebox.showwarning("Aviso", "Selecione uma tarefa!")

def limpar_tudo():
    if messagebox.askyesno("Confirmação", "Tem certeza que deseja apagar TODAS as tarefas?"):
        tarefas.clear()
        salvar_tarefas()
        atualizar_lista()

def filtrar_tarefas():
    termo = filtro.get().strip().lower()
    if termo == "":
        return tarefas
    return [t for t in tarefas if termo in t["titulo"].lower()]

def atualizar_lista():
    lista_tarefas.delete(0, tk.END)
    for t in filtrar_tarefas():
        status = "✔️" if t["concluida"] else "❌"
        cor = "#4CAF50" if t["concluida"] else "#F44336"
        lista_tarefas.insert(tk.END, f"{status} {t['titulo']}")
        lista_tarefas.itemconfig(tk.END, {'fg': cor})


root = tk.Tk()
root.title("Gerenciador de Tarefas PRO")
root.geometry("500x500")
root.config(bg="#222")
root.resizable(False, False)


entrada = tk.Entry(root, font=("Arial", 14))
entrada.pack(pady=10, padx=10, fill=tk.X)


frame_botoes = tk.Frame(root, bg="#222")
frame_botoes.pack(pady=5)

btn_add = tk.Button(frame_botoes, text="Adicionar", command=adicionar_tarefa, bg="#2196F3", fg="white", width=12)
btn_add.grid(row=0, column=0, padx=5)

btn_done = tk.Button(frame_botoes, text="Concluir", command=alternar_conclusao, bg="#4CAF50", fg="white", width=12)
btn_done.grid(row=0, column=1, padx=5)

btn_remove = tk.Button(frame_botoes, text="Remover", command=remover_tarefa, bg="#F44336", fg="white", width=12)
btn_remove.grid(row=0, column=2, padx=5)

filtro = tk.Entry(root, font=("Arial", 12))
filtro.pack(pady=10, padx=10, fill=tk.X)
filtro.insert(0, "Digite para filtrar...")
filtro.bind("<KeyRelease>", lambda e: atualizar_lista())


lista_tarefas = tk.Listbox(root, font=("Arial", 12), height=15)
lista_tarefas.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)


btn_clear_all = tk.Button(root, text="Limpar Tudo", command=limpar_tudo, bg="#FF9800", fg="white", width=15)
btn_clear_all.pack(pady=10)


tarefas = carregar_tarefas()
atualizar_lista()

root.mainloop()
