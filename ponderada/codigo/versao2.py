"""
versao2.py - A4, versão 2: buffer circular COM semáforos.

Três semáforos: vazio (começa em N) conta posições livres, cheio (começa
em 0) conta posições ocupadas e mutex (começa em 1) garante exclusão mútua
no acesso ao buffer. O time.sleep(0) dentro da região crítica continua lá
para mostrar que, protegida, a interrupção não causa mais erro.

Uso: python3 ponderada/codigo/versao2.py
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
    Funcionamento: wait(vazio) -> wait(mutex) -> grava -> signal(mutex)
    -> signal(cheio). Se o consumidor travar, a thread (daemon) morre
    junto com o programa.
    """
    entrada = 0
    for amostra in range(TOTAL):
        vazio.acquire()               # wait(vazio): espera posição livre
        mutex.acquire()               # wait(mutex): entra na região crítica
        buffer[entrada] = amostra
        time.sleep(0)
        entrada = (entrada + 1) % N
        mutex.release()               # signal(mutex)
        cheio.release()               # signal(cheio): mais uma ocupada


def consumidor(recebidas):
    """Retira amostras do buffer até receber a última ou travar.

    Parâmetros:
        recebidas (list[int]): lista onde cada amostra retirada é anotada.
    Retorno:
        bool: True se algum wait esperou mais que TIMEOUT (travamento).
    Funcionamento: wait(cheio) -> wait(mutex) -> lê -> signal(mutex)
    -> signal(vazio).
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
    relatorio("Versão 2 (semáforos)", recebidas, travou,
              time.monotonic() - inicio)


if __name__ == "__main__":
    main()
