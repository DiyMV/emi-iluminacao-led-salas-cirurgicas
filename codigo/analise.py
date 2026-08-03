# -*- coding: utf-8 -*-
"""Reproduz, a partir das varreduras brutas, todos os valores publicados.

Uso:
    python codigo/analise.py                # tabelas no terminal
    python codigo/analise.py --csv saida/   # grava as tabelas em CSV

Dependencia: numpy.

A grandeza analisada e a elevacao do piso de ruido produzida pela iluminacao:

    Delta = media( A_luz_on(f) )  -  media( A_luz_off(f) ),   f na faixa de analise

com as duas leituras tomadas no mesmo ponto, com o mesmo arranjo e separadas por
segundos. A subtracao cancela os erros sistematicos comuns as duas condicoes
(ganho de antena, perda de cabo, desvio absoluto de calibracao); o resultado e
uma razao em dB, e nao um nivel absoluto em dBm.
"""
import argparse
import io
import os
import sys

try:
    import numpy as np
except ImportError:
    sys.exit("necessario: pip install numpy")

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FAIXA_CRITICA = (30e6, 150e6)    # faixa que afeta IVUS e FFR Link
FAIXA_ALTA = (225e6, 350e6)      # faixa da varredura que produziu falso negativo
CRITERIO = 3.0                   # dB
POSICOES = ["P1", "P2", "P3", "P4", "P5", "P6", "P7"]
NOME_POS = {"P1": "entrada esq.", "P2": "entrada dir.", "P3": "centro esq.",
            "P4": "central", "P5": "centro dir.", "P6": "fundo esq.",
            "P7": "fundo dir."}


def ler(caminho):
    """Le um CSV do repositorio. Retorna (frequencia_hz, amplitude_dbm)."""
    linhas = io.open(caminho, encoding="utf-8").read().splitlines()
    if linhas and not linhas[0][:1].isdigit():
        linhas = linhas[1:]
    dados = np.array([[float(x) for x in l.split(",")] for l in linhas if l.strip()])
    return dados[:, 0], dados[:, 1]


def media_faixa(freq, amp, faixa):
    sel = (freq >= faixa[0]) & (freq <= faixa[1])
    if not sel.any():
        raise ValueError("a varredura nao cobre a faixa pedida")
    return amp[sel].mean()


def elevacao(arq_on, arq_off, faixa=FAIXA_CRITICA):
    f1, a1 = ler(arq_on)
    f0, a0 = ler(arq_off)
    return media_faixa(f1, a1, faixa) - media_faixa(f0, a0, faixa)


# --------------------------------------------------------------- campanha 2
def campanha2(faixa=FAIXA_CRITICA):
    base = os.path.join(RAIZ, "dados_brutos", "campanha_2_verificacao")
    saida = {}
    for sala in ("01", "02", "03"):
        por_ponto = []
        for pos in POSICOES:
            on = os.path.join(base, "C2_sala%s_%s_luz_on.csv" % (sala, pos))
            off = os.path.join(base, "C2_sala%s_%s_luz_off.csv" % (sala, pos))
            por_ponto.append(elevacao(on, off, faixa))
        saida[sala] = np.array(por_ponto)
    return saida


# --------------------------------------------------------------- campanha 1
def campanha1(faixa=FAIXA_CRITICA):
    """Cinco varreduras com a luz acionada contra a referencia com a luz apagada."""
    base = os.path.join(RAIZ, "dados_brutos", "campanha_1_diagnostico")
    f0, a0 = ler(os.path.join(base, "C1_sala03_luz_off_ref.csv"))
    ref = media_faixa(f0, a0, faixa)
    vals = []
    for i in range(1, 6):
        f1, a1 = ler(os.path.join(base, "C1_sala03_luz_on_rep%d.csv" % i))
        vals.append(media_faixa(f1, a1, faixa) - ref)
    return np.array(vals)


def repetibilidade():
    """Desvio-padrao entre as cinco varreduras sucessivas da mesma condicao.

    E esta -- e nao o intervalo de calibracao -- a grandeza de estabilidade
    relevante para uma diferenca tomada no intervalo de segundos.
    """
    base = os.path.join(RAIZ, "dados_brutos", "campanha_1_diagnostico")
    m = []
    for i in range(1, 6):
        f, a = ler(os.path.join(base, "C1_sala03_luz_on_rep%d.csv" % i))
        m.append(media_faixa(f, a, FAIXA_CRITICA))
    return float(np.std(m, ddof=1))


# ---------------------------------------------------------- demonstracao faixa
def demonstracao_faixa():
    """Mesma sala, mesmo dia: o resultado depende da faixa varrida.

    As varreduras de 225-575 MHz nao cobrem a faixa critica. Confrontadas com
    as de 0-350 MHz, mostram que uma escolha de faixa mal fundamentada produz
    aprovacao aparente de uma sala reprovada.
    """
    df = os.path.join(RAIZ, "dados_brutos", "demonstracao_faixa")
    c2 = os.path.join(RAIZ, "dados_brutos", "campanha_2_verificacao")
    linhas = []
    for sala in ("01", "03"):
        alta = elevacao(os.path.join(df, "DF_sala%s_luz_on_225-575MHz.csv" % sala),
                        os.path.join(df, "DF_sala%s_luz_off_225-575MHz.csv" % sala),
                        (225e6, 575e6))
        crit = elevacao(os.path.join(c2, "C2_sala%s_P4_luz_on.csv" % sala),
                        os.path.join(c2, "C2_sala%s_P4_luz_off.csv" % sala),
                        FAIXA_CRITICA)
        linhas.append((sala, alta, crit))
    return linhas


def veredito(v):
    return "aprovado" if v <= CRITERIO else "REPROVADO"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--csv", metavar="PASTA", help="grava as tabelas em CSV")
    a = p.parse_args()

    print("=" * 68)
    print("Elevacao do piso de ruido por iluminacao LED -- faixa 30-150 MHz")
    print("criterio de aceitacao: %.1f dB" % CRITERIO)
    print("=" * 68)

    c2 = campanha2()
    print("\nCampanha 2 -- verificacao, 7 pontos por sala\n")
    print("  sala  ponto  local           Delta (dB)  veredito")
    print("  " + "-" * 54)
    linhas_csv = [["campanha", "sala", "posicao", "local", "delta_db", "veredito"]]
    for sala in ("01", "02", "03"):
        for pos, v in zip(POSICOES, c2[sala]):
            print("  %-5s %-6s %-15s %+7.2f    %s"
                  % (sala, pos, NOME_POS[pos], v, veredito(v)))
            linhas_csv.append([2, sala, pos, NOME_POS[pos], "%.2f" % v, veredito(v)])
        print("  " + "-" * 54)

    print("\n  resumo por sala")
    print("  sala   media    min      max     dp    veredito")
    for sala in ("01", "02", "03"):
        v = c2[sala]
        print("  %-5s %+7.2f %+7.2f %+7.2f %6.2f   %s"
              % (sala, v.mean(), v.min(), v.max(), v.std(ddof=1),
                 veredito(v.mean())))

    c1 = campanha1()
    print("\nCampanha 1 -- diagnostico, sala 03 com a falha clinicamente ativa\n")
    print("  cinco varreduras: " + "  ".join("%+.2f" % x for x in c1))
    print("  media %+.2f dB   dp %.2f dB" % (c1.mean(), c1.std(ddof=1)))
    print("\n  repetibilidade de curto prazo do arranjo: %.2f dB" % repetibilidade())

    print("\nEfeito da faixa de analise\n")
    print("  sala   225-575 MHz    30-150 MHz    subestimacao")
    for sala, alta, crit in demonstracao_faixa():
        print("  %-5s %+9.2f dB %+11.2f dB %11.2f dB"
              % (sala, alta, crit, crit - alta))
    print("\n  Uma varredura em 225-575 MHz aprovaria salas que a faixa critica")
    print("  reprova. A escolha de faixa e, portanto, parte do criterio.")

    if a.csv:
        os.makedirs(a.csv, exist_ok=True)
        destino = os.path.join(a.csv, "elevacao_por_ponto.csv")
        io.open(destino, "w", encoding="utf-8", newline="\n").write(
            "\n".join(",".join(str(c) for c in l) for l in linhas_csv) + "\n")
        print("\ngravado: %s" % destino)


if __name__ == "__main__":
    main()
