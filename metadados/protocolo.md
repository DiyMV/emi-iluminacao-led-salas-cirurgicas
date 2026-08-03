# Protocolo de aquisição

O que foi feito, na ordem em que foi feito, com detalhe suficiente para que
outra equipe reproduza o procedimento em outro ambiente.

## Princípio

Cada ponto de medição produz **um par** de varreduras: uma com a iluminação da
sala acionada e outra com ela apagada. O par é tomado com o mesmo arranjo, sem
tocar na antena, no cabo ou em qualquer configuração do analisador entre as duas
leituras, e separado por segundos — apenas o tempo de acionar o interruptor e
aguardar a estabilização da varredura.

A grandeza de interesse é a **diferença** entre as duas leituras. Essa escolha é
deliberada: ela cancela os erros sistemáticos comuns às duas condições — ganho
de antena, perda de cabo, resposta do pré-amplificador, desvio absoluto de
calibração — e torna o resultado robusto ao fato de o instrumento não ter
calibração vigente. Ver `../calibracao/LEIA-ME.md`.

O que a diferença **não** cancela é a não linearidade de amplitude, porque as
duas condições são lidas em níveis distintos. Esse termo residual é limitado
pela exatidão de amplitude declarada do instrumento.

## Configuração do analisador

| Parâmetro | Valor | Por quê |
|---|---|---|
| Faixa | 0–350 MHz | cobre a faixa crítica de 30–150 MHz com margem, e as harmônicas superiores dos drivers |
| Pontos | 450 | resolução nativa do instrumento |
| RBW | 850 kHz | mantido idêntico entre todas as varreduras |
| VBW | 850 kHz | idem |
| Atenuação de entrada | 0 dB | níveis medidos muito abaixo da compressão |
| Detector | traço ao vivo | sem retenção de máximo, para que cada varredura seja uma amostra independente |
| Referência de nível | fixa | nunca ajustada entre condições |

**A regra que domina todas as outras:** nenhum parâmetro muda entre as duas
condições de um mesmo par. Um ajuste de referência de nível ou de atenuação
entre a leitura acesa e a apagada invalida a subtração e produz um número sem
significado.

## Arranjo físico

- Antena telescópica, comprimento fixo, mantido em todas as posições e
  condições.
- Orientação da antena fixa em relação ao eixo da sala, não em relação à
  luminária mais próxima.
- Altura aproximada de 1,2 m, correspondente à altura de trabalho dos consoles.
- Analisador operado por bateria, desconectado do carregador durante a
  aquisição, para eliminar acoplamento pela rede.
- Cabo mantido no mesmo encaminhamento; sem reposicionamento entre condições.

## Sequência por sala

1. Sala vazia, sem procedimento em curso, sem circulação de pessoas.
2. Os equipamentos fixos da sala no mesmo estado nas duas condições —
   ligados em repouso, sem emissão de radiação ionizante.
3. Para cada uma das sete posições (`posicoes.md`):
   1. posicionar a antena;
   2. iluminação **apagada** — aguardar a estabilização da varredura, salvar;
   3. iluminação **acionada** — aguardar a estabilização, salvar;
   4. seguir para a próxima posição sem alterar configuração.
4. Registrar em caderno a correspondência entre nome de arquivo e posição, no
   momento da aquisição.

A ordem apagada-antes-de-acesa é intencional: reduz o risco de contaminar a
referência com transitório de acionamento dos drivers.

## Faixa de análise

A elevação é calculada sobre a média de amplitude na faixa de **30–150 MHz**,
não sobre o pico. A média é menos sensível a um evento de RF externo transitório
que caia em um único bin, e é a estatística que corresponde ao conceito de
elevação do ruído eletromagnético ambiente.

**A faixa varrida precisa cobrir a faixa de análise.** Isso parece óbvio e não
é: quatro varreduras deste conjunto, em `../dados_brutos/demonstracao_faixa/`,
foram tomadas em 225–575 MHz e produziriam aprovação de uma sala que a faixa
crítica reprova por margem de mais de quatro vezes. Um protocolo que não fixa a
faixa explicitamente admite esse falso negativo.

Recomendação para quem reutilizar este protocolo: **verificar a faixa de cada
arquivo antes de compará-lo**, programaticamente, e rejeitar pares cujas faixas
não coincidam. `../codigo/analise.py` levanta exceção quando a varredura não
cobre a faixa pedida, em vez de reamostrar silenciosamente.

## Critério de aceitação

Elevação média em 30–150 MHz igual ou inferior a **3 dB em todos os sete
pontos**. A reprovação de um único ponto reprova a sala.

O valor de 3 dB aplica-se a uma grandeza relativa e não é limite de emissão da
CISPR 15 — os limites dessa norma são absolutos e exigem antena calibrada e
sítio normalizado. Não é, porém, convenção arbitrária: 3,01 dB é exatamente a
elevação de uma leitura quando a contribuição acrescentada iguala o ruído de
fundo preexistente (adição de potências não correlacionadas, 10·log₁₀2). Abaixo
desse valor a elevação não é atribuível à fonte de preferência ao ambiente — é
a mesma relação que leva o método de medição invocado pela CISPR 15 a exigir
margem entre o nível medido e o ambiente, preferencialmente 20 dB e no mínimo
6 dB (CISPR 16-2-2). Com 6 dB de margem o ambiente ainda infla a leitura em
1,25 dB; na paridade, em 3,01 dB.

Dois fatos independentes corroboram o critério: equivale a cerca de três vezes e
meia a repetibilidade do arranjo (desvio-padrão de 0,89 dB entre varreduras
sucessivas) e foi validado pelo desfecho — ausência de recorrência dos sintomas
clínicos na sala adequada. Ver as limitações no `../README.md`.

## Verificação funcional

A medição espectral não substitui a confirmação clínica. O protocolo prevê,
após a adequação, teste funcional do sistema de orientação intravascular por no
mínimo 30 minutos com a iluminação acionada, confirmando imagem sem artefato e
conexão estável.
