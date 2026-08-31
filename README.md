# Interferência eletromagnética de iluminação LED em salas cirúrgicas de alta complexidade

Varreduras espectrais brutas de um estudo de campo sobre interferência
eletromagnética (EMI) gerada por drivers de iluminação LED em três salas
cirúrgicas de alta complexidade, e o efeito dessa interferência sobre sistemas
de orientação intravascular (IVUS e FFR).

O conjunto acompanha o artigo listado em [Como citar](#como-citar) e contém
tudo o que é necessário para reproduzir, ponto a ponto, cada valor publicado.

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/DiyMV/emi-iluminacao-led-salas-cirurgicas/blob/main/codigo/validacao.ipynb)

O caderno de conferência roda direto no navegador, sem instalar nada: ele
clona este repositório e recalcula cada valor a partir dos CSV brutos.

---

## Finalidade

Este repositório constitui os **dados subjacentes** ao artigo — o material
primário sobre o qual os resultados publicados foram calculados. Destina-se à
**consulta, verificação e reprodução** desses resultados pelas instâncias
avaliadoras às quais o trabalho foi submetido:

| Instância avaliadora | Identificador da submissão |
|---|---|
| XXX Congresso Brasileiro de Engenharia Biomédica (CBEB 2026) — área temática E, Engenharia Clínica e Hospitalar | submissão nº 717 |
| Instância institucional do serviço de origem | submissão interna, sem identificador atribuído |

O depósito é permanente e de acesso aberto. Os dados são publicados **sem
tratamento** — sem fator de antena, perda de cabo ou correção de calibração —
precisamente para que qualquer avaliador possa refazer o cálculo a partir da
leitura bruta do instrumento, e para que o conjunto admita reprocessamento
futuro quando houver certificado de calibração (ver
[Instrumentação e situação de calibração](#instrumentação-e-situação-de-calibração)).

---

## Sumário

- [Finalidade](#finalidade)
- [O que há aqui](#o-que-há-aqui)
- [Reprodução em um comando](#reprodução-em-um-comando)
- [Resultados](#resultados)
- [Organização dos arquivos](#organização-dos-arquivos)
- [Formato dos dados](#formato-dos-dados)
- [Instrumentação e situação de calibração](#instrumentação-e-situação-de-calibração)
- [Limitações — leia antes de reutilizar](#limitações--leia-antes-de-reutilizar)
- [Como citar](#como-citar)
- [Licença](#licença)

---

## O que há aqui

52 varreduras espectrais, organizadas em duas campanhas e um conjunto auxiliar.

| Conjunto | Arquivos | O que é |
|---|---:|---|
| Campanha 1 — diagnóstico | 6 | Sala 03 com a falha clinicamente ativa: cinco varreduras sucessivas com a iluminação acionada e uma referência com ela apagada |
| Campanha 2 — verificação | 42 | Três salas × sete posições × duas condições, medidas no mesmo dia com o mesmo arranjo |
| Demonstração de faixa | 4 | Varreduras de 225–575 MHz das salas 01 e 03, que documentam um falso negativo por escolha inadequada de faixa |

Entre as duas campanhas, apenas a **sala 03** recebeu intervenção: substituição
do conjunto de drivers de iluminação por modelos com filtro EMI integrado e
carcaça metálica aterrada. As salas 01 e 02 permaneceram intactas e funcionam,
na campanha 2, como **controles simultâneos** — medidos no mesmo dia, com o
mesmo instrumento e o mesmo operador. É essa simultaneidade, e não a comparação
temporal isolada, que sustenta a atribuição causal.

## Reprodução em um comando

```bash
pip install numpy
python codigo/analise.py
```

Sem argumentos, imprime todas as tabelas. Com `--csv <pasta>`, grava a tabela
ponto a ponto em CSV.

Para conferir **valor por valor** contra o que o artigo publicou, há um caderno
com implementação independente da de `analise.py` — duas implementações que
chegam ao mesmo número valem mais do que uma executada duas vezes:

```bash
pip install numpy matplotlib
jupyter lab codigo/validacao.ipynb
```

Ele recalcula 22 afirmações publicadas, imprime calculado × publicado × erro
para cada uma, e sinaliza qualquer divergência.

A grandeza analisada é a elevação do ruído eletromagnético ambiente produzida
pela iluminação:

```
Δ = média( A_luz_on(f) ) − média( A_luz_off(f) ),    f ∈ faixa de análise
```

As duas leituras são tomadas no mesmo ponto, com o mesmo arranjo, separadas por
segundos. A subtração cancela os erros sistemáticos comuns às duas condições —
ganho de antena, perda de cabo, desvio absoluto de calibração. **O resultado é
uma razão, em dB, e não um nível absoluto em dBm.**

## Resultados

Faixa de análise 30–150 MHz. Critério de aceitação adotado: 3 dB — o limiar em
que a contribuição da iluminação iguala o ruído de fundo preexistente (ver
[Limitações](#limitações--leia-antes-de-reutilizar)).

| Sala | Intervenção | Média | Mín. | Máx. | Desvio-padrão | Veredito |
|---|---|---:|---:|---:|---:|---|
| 01 | nenhuma | +12,68 dB | +11,62 | +13,77 | 0,70 | reprovado |
| 02 | nenhuma | +12,40 dB | +9,24 | +14,32 | 1,74 | reprovado |
| 03 | drivers substituídos | +1,04 dB | +0,34 | +1,73 | 0,52 | aprovado |

Campanha 1, sala 03 antes da intervenção: **+13,23 dB** (média de cinco
varreduras, desvio-padrão 0,89 dB). Depois: +1,04 dB.

O desvio-padrão de 0,89 dB entre varreduras sucessivas caracteriza a
repetibilidade de curto prazo do arranjo. É essa — e não o intervalo de
calibração — a grandeza de estabilidade relevante para uma diferença tomada no
intervalo de segundos. O efeito medido é cerca de quinze vezes maior.

A dispersão espacial distingue os dois casos reprovados. Na sala 01 os sete
pontos variam apenas 2,15 dB, o que indica emissão distribuída por todo o
circuito. Na sala 02 a variação chega a 5,08 dB, com o pior ponto na entrada
direita — padrão compatível com contribuição localizada somada à distribuída.

### O efeito da faixa varrida

| Sala | 225–575 MHz | 30–150 MHz | Subestimação |
|---|---:|---:|---:|
| 01 | +2,94 dB | +13,01 dB | 10,08 dB |
| 03 | +0,07 dB | +0,47 dB | 0,40 dB |

Uma varredura em 225–575 MHz aprovaria a sala 01 — que a faixa crítica reprova
por margem de mais de quatro vezes. Os quatro arquivos em
`dados_brutos/demonstracao_faixa/` documentam esse falso negativo com dados
reais, medidos na mesma sala e no mesmo dia que os da campanha 2.

**A escolha da faixa é parte do critério de aceitação, não um detalhe de
configuração.** Um protocolo que não a fixa explicitamente pode produzir
aprovação de ambientes reprovados.

### A fronteira de 80 MHz

O ensaio de imunidade a RF **radiada** da IEC 60601-1-2, para o ambiente de
estabelecimento de assistência à saúde, começa em **80 MHz** (3 V/m até
2,7 GHz). Abaixo dessa fronteira, a qualificação do equipamento se dá por
imunidade **conduzida** — de 150 kHz a 80 MHz, com o cabeamento como caminho de
acoplamento, e não o campo incidente.

A faixa em que a interferência se concentrou atravessa essa fronteira:

| Sub-faixa | Pontos espectrais | Elevação média | Como a norma qualifica |
|---|---:|---:|---|
| 30–80 MHz | 64 (42%) | +13,65 dB | imunidade conduzida, via cabos |
| 80–150 MHz | 90 (58%) | +12,93 dB | imunidade radiada, 3 V/m |

Cinco dos dez pontos de maior elevação — 77,17 · 77,95 · 78,73 · 74,83 ·
74,05 MHz — caem abaixo de 80 MHz, e o primeiro deles iguala o máximo global de
+25,30 dB, observado em 88,86 MHz. Os números são reproduzíveis a partir de
`dados_brutos/campanha_1_diagnostico/`.

**Isto não é constatação de violação.** As amplitudes aqui são relativas e não
admitem confronto com os 3 V/m, pelas razões da seção
[Limitações](#limitações--leia-antes-de-reutilizar). A observação é outra: cerca
de metade da energia do fenômeno está em uma região onde a imunidade do
equipamento não é caracterizada por ensaio radiado. Para um sistema cuja cadeia
de recepção é um cateter e seu cabeamento, a distinção importa.

Vale ainda o que a norma colateral não faz: ela qualifica o **equipamento**
presumindo um ambiente eletromagnético, e atribui à organização responsável
mantê-lo compatível com o declarado pelo fabricante. Não há, em norma alguma,
limite para o ruído eletromagnético ambiente. É por isso que o critério de 3 dB é
critério de aceitação de instalação, e não transcrição de requisito normativo.

## Organização dos arquivos

```
dados_brutos/
  campanha_1_diagnostico/    C1_sala03_luz_{on_rep1..5,off_ref}.csv
  campanha_2_verificacao/    C2_sala{01,02,03}_P{1..7}_luz_{on,off}.csv
  demonstracao_faixa/        DF_sala{01,03}_luz_{on,off}_225-575MHz.csv
metadados/
  inventario.json            um registro por arquivo, legível por máquina
  cronologia.md              quando cada varredura foi adquirida
  posicoes.md                as sete posições de amostragem
  protocolo.md               procedimento de aquisição
codigo/
  analise.py                 reproduz todos os valores publicados
  validacao.ipynb            confere valor por valor contra o artigo
  requisitos.txt
calibracao/
  LEIA-ME.md                 situação de calibração e o que será acrescentado
```

As sete posições, idênticas nas três salas:

| Código | Posição |
|---|---|
| P1 | entrada, lado esquerdo |
| P2 | entrada, lado direito |
| P3 | centro, lado esquerdo |
| P4 | central — junto à mesa de exame |
| P5 | centro, lado direito |
| P6 | fundo, lado esquerdo |
| P7 | fundo, lado direito |

Esquerda e direita referem-se ao observador posicionado na entrada, olhando
para o interior da sala. Detalhes em `metadados/posicoes.md`.

## Formato dos dados

CSV com cabeçalho, duas colunas, ponto como separador decimal:

```
frequencia_hz,amplitude_dbm
0,-13.5
779510,-89.2
```

450 pontos por varredura, passo de 779.510 Hz — as duas faixas empregadas têm a
mesma extensão de 350 MHz. Amplitude em dBm na entrada do analisador,
**sem qualquer correção aplicada** — nem fator de antena, nem perda de cabo,
nem correção de calibração. Os dados são publicados exatamente como saíram do
instrumento, justamente para que o reprocessamento seja possível por terceiros.

O arquivo em si não carrega data: o analisador não grava carimbo de tempo. A
data de aquisição está no campo `data_aquisicao` do `inventario.json`, com
resolução de **dia** e procedência verificável — ver
[`metadados/cronologia.md`](metadados/cronologia.md).

## Instrumentação e situação de calibração

| Item | Valor |
|---|---|
| Analisador | tinySA Ultra, firmware 1.4-104 |
| Faixa varrida | 0–350 MHz (conjunto principal); 225–575 MHz (demonstração de faixa) |
| Pontos por varredura | 450 |
| RBW / VBW | 850 kHz |
| Atenuação de entrada | 0 dB |
| Detector | traço ao vivo, sem retenção de máximo |
| Antena | telescópica, altura e orientação fixas entre condições |

> **O instrumento não dispunha de calibração vigente rastreável durante as
> campanhas.** Não houve janela de calibração disponível antes das medições.
> Esta condição é declarada aqui, no artigo e em `calibracao/LEIA-ME.md`,
> porque condiciona a leitura de todos os resultados.

O que a ausência de calibração afeta, e o que não afeta:

- **Não afeta** a comparação relativa entre as duas condições no mesmo ponto: os
  erros sistemáticos comuns às duas leituras cancelam-se na subtração.
- **Afeta** qualquer afirmação de nível absoluto. Nenhum valor deste conjunto
  pode ser confrontado com limites normativos, que são expressos em dBµV/m com
  antena calibrada e distância normalizada.
- **Sobrevive parcialmente à subtração** a não linearidade de amplitude do
  instrumento, porque as duas condições são lidas em níveis distintos. A
  exatidão de amplitude declarada pelo fabricante para a faixa empregada é de
  ±1 dB, o que limita esse termo residual a cerca de 2 dB no pior caso.

Para comparação: a CISPR 16-4-2 atribui a uma medição radiada **acreditada**
incerteza de instrumentação de 4,95 dB a 3 m. A elevação observada, de 12 a
13 dB, excede em cerca de duas vezes e meia a incerteza que a própria norma
admite para o ensaio de referência.

Assim que o instrumento for calibrado, a tabela de correção será acrescentada em
`calibracao/`, permitindo reprocessar estas varreduras e avaliar de forma
independente a repetibilidade e a rastreabilidade dos resultados. Ver
`calibracao/LEIA-ME.md`.

## Limitações — leia antes de reutilizar

1. **Estes dados não são medida de conformidade.** São diferenças relativas
   obtidas com instrumento sem calibração vigente, sem detector de quase-pico e
   sem as larguras de banda normativas exigidas pela CISPR 16-1-1. Analisadores
   sem pré-seleção não são admitidos em medição de conformidade.
2. **O critério de 3 dB é operacional, mas não arbitrário.** Ele não é limite
   de emissão da CISPR 15: os limites dessa norma são absolutos, em dBµV/m ou
   dBµV, com antena calibrada e sítio normalizado, e não se aplicam a uma
   grandeza relativa. O valor decorre da adição de potências não correlacionadas
   que o método de medição invocado pela norma usa para separar perturbação de
   ambiente — uma contribuição exatamente igual ao ruído de fundo preexistente
   eleva a leitura combinada em 3,01 dB (10·log₁₀2). Abaixo disso, a elevação
   não pode ser atribuída à fonte de preferência ao próprio ambiente. É a mesma
   relação que sustenta a exigência de margem entre o nível medido e o ambiente
   — preferencialmente 20 dB, no mínimo 6 dB (CISPR 16-2-2, base metrológica
   invocada pela CISPR 15). Duas evidências independentes corroboram o valor:
   equivale a cerca de três vezes e meia a repetibilidade do arranjo (0,89 dB) e
   foi validado pelo desfecho clínico — ausência de recorrência dos sintomas
   após a intervenção. O que ele **não** é: relação dose–resposta estabelecida
   entre elevação do ruído eletromagnético ambiente e degradação mensurável do
   sinal clínico. Estabelecer essa relação é trabalho futuro.
3. **A campanha 1 não incluiu amostragem espacial.** Não é possível reconstruir
   a distribuição da emissão anterior à intervenção; apenas sua magnitude no
   ponto central.
4. **A amostra é de três salas de um único serviço.** Não sustenta
   generalização quantitativa para outros ambientes.
5. **Reprodução não é validação.** `analise.py` e `codigo/validacao.ipynb` são
   implementações independentes entre si, e o acordo entre as duas exclui erro
   de codificação — não exclui erro de medição, de arranjo ou de premissa. A
   verificação por terceiros é justamente o motivo de os dados brutos estarem
   aqui.

## Como citar

Se estes dados forem úteis ao seu trabalho, cite o artigo:

> A. A. dos Santos, W. Knob de Souza, G. Fallavena Chaves e R. Lopes Rezer, "Mitigando e
> Caracterizando Relativamente EMI Irradiadas em Salas Cirúrgicas de Alta
> Complexidade," in *Anais do XXX Congresso Brasileiro de Engenharia Biomédica
> (CBEB 2026)*, 2026.

Um arquivo `CITATION.cff` acompanha o repositório para citação automática.

## Licença

Dados e documentação sob [CC BY 4.0](LICENSE). O código em `codigo/` sob
[MIT](LICENSE-CODE). Uso livre, inclusive comercial, com atribuição.

## Contribuições

Reprocessamento independente, correções e comparações com outros ambientes são
bem-vindos — abra uma *issue*. Discordâncias metodológicas fundamentadas são
particularmente úteis: o critério de 3 dB e a escolha da faixa de análise são as
duas decisões deste trabalho que mais merecem escrutínio.
