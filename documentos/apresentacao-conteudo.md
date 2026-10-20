# Conteúdo da apresentação — Assistente de Catálogo Rodavale

Fonte do arquivo `Apresentacao-Rodavale.pptx`.

**Princípio da estrutura.** Modo usuário/produto lidera a apresentação; modo técnico fica no anexo e só entra quando questionado. A sequência responde, nesta ordem: o que o usuário consegue fazer agora, o que conseguimos provar, o que isso significa para a decisão.

Nove slides na apresentação. Quatro slides de anexo, que não são apresentados — existem para responder pergunta.

---

## Slide 1 — Capa

KUMULUS

**Assistente de Catálogo**

O vendedor pergunta como o cliente fala. A resposta vem do catálogo.

Rafael Tomiazi · Rodavale Distribuidora de Autopeças

---

## Slide 2 — O que o vendedor consegue fazer agora

> "Agora eu pergunto o que serve num Onix 2018 1.4 e recebo as peças aplicáveis, o preço do meu cliente e o estoque — em segundos, na mesma conversa."

| Antes | Agora |
|---|---|
| Procurar por código no ERP | Perguntar pelo veículo |
| Consultar um vendedor experiente | Resposta imediata, sem depender de ninguém |
| Abrir outra tela para o desconto do cliente | Cotação com a tabela do cliente aplicada |
| Chutar quando não acha | O assistente diz que não existe |

Três capacidades novas:

- **Perguntar pelo veículo, não pelo código.** Montadora, modelo, ano, motorização e posição da peça.
- **Cotar com o desconto do cliente na hora.** Preço-base, tabela do cliente e preço final na mesma resposta.
- **Saber quando a peça não existe.** O assistente informa que não encontrou, em vez de sugerir algo parecido.

---

## Slide 3 — Por que isso importa

O cliente não liga pedindo um código. Ele pergunta se a peça serve no carro dele.

| 11 min | 30% | 6% |
|---|---|---|
| tempo médio de atendimento | chamadas que exigem retorno posterior | pedidos perdidos por demora |

**Causa raiz:** a tradução entre "meu carro" e "este código" acontece na memória de dois vendedores experientes.

Rodapé: premissas levantadas na pré-venda. A descoberta mede os números reais da operação.

---

## Slide 4 — Como funciona, em três papéis

Um ponto de entrada para o vendedor. Três responsabilidades separadas.

| Papel | O que faz |
|---|---|
| **Triagem** | Entende o que foi pedido e encaminha para quem responde |
| **Especialista de peças** | Compatibilidade, código, marca, preço de tabela e saldo por filial |
| **Especialista de preço** | Cliente, tabela, desconto e cotação |

**Na cotação, os dois trabalham em sequência.** O especialista de peças confirma a peça antes de o especialista de preço aplicar o desconto. Ninguém dá preço de peça que não confirmou.

Três regras de comportamento:

- **Ancorado no catálogo.** Não inventa código, preço nem saldo.
- **Somente consulta.** Não cria pedido, reserva nem aprovação de crédito.
- **O vendedor decide.** O assistente apresenta opções; a recomendação continua sendo do profissional.

Rodapé: a arquitetura que sustenta isso está no anexo.

---

## Slide 5 — Demonstração

| # | O que vou perguntar | O que observar |
|---|---|---|
| 1 | Pastilha dianteira para Onix 2018 1.4 | Filtra por ano e motorização, não só pelo nome da peça |
| 2 | Cotação da RV-1002 para a Auto Center Central | Confirma a peça e depois aplica o desconto do cliente |
| 3 | Pastilha para uma Kia Sportage 2020 | Não existe na base. O assistente diz isso |

O caso 3 é tão importante quanto a cotação: é o que evita vender peça incompatível.

---

## Slide 6 — O que conseguimos provar

Seis casos testados com gabarito conferido na base. Seis aprovados.

| Caso | Resultado |
|---|---|
| Consulta por veículo | Cinco peças corretas, exclui a que é só de motor 1.0 |
| Consulta comercial | Cliente localizado, tabela correta |
| Cotação | Preço de tabela com o desconto do cliente aplicado |
| Conversa em duas mensagens | Mantém o contexto e respeita a faixa de anos |
| Peça fora da base | Informa que não encontrou |
| Pergunta fora do assunto | Responde o escopo do assistente |

**Escopo da evidência:** 3.367 aplicações veiculares, 194 produtos, 90 clientes e 24 regras de desconto, sobre uma posição de catálogo e estoque datada.

**O que a próxima etapa precisa medir:** o catálogo completo de 18.000 SKUs, o uso simultâneo pela equipe de televendas e a atualização a partir do ERP.

---

## Slide 7 — O que isso significa para a decisão

**01 — A hipótese se confirmou.** O vendedor resolve aplicação, preço e estoque em uma conversa, sem desenvolver sistema e sem infraestrutura para a TI manter.

**02 — O ambiente real ainda precisa ser mapeado.** Catálogo completo, ERP, volume de atendimento e perfis de acesso.

**03 — A decisão de hoje é seguir para o ambiente real.** Não é aprovar o projeto inteiro.

---

## Slide 8 — Próximo passo e investimento

| Etapa | Valor | O que entrega |
|---|---|---|
| **Assinatura mensal** | R$ 4.500/mês · 12 meses | Implantação, integração com o ERP, sustentação e evolução. Sem investimento inicial |
| **Primeiro mês** | Descoberta | Levanta ERP, catálogo e acessos. Confirma ou ajusta o valor antes do compromisso de 12 meses |

Não há investimento inicial. O consumo do Azure é faturado pelo provedor e dimensionado na descoberta, conforme volume de consultas e de buscas no catálogo.

**R$ 4.500 por mês contra uma economia estimada de R$ 9.900 por mês.** A conta fecha já no primeiro mês — e é isso que a descoberta vai medir.

Base da economia estimada: 4 minutos por atendimento, 270 atendimentos por dia, 22 dias — cerca de 396 horas por mês. É premissa de pré-venda, não medição.

---

## Slide 9 — Encerramento

**O que o vendedor fez aqui com 3.367 aplicações, ele faz com o catálogo inteiro.**

O que muda é a origem do dado, não a experiência.

Obrigado.

Rafael Tomiazi

Entregáveis: proposta comercial · documentação técnica · solução funcional no Microsoft Foundry

---

# Anexo — não apresentado

Slides de resposta. Abrir somente se perguntarem.

## Anexo 1 — O requisito do desafio

Simular um ciclo completo de pré-vendas e entrega: criar o cliente, diagnosticar o problema, propor e implementar.

Requisito da revisão: arquitetura multiagente, com no mínimo três agentes e um orquestrador, configurada sem código.

Atendido: `orquestrador-rodavale`, `especialista-catalogo-estoque-rodavale` e `especialista-comercial-rodavale`, com roteamento visual no Workflow do Foundry. Nenhuma linha de código na solução.

## Anexo 2 — Arquitetura

```
Orquestrador  -->  If / else condition
                     CATALOGO   --> Catálogo e Estoque
                     COTACAO    --> Catálogo --> Comercial
                     COMERCIAL  --> Comercial
                     Else       --> mensagem padrão
```

| Camada | Componente |
|---|---|
| Interface | Microsoft Foundry |
| Orquestração | Workflow do Foundry, condição Power Fx |
| Agentes | Foundry Agent Service |
| Modelo | GPT-5-mini |
| Conhecimento | File Search — catálogo, índice de SKUs e base comercial |

## Anexo 3 — Decisões técnicas

- **Três agentes, não um.** Um agente com todos os assuntos mistura domínios: aplica desconto sem confirmar a peça, sugere peça sem checar a aplicação.
- **Orquestrador sem ferramentas.** Ele só classifica. Sem arquivos, não tem como inventar preço ou estoque.
- **Roteamento por condição no fluxo.** O caminho é explícito e auditável, visível no diagrama e no rastreamento.
- **Dois arquivos de catálogo.** O completo responde por veículo; o índice compacto responde por código. Foi o que fez a cotação funcionar.
- **Modelo mini.** A tarefa é classificar, buscar e formatar. Modelo maior custaria mais sem ganho.

## Anexo 4 — Limites e encaminhamento

| Limite | Encaminhamento |
|---|---|
| Base é uma posição de 20/08/2026, sem tempo real | Sincronização automática com o ERP |
| Sem controle de acesso por perfil | Restrição do projeto em produção |
| Bases indexadas em East US | Provisionamento em Brazil South na implantação |
| Até dez opções por resposta | Refinamento por marca, filial ou preço |
| Workflows do Foundry saem em 01/12/2026 | Migrar o roteamento para Agent Framework ou Logic Apps |
| A camada SQL + MCP da versão 1 ficou fora do escopo | Retomar quando "sem código" não for o critério dominante |

Hoje não existe no Foundry um caminho de orquestração sem código com longevidade garantida. A escolha foi a melhor opção dentro da restrição, com a migração já mapeada.
