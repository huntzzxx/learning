#! python
import math

numero_secreto = 7
numero_limite = 10

chute = int(input("Digite o seu número: "))

def insira_numero():
    chute = int(input("Digite o seu número: "))

def verifica_acerto():
    if numero_secreto == chute:
        print("Você acertou!", chute, "é o número secreto.")

while chute > numero_limite or chute < 0:
    print("Você digitou um número inválido. Insira um número entre 0 e ", numero_limite)
    insira_numero()

if chute > numero_limite:
    print("Você não pode digitar números maiores que ", numero_limite)

    
if chute < 0:
    print("Você não pode digitar números negativos.")
    

if numero_secreto == chute:
    print("Você acertou!", chute, "é o número secreto.")


while numero_secreto != chute:
    print("Você errou!", chute, "não é o número secreto.")
    insira_numero()
    if numero_secreto == chute:
        verifica_acerto()
        break