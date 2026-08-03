# Situação de calibração

## O fato

**O analisador não dispunha de calibração vigente rastreável durante as duas
campanhas de medição.** Não houve janela de calibração disponível antes das
medições — restrição operacional de um serviço hospitalar em funcionamento, não
uma escolha metodológica.

Esta pasta está vazia de dados por esse motivo. Ela existe para declarar a
lacuna, delimitar o que ela afeta, e receber a correção quando ela existir.

## O que a lacuna afeta

**Não afeta** a comparação relativa entre as duas condições no mesmo ponto.
Sendo Δ uma diferença entre duas leituras tomadas com o mesmo arranjo, separadas
por segundos e sem deslocamento da antena:

```
Δ_medido = (A_on + e_sist) − (A_off + e_sist) = Δ_real
```

onde `e_sist` agrega ganho de antena, perda de cabo, resposta do
pré-amplificador e desvio absoluto de calibração. O termo cancela.

**Afeta integralmente** qualquer afirmação de nível absoluto. Nenhum valor deste
conjunto pode ser confrontado com limites normativos. A CISPR 32, por exemplo,
fixa a emissão radiada Classe B em 30 dBµV/m entre 30 e 230 MHz a 10 m — grandeza
que exige antena com fator individual calibrado e distância normalizada, e com a
qual estes dados não são comparáveis.

**Sobrevive parcialmente à subtração** a não linearidade de amplitude, porque as
duas condições são lidas em níveis distintos — cerca de −73 dBm com a iluminação
acionada contra −87 dBm com ela apagada:

```
Δ_medido = Δ_real + [ e(A_on) − e(A_off) ]
```

O que resta é o desvio de linearidade ao longo desse intervalo de ~14 dB. A
exatidão de amplitude declarada pelo fabricante para a faixa empregada é de
±1 dB, o que limita o termo residual a aproximadamente 2 dB no pior caso.

## Por que o resultado se sustenta

Duas comparações, ambas desfavoráveis à nossa própria posição:

**Contra a incerteza normativa.** A CISPR 16-4-2 atribui a uma medição radiada
*acreditada* incerteza de instrumentação de 4,95 dB a 3 m e 4,94 dB a 10 m. A
elevação observada, de 12 a 13 dB, excede em cerca de duas vezes e meia a
incerteza que a própria norma admite para o ensaio de referência.

**Contra a estabilidade do arranjo.** Para uma diferença tomada no intervalo de
segundos, a grandeza relevante não é o intervalo de calibração, mas a
estabilidade de curto prazo — caracterizada por desvio-padrão de 0,89 dB entre
as cinco varreduras sucessivas da campanha 1. O efeito medido é cerca de quinze
vezes maior.

Some-se o resultado dos controles simultâneos: duas salas sem intervenção,
medidas no mesmo dia com o mesmo instrumento, mantiveram +12,40 e +12,68 dB
enquanto a sala adequada caiu para +1,04 dB. Um desvio de calibração afetaria as
três igualmente e não produziria essa separação.

## Sobre o intervalo de calibração

Não há intervalo normativo universal que tenha sido descumprido. O ILAC-G24 /
OIML D 10:2022 é explícito: o intervalo de recalibração deve ser **definido e
justificado pelo usuário**, a partir do histórico de deriva do instrumento, da
intensidade de uso e da consequência de um resultado fora de tolerância. A
ISO/IEC 17025:2017 exige que exista um programa de calibração, sem fixar
periodicidade. Os doze meses correntes são prática de mercado, não requisito.

Isso não converte a lacuna em conformidade. Há uma lacuna de **rastreabilidade**
— o que é coisa distinta de um prazo vencido, e o que este documento declara.

## O que será acrescentado, e o que isso permitirá

Quando o instrumento for calibrado, esta pasta receberá:

1. `tabela_correcao.csv` — desvio de amplitude por frequência, na resolução
   fornecida pelo laboratório;
2. `certificado.pdf` — certificado de calibração, com identificação do
   laboratório e cadeia de rastreabilidade;
3. `reprocessamento.md` — recálculo de todas as tabelas do artigo com a correção
   aplicada, lado a lado com os valores publicados.

Isso permitirá **caracterizar o instrumento** e **quantificar de quanto a
correção desloca os resultados publicados**. Os dados brutos estão aqui sem
tratamento justamente para que esse reprocessamento seja possível — por nós ou
por terceiros.

### O intervalo de deriva a caracterizar

Limitar a deriva exige saber quando cada leitura foi tomada. As datas estão
fixadas em `../metadados/cronologia.md` e, por arquivo, no campo
`data_aquisicao` do inventário:

| Conjunto | Data de aquisição |
|---|---|
| Campanha 1 — diagnóstico (6 varreduras) | 2026-02-12 |
| Campanha 2 — verificação (42 varreduras) | 2026-07-28 |
| Demonstração de faixa (4 varreduras) | 2026-07-28 |

Sendo `D_cal` a data do certificado, o intervalo a caracterizar é
`[2026-02-12, D_cal]` para a campanha 1 e `[2026-07-28, D_cal]` para as demais.
As duas campanhas estão separadas por cerca de cinco meses e meio, e essa
separação é ela própria objeto do reprocessamento: qualquer deriva ocorrida
nesse intervalo afeta a comparação **entre** campanhas, e não a comparação
pareada **dentro** de cada ponto, pela álgebra da primeira seção.

### O que o reprocessamento não vai alterar

Convém antecipar, para que a expectativa sobre a ação futura seja correta: a
correção de calibração **não desloca os valores relativos publicados**. Sendo a
correção uma função da frequência aplicada igualmente às duas leituras do par,
ela cancela na subtração pelo mesmo argumento que cancela `e_sist`.

O que o reprocessamento entrega é: nível absoluto rastreável, o limite do
resíduo de não linearidade entre os dois níveis lidos, e a caracterização da
deriva nos intervalos acima. É por isso que a comparação futura é com os dados
brutos aqui depositados, e não com os valores já publicados.

### Uma delimitação que precisa ficar clara

Uma calibração futura **não torna as medições de 2026 retroativamente
rastreáveis**. Rastreabilidade metrológica é uma propriedade da medição no
momento em que ela é feita, e nenhum certificado posterior a restitui.

O que uma calibração futura permite é: caracterizar a resposta do instrumento,
limitar sua deriva no intervalo entre as medições e a calibração, e verificar se
a correção altera de forma material as conclusões relativas. É um estudo de
repetibilidade e de caracterização instrumental — valioso, e distinto de
rastreabilidade.

Esta distinção está registrada aqui para que o compromisso assumido não seja
lido como promessa de algo que a metrologia não permite entregar.
