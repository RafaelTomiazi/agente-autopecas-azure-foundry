# Workflow `televendas-rodavale`

Configuração do fluxo no portal do Microsoft Foundry. Versão validada: **4**.

Criado em Agents → Workflows → Create → **Blank workflow**. Não use o template Group chat: ele monta um loop entre dois agentes fixos, não um roteador.

---

## Desenho

```
Start
  |
  v
orquestrador-rodavale                       (devolve ROTA e CONTEXTO)
  |
  v
If / else condition
  |
  +-- ROTA: CATALOGO   --> especialista-catalogo-estoque-rodavale ---+
  |                                                                  |
  +-- ROTA: COTACAO    --> especialista-catalogo-estoque-rodavale    |
  |                            |                                     |
  |                            v                                     |
  |                        especialista-comercial-rodavale ----------+
  |                                                                  |
  +-- ROTA: COMERCIAL  --> especialista-comercial-rodavale ----------+
  |                                                                  |
  +-- Else             --> Deliver a message -----------------------+
                                                                     |
                                                                     v
                                                                    End
```

---

## Nós de agente

Todos usam `System.ConversationId` como **Conversation context**, com **Allow multi-turn conversation** desativado e **Automatically include agent response** ativado.

| Nó | Agente | Input message | Save agent output message as |
|---|---|---|---|
| 1 | `orquestrador-rodavale` | `System.LastMessageText` | `rota_orquestrador` |
| Rota CATALOGO | `especialista-catalogo-estoque-rodavale` | `rota_orquestrador` | — |
| Rota COTACAO, 1º | `especialista-catalogo-estoque-rodavale` | `rota_orquestrador` | `resposta_catalogo` |
| Rota COTACAO, 2º | `especialista-comercial-rodavale` | `resposta_catalogo` | — |
| Rota COMERCIAL | `especialista-comercial-rodavale` | `rota_orquestrador` | — |

O campo **Save output json_object/json_schema as** fica em branco em todos.

Para encadear dois agentes na mesma rota, use o campo **Next node** no painel do primeiro nó. O botão `+` do canvas cria um caminho paralelo, não uma sequência.

---

## Condições

O nó **If / else condition** tem três caminhos com condição e o `Else` sem condição.

```
StartsWith(Last(ShowColumns(Local.rota_orquestrador, Text)).Text, "ROTA: CATALOGO")
StartsWith(Last(ShowColumns(Local.rota_orquestrador, Text)).Text, "ROTA: COTACAO")
StartsWith(Last(ShowColumns(Local.rota_orquestrador, Text)).Text, "ROTA: COMERCIAL")
```

Três detalhes que custaram tentativas até funcionar:

1. **O prefixo `Local.` é obrigatório.** Sem ele: `Name isn't valid. 'rota_orquestrador' isn't recognized`.
2. **A variável é uma tabela de mensagens, não texto.** Sem `Last(...)`: `Invalid argument type (Table). Expecting a Text value`.
3. **Selecionar a coluna com ponto não é aceito.** `Local.rota_orquestrador.Text` retorna `Deprecated use of '.'. Please use the 'ShowColumns' function instead`.

---

## Caminho Else

Nó do tipo **Deliver a message**, com o texto:

```
Esta solicitação está fora do escopo do televendas da Rodavale. Posso ajudar com compatibilidade de peças, estoque, preços, clientes e cotações.
```

Ele atende tanto assuntos fora do televendas quanto qualquer resposta do orquestrador fora do formato esperado.

---

## Operação

- O Foundry **não salva automaticamente**. Clique em Save após cada alteração.
- Cada Save cria uma versão imutável, acessível pelo seletor à esquerda do botão Save.
- Teste sempre no **Preview**, em conversa nova para cada caso.
- A numeração `1.0.0` que aparece na publicação para Teams pertence ao pacote de distribuição e não substitui a versão do workflow.
