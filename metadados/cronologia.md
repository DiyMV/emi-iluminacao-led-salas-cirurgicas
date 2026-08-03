# Cronologia das medições

Este documento fixa **quando** cada varredura foi adquirida. A informação é
exigida por dois usos do conjunto: situar cada leitura em relação à intervenção
que separa as duas campanhas, e delimitar o intervalo de deriva instrumental a
ser caracterizado quando houver certificado de calibração (ver
`../calibracao/LEIA-ME.md`).

## Linha do tempo

| Data | Evento | Varreduras |
|---|---|---:|
| 2026-02-12 | **Campanha 1 — diagnóstico.** Sala 03 com a falha clinicamente ativa: artefato na imagem de IVUS e perda de conexão do FFR Link. Cinco varreduras sucessivas com a iluminação acionada e uma referência com ela apagada. | 6 |
| entre 2026-02-12 e 2026-07-28 | **Intervenção na Sala 03.** Substituição do conjunto de drivers de iluminação por modelos com filtro EMI integrado e carcaça metálica aterrada. As salas 01 e 02 não receberam intervenção. *A data exata da substituição não foi registrada em documento contemporâneo e não é afirmada aqui.* | — |
| 2026-07-28 | **Campanha 2 — verificação.** Três salas × sete posições × duas condições, com o mesmo instrumento e o mesmo operador. As salas 01 e 02, sem intervenção, funcionam como controles simultâneos. | 42 |
| 2026-07-28 | **Demonstração de faixa.** Varreduras de 225–575 MHz nas salas 01 e 03, no mesmo dia e nos mesmos pontos centrais da campanha 2, que documentam o falso negativo por escolha inadequada de faixa. | 4 |

O campo `data_aquisicao` do `inventario.json` registra essa data por arquivo.

## Resolução temporal, e por que ela é o dia

**A resolução é o dia. Não há ordenação intradiária, e ela não é reconstruível.**

O analisador não grava carimbo de tempo: o CSV exportado tem duas colunas
numéricas, sem cabeçalho e sem metadado, e os arquivos de configuração e de
preset não guardam relógio. O único horário disponível é o de modificação dos
arquivos no sistema de arquivos, que marca **a cópia do cartão de memória, não a
aquisição**. Isso é verificável: as mesmas varreduras, com conteúdo idêntico por
soma de verificação, aparecem em duas cópias do mesmo dia com horários
diferentes.

Ordenar as varreduras dentro do dia exigiria inventar informação que o
instrumento não produziu, e não se faz aqui.

O que a resolução de dia **não** compromete: a comparação pareada. As duas
condições de cada ponto foram lidas com o mesmo arranjo, sem deslocamento da
antena, separadas por segundos — a estabilidade de curto prazo relevante para
essa diferença está caracterizada pelo desvio-padrão de 0,89 dB entre as cinco
varreduras sucessivas da campanha 1, e não depende de saber a que hora do dia
cada par foi tomado.

## Procedência da datação

As datas não vêm de declaração retrospectiva: cada varredura do repositório foi
casada, por soma de verificação do seu conteúdo numérico, com o acervo de origem
em que aparece pela primeira vez.

| Verificação | Resultado |
|---|---|
| Varreduras com origem localizada | 52 de 52 |
| Presentes já no acervo de fevereiro de 2026 | 6 — exatamente o conjunto da campanha 1 |
| Presentes apenas no acervo de 28/07/2026 | 46 — as 42 da campanha 2 e as 4 da demonstração de faixa |

A data atribuída é a do acervo mais antigo em que a varredura aparece. As seis
varreduras da campanha 1 também constam do descarregamento de julho, porque
permaneceram no cartão de memória do instrumento entre as duas campanhas; isso
não as torna de julho.

## Advertência sobre datas em documentos administrativos

Ordens de serviço e relatórios derivados deste estudo podem trazer a data de
**emissão do documento**, não a da medição. As medições da campanha 2 são de
**28/07/2026**. Em caso de divergência, prevalece a data registrada aqui e no
`inventario.json`, que é a que tem procedência verificável.
