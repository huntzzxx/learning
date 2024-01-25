#! python


def fibonacci(quantidade):
    resutado = [0, 1]
    for _ in range(2, quantidade):
        resutado.append(sum(resutado[-2:]) )
    return resutado


if __name__ == '__main__':
    for fib in fibonacci(20):
        print(fib)
