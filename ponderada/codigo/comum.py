"""
comum.py - Parâmetros e relatório compartilhados pelas três versões da questão A4.

Ponderada CC08 (Tato) - Teodoro Borges de Carvalho Neira.
Buffer circular entre a thread do sensor (produtora) e a do motor (consumidora).
Parâmetros individuais: D1 = 7, D2 = 8, N = 3 + (8 mod 5) = 6.
"""

N = 6                # posições do buffer circular
TOTAL = 20_000       # amostras geradas pelo produtor (0, 1, ..., TOTAL - 1)
TIMEOUT = 1.0        # segundos sem receber nada => travamento


def relatorio(versao, recebidas, travou, segundos):
    """Analisa as amostras recebidas pelo consumidor e imprime o resultado.

    Parâmetros:
        versao (str): nome da versão, usado no cabeçalho da saída.
        recebidas (list[int]): números das amostras na ordem em que o
            consumidor as recebeu (pode ter repetições ou buracos).
        travou (bool): True se o consumidor ficou TIMEOUT segundos sem receber.
        segundos (float): duração da execução.

    Retorno:
        dict com as chaves consumidas, perdidas, duplicadas e travou.

    Funcionamento:
        consumidas = total de itens retirados do buffer (com repetições);
        perdidas   = amostras de 0..TOTAL-1 que nunca chegaram ao consumidor;
        duplicadas = recebimentos extras de uma amostra que já tinha chegado.
    """
    vistas = set(recebidas)
    resultado = {
        "consumidas": len(recebidas),
        "perdidas": sum(1 for i in range(TOTAL) if i not in vistas),
        "duplicadas": len(recebidas) - len(vistas),
        "travou": travou,
    }
    print(f"=== {versao} | N = {N} | {TOTAL} amostras ===")
    print(f"consumidas: {resultado['consumidas']}")
    print(f"perdidas:   {resultado['perdidas']}")
    print(f"duplicadas: {resultado['duplicadas']}")
    print(f"travou:     {'SIM' if travou else 'não'}")
    print(f"tempo:      {segundos:.2f} s")
    return resultado
