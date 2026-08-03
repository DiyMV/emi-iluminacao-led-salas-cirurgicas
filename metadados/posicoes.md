# Posições de amostragem

Sete posições por sala, idênticas nas três salas, escolhidas para cobrir a
extensão da sala e não apenas o ponto de operação.

## Convenção

Esquerda e direita referem-se ao **observador posicionado na entrada, olhando
para o interior da sala**. Essa convenção é mantida nas três salas
independentemente do lado em que a porta se encontra.

```
                    F U N D O
        +-------------------------------+
        |                               |
        |   P6                     P7   |
        |  fundo esq.          fundo dir.|
        |                               |
        |                               |
        |   P3          P4          P5  |
        | centro esq.  central   centro dir.
        |            (mesa de           |
        |             exame)            |
        |                               |
        |   P1                     P2   |
        | entrada esq.        entrada dir.
        |                               |
        +----------[  entrada  ]--------+
```

| Código | Posição | Observação |
|---|---|---|
| P1 | entrada, lado esquerdo | |
| P2 | entrada, lado direito | |
| P3 | centro, lado esquerdo | |
| P4 | central | junto à mesa de exame — ponto de operação do sistema de orientação intravascular |
| P5 | centro, lado direito | |
| P6 | fundo, lado esquerdo | |
| P7 | fundo, lado direito | |

**P4 é o ponto de referência entre campanhas.** A campanha 1 mediu apenas o
ponto central; é o único ponto que permite comparação direta antes/depois da
intervenção. As comparações por sala da campanha 2 usam a média dos sete
pontos.

## Por que sete pontos, e não um

Um único ponto não distingue emissão distribuída de emissão localizada, e essa
distinção define o escopo da correção. Os dados deste conjunto mostram os dois
padrões:

- **Sala 01** — os sete pontos variam apenas 2,15 dB (de +11,62 a +13,77 dB).
  Dispersão pequena indica emissão distribuída por todo o circuito de
  iluminação. A correção tem de abranger o conjunto; substituição pontual não
  resolveria.
- **Sala 02** — variação de 5,08 dB (de +9,24 a +14,32 dB), com o pior ponto na
  entrada direita. Padrão compatível com contribuição localizada somada à
  distribuída.

Medida apenas no ponto central, a sala 02 apresentaria +12,11 dB e a sala 01
+13,01 dB — números próximos que esconderiam a diferença de padrão espacial, e
com ela a informação que orienta o escopo do serviço.

## O que não está aqui

Não há plantas arquitetônicas, cotas, dimensões de sala ou qualquer elemento
que permita reconhecer o edifício. As posições são descritas de forma relativa e
reprodutível em qualquer sala de geometria comparável — o que basta para
reutilizar o protocolo, e não basta para identificar a instalação. Ver a seção
de anonimização no `../README.md`.
