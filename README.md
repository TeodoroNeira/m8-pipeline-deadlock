# m8-pipeline-deadlock

Autor: Teodoro Borges de Carvalho Neira

Ponderada de Computação CC08 (Módulo 8, Ciência da Computação): arquitetura, pipeline, threads, semáforos e deadlock aplicados à pulseira sensorial Tato.

## Estrutura

- [`ponderada/ponderada-tato.md`](ponderada/ponderada-tato.md): Parte A (problema técnico) e Parte B (memorando do CTO)
- `ponderada/codigo/`: código da questão A4
- `ponderada/img/`: prints

## Como rodar a questão A4

Requisito: Python 3 (só biblioteca padrão). Na raiz do repositório:

```bash
python3 ponderada/codigo/versao1.py   # versão 1: sem sincronização (espera ocupada)
python3 ponderada/codigo/versao2.py   # versão 2: semáforos vazio, cheio e mutex
python3 ponderada/codigo/versao3.py   # versão 3: produtor com wait(mutex) antes de wait(vazio)
```

Cada execução produz 20.000 amostras com buffer de N = 6 posições. Ela imprime as amostras consumidas, perdidas e duplicadas e diz se travou (1 s sem o consumidor receber nada).
