# 📋 Backlog de Teste Piloto - Azure Boards Automation

> **Projeto:** PetGuardian  
> **Disciplina:** Compliance & QA (Automação de Testes e Boards)  
> **Epic Principal:** `[TESTE] Epic Piloto de Validação da Automação Azure Boards`  
> **Finalidade:** Validar a criação automática da hierarquia Epic ➔ Feature ➔ PBI ➔ Task no Azure Boards antes de importar todas as matérias.

---

## 👑 [EPIC-TESTE] Epic Piloto de Validação da Automação Azure Boards
* **Work Item Type:** `Epic`
* **Tags:** `Teste`, `Automacao`, `Sprint3`, `Piloto`
* **Descrição:** Epic piloto criado para validar o script Python de importação automática do Backlog Master da Sprint 3 no Azure Boards.

---

## 🏆 [FEAT-TESTE-01] Feature de Homologação da Hierarquia e Links
* **Work Item Type:** `Feature`
* **Parent Epic:** `[EPIC-TESTE] Epic Piloto de Validação da Automação Azure Boards`
* **Tags:** `Teste`, `Feature`, `Sprint3`
* **Descrição:** Feature de teste destinada a validar a amarração correta entre o Epic pai e os PBIs filhos no Azure Boards.

---

### 🔹 [PBI-TESTE-01] Validação de Leitura de User Story, Tags e Prioridade
* **Work Item Type:** `Product Backlog Item`
* **Parent Feature:** `[FEAT-TESTE-01] Feature de Homologação da Hierarquia e Links`
* **Priority:** `1 - Critical`
* **Effort / Story Points:** `3`
* **Tags:** `Teste`, `PBI`, `Validacao`

#### Descrição (User Story)
> **Como** Desenvolvedor do Projeto PetGuardian,  
> **Eu quero** validar a criação automática de itens de backlog via script Python,  
> **Para que** todo o trabalho manual de cadastro de 65+ PBIs seja feito em segundos com precisão.

#### Critérios de Aceite (Acceptance Criteria)
- [ ] O script deve ler este PBI a partir do arquivo `.md`.
- [ ] O título, prioridade, story points e tags devem ser preenchidos corretamente no Azure DevOps.
- [ ] O link com a Feature pai deve estar estabelecido (`Hierarchy-Reverse`).

#### Tarefas Técnicas (Child Tasks)
- [ ] `[TASK-01]` Executar script em modo `--dry-run` para validar parse.
- [ ] `[TASK-02]` Executar script real e verificar visualmente no Azure Boards.

---

### 🔹 [PBI-TESTE-02] Validação de Critérios de Aceite e Story Points
* **Work Item Type:** `Product Backlog Item`
* **Parent Feature:** `[FEAT-TESTE-01] Feature de Homologação da Hierarquia e Links`
* **Priority:** `2 - High`
* **Effort / Story Points:** `5`
* **Tags:** `Teste`, `PBI`, `StoryPoints`

#### Descrição (User Story)
> **Como** Scrum Master da equipe PetGuardian,  
> **Eu quero** garantir que a pontuação de esforço (Story Points) seja enviada no campo padrão do Azure DevOps,  
> **Para que** os gráficos de Burndown e Velocity funcionem com precisão.

#### Critérios de Aceite (Acceptance Criteria)
- [ ] O campo `Microsoft.VSTS.Scheduling.Effort` deve conter o valor numérico `5`.
- [ ] A prioridade deve estar cadastrada corretamente.
- [ ] A descrição deve conter o texto formatado da história e dos critérios de aceite.
