#! python

import math
import sys
import errno

class TerminalColor:
    erro = '\033[91m'
    normal = '\033[0m'


def help():
    print("É necessário informar o raio de um círculo.")
    print("Sintaxe: {} <raio>".format(sys.argv[0][2:]))


def circulo(raio):
    return math.pi * (float(raio) ** 2)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        help()
        sys.exit(errno.EPERM)
    elif not sys.argv[1].isnumeric():
        help()
        print(TerminalColor.erro + 'O raio deve ser um valor númerico.', TerminalColor.normal)
        sys.exit(errno.EINVAL)
    else:
        raio = sys.argv[1]
        try:
            area = circulo(raio)
            print('Área do círculo:', area)
        except ValueError:
            print("Erro: Certifique-se de que o raio fornecido é um número válido.")
            sys.exit(1)