"""
versao3.py - A4, versão 3: semáforos com a ordem do produtor TROCADA.

Igual à versão 2, mas o produtor faz wait(mutex) ANTES de wait(vazio).
Quando o buffer enche, o produtor dorme em vazio segurando o mutex, e o
consumidor, que precisa do mutex para liberar uma posição, fica bloqueado:
deadlock. O consumidor detecta o travamento pelo timeout de 1 s.

Uso: python3 ponderada/codigo/versao3.py
"""

import threading
import time

from comum import N, TOTAL, TIMEOUT, relatorio

buffer = [None] * N
vazio = threading.Semaphore(N)
cheio = threading.Semaphore(0)
mutex = threading.Semaphore(1)


def produtor():
    """Gera as amostras 0..TOTAL-1 e as coloca no buffer.

    Parâmetros: nenhum. Retorno: None.
    Funcionamento: wait(mutex) -> wait(vazio) (ordem errada) -> grava
    -> signal(mutex) -> signal(cheio). Com o buffer cheio, bloqueia em
    vazio segurando o mutex.
    """
    entrada = 0
    for amostra in range(TOTAL):
        mutex.acquire()               # wait(mutex) primeiro (ERRADO)
        vazio.acquire()               # wait(vazio) com o mutex na mão
        buffer[entrada] = amostra
        time.sleep(0)
        entrada = (entrada + 1) % N
        mutex.release()
        cheio.release()


def consumidor(recebidas):
    """Retira amostras do buffer até receber a última ou travar.

    Parâmetros:
        recebidas (list[int]): lista onde cada amostra retirada é anotada.
    Retorno:
        bool: True se algum wait esperou mais que TIMEOUT (travamento).
    Funcionamento: idêntico ao consumidor da versão 2.
    """
    saida = 0
    while True:
        if not cheio.acquire(timeout=TIMEOUT):
            return True
        if not mutex.acquire(timeout=TIMEOUT):
            return True
        amostra = buffer[saida]
        time.sleep(0)
        saida = (saida + 1) % N
        mutex.release()
        vazio.release()
        recebidas.append(amostra)
        if amostra == TOTAL - 1:
            return False


def main():
    """Roda produtor e consumidor em threads e imprime o relatório.

    Parâmetros: nenhum. Retorno: None.
    """
    recebidas = []
    inicio = time.monotonic()
    threading.Thread(target=produtor, daemon=True).start()
    travou = consumidor(recebidas)
    relatorio("Versão 3 (ordem trocada no produtor)", recebidas, travou,
              time.monotonic() - inicio)


if __name__ == "__main__":
    main()
