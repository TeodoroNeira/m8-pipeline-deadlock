"""
versao1.py - A4, versão 1: buffer circular SEM sincronização.

Produtor (sensor) e consumidor (motor) dividem um contador de posições
ocupadas e esperam em laço (espera ocupada). Um time.sleep(0) entre ler e
escrever o contador simula a thread sendo interrompida no pior momento,
o que faz a condição de corrida aparecer.

Uso: python3 ponderada/codigo/versao1.py
"""

import threading
import time

from comum import N, TOTAL, TIMEOUT, relatorio

buffer = [None] * N
contador = 0          # posições ocupadas (compartilhado, sem proteção)
parar = False         # avisa o produtor para desistir quando o consumidor encerra


def produtor():
    """Gera as amostras 0..TOTAL-1 e as coloca no buffer.

    Parâmetros: nenhum (usa as variáveis globais buffer, contador e parar).
    Retorno: None.
    Funcionamento: espera ocupada enquanto o contador indica buffer cheio,
    grava na posição de entrada e incrementa o contador em dois passos
    (ler, ceder a CPU, escrever) - essa é a região crítica desprotegida.
    """
    global contador
    entrada = 0
    for amostra in range(TOTAL):
        while contador >= N:          # espera ocupada: buffer cheio
            if parar:
                return
            time.sleep(0)             # cede a CPU, mas continua girando
        buffer[entrada] = amostra
        entrada = (entrada + 1) % N
        lido = contador               # lê o contador
        time.sleep(0)                 # interrupção no pior momento
        contador = lido + 1           # escreve o contador


def consumidor(recebidas):
    """Retira amostras do buffer até receber a última ou travar.

    Parâmetros:
        recebidas (list[int]): lista onde cada amostra retirada é anotada.
    Retorno:
        bool: True se ficou TIMEOUT segundos sem receber nada (travamento).
    Funcionamento: espera ocupada enquanto o contador indica buffer vazio,
    lê a posição de saída e decrementa o contador em dois passos, com a
    mesma janela de corrida do produtor.
    """
    global contador
    saida = 0
    while True:
        inicio = time.monotonic()
        while contador <= 0:          # espera ocupada: buffer vazio
            if time.monotonic() - inicio > TIMEOUT:
                return True
            time.sleep(0)
        amostra = buffer[saida]
        saida = (saida + 1) % N
        lido = contador
        time.sleep(0)
        contador = lido - 1
        recebidas.append(amostra)
        if amostra == TOTAL - 1:
            return False


def main():
    """Roda produtor e consumidor em threads e imprime o relatório.

    Parâmetros: nenhum. Retorno: None.
    """
    global parar
    recebidas = []
    inicio = time.monotonic()
    t_prod = threading.Thread(target=produtor, daemon=True)
    t_prod.start()
    travou = consumidor(recebidas)    # o consumidor roda na thread principal
    parar = True
    t_prod.join(timeout=TIMEOUT)
    relatorio("Versão 1 (sem sincronização)", recebidas, travou,
              time.monotonic() - inicio)


if __name__ == "__main__":
    main()
