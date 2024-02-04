# lista de tarefas
import json
import os 
import time


def limpar_tela():
    sistema = os.name
    if sistema == "nt":
        os.system("cls")
    else:
        os.system("clear")

def salvar_tarefas(lista_tarefas):
    with open("tarefas.json", "w") as arquivo:
        json.dump(lista_tarefas, arquivo)
        
def carregar_tarefas():
    try:
        with open("tarefas.json", "r") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []

def adicionar_tarefa(tarefa, lista_tarefas):
    lista_tarefas.append(tarefa)
    
def remover_tarefa(numero, lista_tarefas):
    try:
        numero = int(numero)
        if 1 <= numero <= len(lista_tarefas):
            tarefa_removida = lista_tarefas.pop(numero - 1)
            print(f"Tarefa '{tarefa_removida}' removida com sucesso!")
        else:
            print("Número de tarefa inválido.")
    except (ValueError, IndexError):
        print("Número de tarefa inválido.")
    
def listar_tarefas(lista_tarefas):
    for tarefa in lista_tarefas:
        print(tarefa)
        
tarefas = carregar_tarefas()
limpar_tela()
print("Bem vindo ao sistema de tarefas")
continuar = True
while continuar:
    print("Escolha no menu a baixo a opção desejada para gerenciar suas tarefas:")
    print("""          1 - Adicionar tarefa
          2 - Remover tarefa
          3 - Listar tarefas
          4 - Sair""")
    try:
        opcao = int(input("Digite a opção desejada: "))
        if opcao == 1:
            tarefa = input("Digite a tarefa a ser adicionada: ")
            adicionar_tarefa(tarefa, tarefas)
            salvar_tarefas(tarefas)
            print("Tarefa adicionada com sucesso!")
            time.sleep(2)
            limpar_tela()
        elif opcao == 2:
            limpar_tela()
            print("Lista de Tarefas:")
            for i, tarefa in enumerate(tarefas, start=1):
                print(f"{i}. {tarefa}")
            
            numero_tarefa = input("Digite o número da tarefa a ser removida: ")
            remover_tarefa(numero_tarefa, tarefas)
            salvar_tarefas(tarefas)
            time.sleep(2)
            limpar_tela()
        elif opcao == 3:
            limpar_tela()
            print("Lista de Tarefas:")
            for i, tarefa in enumerate(tarefas, start=1):
                print(f"{i}. {tarefa}")
            input("Pressione enter para continuar...")
            limpar_tela()
        elif opcao == 4:
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida")
            time.sleep(2)
            limpar_tela()
    except ValueError:
        print("Opção inválida")
        time.sleep(2)
        limpar_tela()
        
        
