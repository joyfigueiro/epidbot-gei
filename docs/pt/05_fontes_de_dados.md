# 05. Fontes de dados

Este documento lista as famílias de fontes que o substrato alcança, com a rota de acesso e
a latência típica de cada uma. Latência é o atraso entre o período de referência e a
disponibilidade do dado, que é a quantidade que determina se uma pergunta sobre o passado
recente pode ser respondida.

| Família | Exemplos | Rota de acesso | Latência típica |
| --- | --- | --- | --- |
| Doenças de notificação | Listas do SINAN, dados abertos do Ministério da Saúde (DEMAS) | Arquivos em lote e API REST | Semanas a meses |
| Mortalidade | SIM | Arquivos por estado e ano | Meses |
| Nascidos vivos | SINASC | Arquivos por estado e ano | Meses |
| Atenção hospitalar | SIH, SIA, CIHA | Arquivos mensais por estado | Dois a seis meses |
| Estabelecimentos de saúde | CNES | Arquivos mensais | Um a três meses |
| Imunização | Registros de doses do PNI, eventos adversos | Arquivos anuais e mensais | Meses |
| Saneamento e água | SISAGUA | Arquivos anuais | Meses |
| Atenção primária | Indicadores do Previne Brasil, programas de provimento médico | API REST | Trimestral |
| Vigilância de arboviroses | InfoDengue, Mosqlimate, redes de ovitrampas | API REST | Dias a semanas |
| Vetores e ambiente | Ocorrência de vetores, séries climáticas, índices de vegetação | API REST e serviços raster | Dias |
| Genômica | Pathoplexus | API REST | Dias a semanas |
| Vigilância internacional | OMS, OPAS, ECDC, Eurostat, Banco Mundial, UN Data | API REST | Meses |
| Geografia | Malhas do IBGE, unidades administrativas do GADM | Arquivos em lote | Anual |
| Terminologia e preços regulados | SIGTAP, TUSS, banco de preços em saúde | Arquivos em lote e API | Mensal |
| Literatura científica | PubMed, OpenAlex, CrossRef, arXiv, servidores de preprints | API REST | Imediata |

## Como o catálogo é usado

Toda fonte é registrada com um descritor que declara origem, licença, cobertura temporal,
resolução espacial, cadência de atualização e problemas de qualidade conhecidos. O
planejador lê o descritor antes de escolher a fonte. Dois comportamentos decorrem disso. Um
pedido fora da cobertura de todas as fontes registradas devolve declaração da lacuna, não
um conjunto substituto. Um pedido cuja resposta depende de dados ainda em revisão devolve a
análise junto com a data de extração, para que o leitor saiba o que estava disponível
quando o número foi produzido.

## Atualidade como achado

A tabela acima também é um resultado. Perguntas sobre as últimas semanas podem ser
respondidas para vigilância de arboviroses e clima, e não podem ser respondidas para
mortalidade ou internações. Os usuários descobrem isso no uso, e o registro de uso mostra
que a atualidade é um dos pontos de atrito mais frequentes. Tornar a latência explícita é,
portanto, parte do projeto e não uma ressalva acrescentada depois.
