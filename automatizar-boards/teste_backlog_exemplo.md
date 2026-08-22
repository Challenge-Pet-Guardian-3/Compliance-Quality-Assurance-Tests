# 📋 Backlog de Teste Piloto - Azure Boards Automation

> **Projeto:** PetGuardian  
> **Disciplina:** Compliance & QA (Automação de Testes e Boards)  
> **Epic Principal:** `[TESTE] Epic Piloto de Validação da Automação Azure Boards`  
> **Finalidade:** Validar a criação automática da hierarquia Epic ➔ Feature ➔ PBI ➔ Task com Start Date, Target Date e Activity no Azure Boards antes de importar todas as matérias.

---

## 👑 [EPIC-TESTE] Epic Piloto de Validação da Automação Azure Boards
* **Work Item Type:** `Epic`
* **Tags:** `Teste`, `Automacao`, `Sprint3`, `Piloto`
* **Start Date:** `2026-08-23`
* **Target Date:** `2026-09-05`
* **Descrição:** Epic piloto criado para validar o script Python de importação automática do Backlog Master da Sprint 3 no Azure Boards com datas de início/término e atividades das tarefas.

---

## 🏆 [FEAT-TESTE-01] Feature de Homologação da Hierarquia, Datas e Activity
* **Work Item Type:** `Feature`
* **Parent Epic:** `[EPIC-TESTE] Epic Piloto de Validação da Automação Azure Boards`
* **Tags:** `Teste`, `Feature`, `Sprint3`, `Dates`
* **Start Date:** `2026-08-23`
* **Target Date:** `2026-08-26`
* **Descrição:** Feature de teste destinada a validar a amarração correta entre o Epic pai, PBIs filhos, Start/Target Dates e Activity das Tasks no Azure Boards.

---

### 🔹 [PBI-TESTE-01] Validação de Leitura de User Story, Tags e Prioridade
* **Work Item Type:** `Product Backlog Item`
* **Parent Feature:** `[FEAT-TESTE-01] Feature de Homologação da Hierarquia, Datas e Activity`
* **Priority:** `1 - Critical`
* **Effort / Story Points:** `3`
* **Tags:** `Teste`, `PBI`, `Validacao`

#### Descrição (User Story)
> **Como** Desenvolvedor do Projeto PetGuardian,  
> **Eu quero** validar a criação automática de itens de backlog com Start Date, Target Date e Activity nas Tasks,  
> **Para que** todo o trabalho manual de cadastro de 65+ PBIs e 150+ Tasks seja feito em segundos com precisão no Azure DevOps.

#### Critérios de Aceite (Acceptance Criteria)
- [ ] O script deve ler o Epic com Start Date (`2026-08-23`) e Target Date (`2026-09-05`).
- [ ] O script deve ler a Feature com Start Date (`2026-08-23`) e Target Date (`2026-08-26`).
- [ ] O título, prioridade, story points e tags devem ser preenchidos corretamente no Azure DevOps.
- [ ] Cada Task técnica deve conter o campo Activity preenchido (`Development`, `Testing`, `Documentation`, etc.).

#### Tarefas Técnicas (Child Tasks)
* **Task 1.1:** `[TASK-01]` Executar script em modo `--dry-run` para validar parse de datas e activities. *(Activity: Testing, Est: 1.0h)*
* **Task 1.2:** `[TASK-02]` Desenvolver parser de Start Date, Target Date e Activity no `parser_backlog.py`. *(Activity: Development, Est: 2.0h)*
* **Task 1.3:** `[TASK-03]` Atualizar documentação técnica e instruções com o novo formato. *(Activity: Documentation, Est: 0.5h)*

---

### 🔹 [PBI-TESTE-02] Validação de Critérios de Aceite, Story Points e Activity
* **Work Item Type:** `Product Backlog Item`
* **Parent Feature:** `[FEAT-TESTE-01] Feature de Homologação da Hierarquia, Datas e Activity`
* **Priority:** `2 - High`
* **Effort / Story Points:** `5`
* **Tags:** `Teste`, `PBI`, `StoryPoints`

#### Descrição (User Story)
> **Como** Scrum Master da equipe PetGuardian,  
> **Eu quero** garantir que a pontuação de esforço (Story Points), datas de planejamento e atividades sejam enviadas nos campos padrão do Azure DevOps,  
> **Para que** os gráficos de Burndown, Velocity, Roadmap e Capacity Planning funcionem com precisão.

#### Critérios de Aceite (Acceptance Criteria)
- [ ] O campo `Microsoft.VSTS.Scheduling.Effort` deve conter o valor numérico `5`.
- [ ] A prioridade deve estar cadastrada corretamente.
- [ ] A descrição deve conter o texto formatado da história e dos critérios de aceite.
- [ ] As Tasks filhas devem possuir Activity preenchido (`Development`, `Design`, `Testing`, etc.).

#### Tarefas Técnicas (Child Tasks)
* **Task 2.1:** `[TASK-04]` Criar payload de envio dos campos `Microsoft.VSTS.Scheduling.StartDate` e `TargetDate`. *(Activity: Development, Est: 1.5h)*
* **Task 2.2:** `[TASK-05]` Validar sincronização de `Microsoft.VSTS.Common.Activity` nas Tasks. *(Activity: Testing, Est: 1.0h)*
