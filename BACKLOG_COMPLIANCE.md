# 📋 Backlog Master Azure Boards — Sprint 3: Compliance, Quality Assurance & Tests

> **Projeto Integrado:** PetGuardian / Clyvo Care (Challenge FIAP 2026 - 2º Ano ADS / 2TDSPG)  
> **Disciplina:** Compliance, Quality Assurance & Tests (FIAP — 2TDSPG)  
> **Epic Principal:** `[EPIC] Sprint 3 - Compliance, Quality Assurance & Tests: Governança Scrum, Gestão do Backlog e Asseguração da Qualidade`  
> **Start Date:** `2026-08-30`  
> **Target Date:** `2026-09-05`  
> **Padrão:** Azure Boards (Scrum Process: Epic ➔ Feature ➔ PBI ➔ Task)  
> **Diretrizes Estratégicas:** 100% de aderência à rubrica oficial da Sprint 3 (5 critérios de 20% cada), gestão ágil e governança de backlog no padrão Scrum do Azure Boards, alinhamento estrito com os objetivos de produto da plataforma PetGuardian, padronização de Histórias de Usuário com critérios de aceitação e Definition of Done (DoD), balanceamento temporal de entregas (Release Plan Semana 1 vs Semana 2) e mapeamento da matriz de dependências técnicas cruzadas entre as 7 disciplinas.

---

## 👥 Integrantes do Grupo (Ordem Alfabética Estrita)

> ⚠️ **Regra da Banca:** Todos os documentos, apresentações e entregáveis do Challenge mantêm a ordem alfabética estrita dos integrantes.

| Integrante | RM | Turma | Papel no Projeto / Foco na Sprint 3 |
| :--- | :---: | :---: | :--- |
| **Enzo Okuizumi** | **561432** | 2TDSPG | Mobile Application Development, Integração de APIs e Coordenação Geral |
| **Gustavo Okada** | **563428** | 2TDSPG | Java Advanced (Spring Security, Flyway, SOLID) & .NET Observabilidade |
| **Lucas Barros Gouveia** | **566422** | 2TDSPG | Database Advanced (PL/SQL Avançado, Auditoria DML, Triggers e Funções) |
| **Luna de Carvalho Guimarães** | **562290** | 2TDSPG | Disruptive Architectures (FastAPI, RAG, IA Generativa) & Compliance / QA Lead |
| **Milton Marcelino** | **564836** | 2TDSPG | DevOps Tools & Cloud Computing (Azure CLI, ACR, ACI, Containers e IaC) |

---

## 🎯 1. Matriz de Alinhamento com a Rubrica da Sprint 3 (5 Critérios Avaliativos — 20% Cada)

A tabela abaixo sintetiza o atendimento integral a todos os critérios avaliativos da Sprint 3 na disciplina de Compliance, Quality Assurance & Tests:

| Critério Avaliativo | Peso na Rubrica | Escopo e Implementação Prática no Projeto PetGuardian | Evidência de Conformidade |
| :--- | :---: | :--- | :--- |
| **1. Estrutura de Backlog de Produto** | **20%** | Backlog 100% estruturado na hierarquia oficial do Azure Boards Scrum Template: 1 Épico integrador, 2 Features de governança e release, 6 PBIs de planejamento/gestão e 12 Tasks técnicas de execução. | Hierarquia estrita documentada em Markdown e cadastrada no Azure Boards com rastreabilidade formal. |
| **2. Histórias de Usuário & Critérios de Aceite** | **20%** | Todos os PBIs redigidos no padrão canônico (`Como... Eu quero... Para que...`), vinculados a critérios de aceitação objetivos, testáveis e alinhados à Definition of Done (DoD). | Histórias e DoDs isoladas nos campos nativos `System.Description` e `Microsoft.VSTS.Common.AcceptanceCriteria` no Azure DevOps. |
| **3. Prioridade, Esforço & Dependências** | **20%** | Definição explícita de Prioridades (1 - Critical a 4 - Low), pontuação de esforço em Story Points (3 SP por PBI = 18 SP total) e mapeamento exaustivo de dependências técnicas entre as 7 disciplinas. | Matriz de Dependências Técnicas Cruzadas documentada e atributos de negócio atribuídos a todos os itens de trabalho. |
| **4. Release Plan da Sprint 3** | **20%** | Planejamento de entregas temporal balanceado entre a Semana 1 (Mobile, Java, Database - 64 SP / 180.0h) e a Semana 2 (.NET, DevOps, Disruptive IA, Compliance - 54 SP / 182.0h), garantindo previsibilidade. | Cronograma de marcos da Sprint 3 com datas-alvo e segregação oficial em Iteration Paths (`Semana 1` vs `Semana 2`). |
| **5. Detalhamento da Sprint Atual (Tasks)** | **20%** | Decomposição técnica em 12 Tasks filhas com estimativas em horas realistas (2.5h cada, totalizando 30.0h), classificação normalizada de atividade (`Requirements`, `Development`, `Documentation`) e descrições detalhadas. | Tasks vinculadas aos PBIs pais no Azure Boards com controle de `Remaining Work` e campo de `Activity`. |

---

## 🐾 2. Visão do Produto e Objetivos do Challenge PetGuardian

O **PetGuardian (Clyvo Care)** é um ecossistema digital integrado concebido para transformar o cuidado com animais de estimação, promovendo a saúde preventiva, a colaboração familiar e o bem-estar animal contínuo.

### 🌟 Proposta de Valor e Pilares Funcionais
1. **Arquitetura Pet-Centric:** O pet é a entidade central absoluta da plataforma. Pontuação de saúde, histórico de vacinas, peso, rotinas de alimentação, medicações e passeios são vinculados diretamente ao animal.
2. **Rede Colaborativa de Cuidado (Care Circle):** Suporte à gestão familiar N:N (`UsuarioPet`), permitindo que múltiplos co-cuidadores compartilhem responsabilidades diárias sobre os mesmos pets.
3. **Gamificação e Engajamento:** Pontuação de bem-estar (`PetScore`) acumulada conforme tarefas da rotina familiar são concluídas, incentivando a disciplina e o cuidado contínuo.
4. **Assistência Inteligente e Triagem de Emergência:** Suporte a chat inteligente com IA generativa e RAG especializado para primeiros cuidados e localização de clínicas veterinárias 24h georreferenciadas.

### 🎯 Desdobramento da Visão nos Backlogs das Disciplinas
Para materializar essa visão de negócio, a liderança de QA e Governança estruturou e refinou colaborativamente os backlogs específicos de cada uma das frentes técnicas:
- **Database Advanced (Oracle):** Modelagem relacional em 3FN, procedimentos analíticos PL/SQL e tabelas de auditoria DML.
- **Java Advanced (Spring Boot):** API RESTful core de negócio, autenticação stateless JWT e controle de acesso da rede familiar.
- **Mobile Application Development (React Native/Expo):** Aplicativo móvel intuitivo, consumo reativo via TanStack Query e rotas protegidas.
- **.NET & Observabilidade (ASP.NET Core):** Serviços auxiliares, instrumentação OpenTelemetry, health checks e testes automatizados AAA.
- **DevOps Tools & Cloud Computing (Azure):** Infraestrutura em nuvem serverless via ACR e ACI provisionada 100% via Azure CLI.
- **Disruptive Architectures (FastAPI/Python):** Microsserviço de inteligência artificial com ChromaDB e orquestração de LLMs.
- **Compliance, QA & Tests (Azure Boards):** Governança ágil de processos Scrum, alinhamento dos critérios avaliativos e garantia da qualidade integrada.

---

## 📅 3. Release Plan da Sprint 3 & Balanceamento Temporal

O plano de entregas da Sprint 3 foi estruturado com divisão rigorosa em duas fases sequenciais para eliminar gargalos de integração e respeitar a cadeia de dependências arquiteturais entre as 7 disciplinas:

```text
+---------------------------------------------------------------------------------------------------+
|                                       RELEASE PLAN - SPRINT 3                                     |
+--------------------------------------------------+------------------------------------------------+
| SEMANA 1 (2026-08-23 a 2026-08-29)               | SEMANA 2 (2026-08-30 a 2026-09-05)             |
| Foco: Arquitetura Core, Dados e Frontend Base    | Foco: Cloud, Observabilidade, IA e Governança  |
+--------------------------------------------------+------------------------------------------------+
| - Database Advanced (Oracle PL/SQL): 20 SP / 47h | - .NET & Observabilidade: 13 SP / 62.0h        |
| - Java Advanced (Spring Boot Core): 24 SP / 82.5h| - DevOps Tools & Cloud (Azure): 10 SP / 42.0h  |
| - Mobile Application (React Native): 20 SP / 50.5h| - Disruptive IA (FastAPI/RAG): 13 SP / 48.0h   |
|                                                  | - Compliance, QA & Tests: 18 SP / 30.0h        |
+--------------------------------------------------+------------------------------------------------+
| SUBTOTAL SEMANA 1: 64 SP | 180.0h                | SUBTOTAL SEMANA 2: 54 SP | 182.0h              |
+--------------------------------------------------+------------------------------------------------+
| TOTAL GLOBAL SPRINT 3 (7 DISCIPLINAS): 118 Story Points (Scrum) | 362.0h Líquidas / 370.0h Totais |
+---------------------------------------------------------------------------------------------------+
```

---

## 🔄 4. Matriz de Dependências Técnicas Cruzadas (Cross-Discipline Matrix)

A governança de qualidade estabelece contratos de interface estritos entre todas as disciplinas do projeto:

```text
                  ┌──────────────────────────────────────────────┐
                  │          Database Advanced (Oracle)          │
                  │   DDL 3FN, Seeds, PL/SQL Functions, DML Trig │
                  └──────┬──────────────┬──────────────┬─────────┘
                         │              │              │
            ┌─────────────▼────┐   ┌─────▼────────┐  ┌──▼──────────────────┐
            │  Java Advanced   │   │ .NET Core API│  │ Disruptive IA (Py)  │
            │  Spring Boot/JWT │   │ EF Core, AAA │  │ SQLAlchemy, ChromaDB│
            └──────┬───────────┘   └─────┬────────┘  └──┬──────────────────┘
                   │                     │              │
                   │       ┌─────────────▼─────────┐    │
                   │       │ DevOps (ACR + ACI)    │    │
                   │       │ Azure CLI Cloud Deploy│    │
                   │       └───────────────────────┘    │
                   │                                    │
            ┌──────▼────────────────────────────────────▼──────────┐
            │      Mobile Application Development (React Native)    │
            │      Auth JWT, Care Circle, Routines, AI Chat Screen │
            └──────────────────────────┬───────────────────────────┘
                                       │
            ┌──────────────────────────▼───────────────────────────┐
            │     Compliance, Quality Assurance & Tests (QA Lead)  │
            │     Scrum Governance, Backlog Planning, Quality DoD  │
            └──────────────────────────────────────────────────────┘
```

| Disciplina de Origem | Disciplina de Destino | Artefato / Contrato de Interface Compartilhado |
| :--- | :--- | :--- |
| **Database Advanced** | **Java, .NET, Disruptive IA** | Modelo relacional 3FN higienizado (`PET`, `HISTORICO_CONSULTA`, `TREINAMENTO_PET`, `TAREFA_ROTINA`). |
| **Database Advanced** | **DevOps** | Script DDL segregado `script_bd.sql` para inicialização do container de banco no ACI com volume persistente. |
| **Java Advanced** | **Mobile Development** | Endpoints de autenticação JWT (`/login`), gestão de pets (`/pets`), rede de cuidado e rotinas diárias. |
| **.NET & Observabilidade** | **DevOps** | Código-fonte C# e `Dockerfile` multi-stage com usuário non-root (`appuser`) para build e push no ACR. |
| **Disruptive Architectures** | **Mobile Development** | Endpoints REST em FastAPI (`/api/v1/chat`, `/api/v1/triage`) para consumo na tela `AiAssistantScreen.tsx`. |
| **Compliance, QA & Tests** | **Todas as Disciplinas** | Padrões de backlog Scrum, alinhamento de prioridades, validação de critérios de aceite e governança ágil. |

---

## 🌳 5. Estrutura Hierárquica no Azure Boards

```text
[EPIC] Sprint 3 - Compliance, Quality Assurance & Tests: Governança Scrum, Gestão do Backlog e Asseguração da Qualidade
│
├── 🏆 [FEATURE 01] Planejamento, Estruturação e Construção do Backlog Geral no Azure Boards
│   ├── 📄 [PBI-01] Planejamento e Estruturação Hierárquica dos Épicos e Features de Todas as Disciplinas (3 pts)
│   │   ├── 🔹 Task 1.1: Realizar levantamento dos requisitos das 6 frentes técnicas e mapear a arquitetura de Épicos (2.5h)
│   │   └── 🔹 Task 1.2: Estruturar as Features funcionais no Azure Boards alinhadas ao escopo de cada matéria (2.5h)
│   ├── 📄 [PBI-02] Estruturação Product Backlog Items (PBIs) e Redação das Histórias de Usuário (3 pts)
│   │   ├── 🔹 Task 2.1: Redigir Histórias de Usuário no padrão canônico (Como/Quero/Para que) para todas as matérias (2.5h)
│   │   └── 🔹 Task 2.2: Cadastrar e organizar os PBIs no backlog do Azure Boards vinculando-os às Features pai (2.5h)
│   └── 📄 [PBI-03] Padronização dos Critérios de Aceite Multidisciplinar (3 pts)
│       ├── 🔹 Task 3.1: Definir checklists de critérios de aceitação objetivos e testáveis por item de trabalho (2.5h)
│       └── 🔹 Task 3.2: Formalizar os critérios de Definition of Done (DoD) e qualidade contínua para o time (2.5h)
│
└── 🏆 [FEATURE 02] Priorização, Gestão de Dependências, Release Planning e Detalhamento da Sprint
    ├── 📄 [PBI-04] Dimensionamento de Esforço em Story Points e Apontamento de Prioridades de Negócio (3 pts)
    │   ├── 🔹 Task 4.1: Conduzir sessões de Planning Poker para estimativa de Story Points dos PBIs do projeto (2.5h)
    │   └── 🔹 Task 4.2: Classificar prioridades de negócio (1 - Critical a 4 - Low) e ordenar o backlog para entrega (2.5h)
    ├── 📄 [PBI-05] Mapeamento da Matriz de Dependências Técnicas Cruzadas entre as Frentes (3 pts)
    │   ├── 🔹 Task 5.1: Mapear acoplamentos e contratos de dados entre Banco de Dados, APIs Backend e Frontend Mobile (2.5h)
    │   └── 🔹 Task 5.2: Documentar a matriz de dependências técnicas cruzadas para mitigar riscos de bloqueio (2.5h)
    └── 📄 [PBI-06] Estruturação do Release Plan da Sprint 3 e Detalhamento das Tarefas Técnicas em Horas (3 pts)
        ├── 🔹 Task 6.1: Elaborar o cronograma de entregas balanceado entre Semana 1 e Semana 2 da Sprint 3 (2.5h)
        └── 🔹 Task 6.2: Decompor os PBIs da disciplina em Tarefas filhas com estimativas em horas e tipos de atividade (2.5h)
```

---

## 📊 6. Tabela Resumo do Backlog

| Feature Pai | ID do PBI | Título do Item de Backlog (PBI) | Story Points | Prioridade | Horas Estimadas |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **[FEATURE 01] Estruturação do Backlog** | **PBI-01** | Planejamento e Estruturação Hierárquica dos Épicos e Features de Todas as Disciplinas | 3 pts | 1 - Critical | 5.0h |
| | **PBI-02** | Estruturação Product Backlog Items (PBIs) e Redação das Histórias de Usuário | 3 pts | 1 - Critical | 5.0h |
| | **PBI-03** | Padronização dos Critérios de Aceite Multidisciplinar | 3 pts | 1 - Critical | 5.0h |
| **[FEATURE 02] Priorização e Release Plan**| **PBI-04** | Dimensionamento de Esforço em Story Points e Apontamento de Prioridades de Negócio | 3 pts | 1 - Critical | 5.0h |
| | **PBI-05** | Mapeamento da Matriz de Dependências Técnicas Cruzadas entre as Frentes | 3 pts | 1 - Critical | 5.0h |
| | **PBI-06** | Estruturação do Release Plan da Sprint 3 e Detalhamento das Tarefas Técnicas em Horas | 3 pts | 1 - Critical | 5.0h |
| **TOTAL CONSOLIDADO** | **2 Features** | **6 PBIs / 12 Child Tasks Técnicas** | **18 pts** | — | **30.0h** |

---

## 📦 7. Detalhamento dos Itens de Trabalho (Épico, Features, PBIs e Tasks)

---

### 🏛️ ÉPICO
* **Work Item Type:** `Epic`
* **Title:** `[EPIC] Sprint 3 - Compliance, Quality Assurance & Tests: Governança Scrum, Gestão do Backlog e Asseguração da Qualidade`
* **Tags:** `Sprint3, Compliance, QA, Scrum, AzureBoards, Governance`
* **Start Date:** `2026-08-30`
* **Target Date:** `2026-09-05`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `18`
* **Business Value:** `100`
* **Description:** Planejamento colaborativo, governança ágil e asseguração da qualidade de todo o backlog da Sprint 3 no projeto PetGuardian, abrangendo a estruturação hierárquica dos Épicos de todas as frentes técnicas no padrão Scrum, a elaboração e padronização de Histórias de Usuário com critérios de aceitação objetivos (Definition of Done), o dimensionamento de esforço em Story Points, o sequenciamento de dependências técnicas cruzadas e a criação de um Release Plan balanceado entre Semana 1 e Semana 2.

---

### 🏆 [FEATURE 01] Planejamento, Estruturação e Construção do Backlog Geral no Azure Boards
* **Work Item Type:** `Feature`
* **Parent:** `[EPIC] Sprint 3 - Compliance, Quality Assurance & Tests: Governança Scrum, Gestão do Backlog e Asseguração da Qualidade`
* **Title:** `[FEATURE 01] Planejamento, Estruturação e Construção do Backlog Geral no Azure Boards`
* **Tags:** `Sprint3, Compliance, Governance, Scrum, AzureBoards, ProductBacklog`
* **Start Date:** `2026-08-30`
* **Target Date:** `2026-09-02`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `9`
* **Description:** Concepção, estruturação arquitetural e cadastramento de todo o Backlog de Produto no padrão Scrum do Azure Boards, decompondo os objetivos do projeto em Épicos temáticos por disciplina, Features funcionais e PBIs granulares com Histórias de Usuário e critérios de aceite auditáveis.

#### 🔹 [PBI-01] Planejamento e Estruturação Hierárquica dos Épicos e Features de Todas as Disciplinas
* **Work Item Type:** `Product Backlog Item`
* **Parent Feature:** `[FEATURE 01] Planejamento, Estruturação e Construção do Backlog Geral no Azure Boards`
* **State:** `Approved`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `3`
* **Tags:** `Sprint3, Compliance, Scrum, Architecture, Governance, AzureBoards`

##### Descrição (História de Usuário)
> **Como** Product Owner e Líder de Governança Ágil,  
> **Eu quero** estruturar a arquitetura hierárquica de Épicos e Features de todas as 6 disciplinas técnicas do Challenge no padrão Scrum do Azure Boards,  
> **Para que** o time possua visibilidade consolidada do escopo global do projeto, alinhamento funcional entre as entregas e total rastreabilidade arquitetural.

##### Critérios de Aceite (Acceptance Criteria / Definition of Done)
- [ ] Árvore Scrum formalizada contendo 1 Épico transversal por disciplina técnica do Challenge.
- [ ] Features funcionais organizadas por domínio de entrega (Autenticação, Dados 3FN, Observabilidade, Cloud, IA, Mobile e QA).
- [ ] Relação pai-filho (`Parent`) configurada corretamente para todos os itens no Azure Boards.
- [ ] Nomenclatura e tags padronizadas atribuídas sem inconsistências.

##### Tarefas Técnicas (Child Tasks)
* **Task 1.1:** [TASK-01] Realizar levantamento dos requisitos das 6 frentes técnicas e mapear a arquitetura de Épicos. *(Activity: Requirements, Est: 2.5h)*
  * *Descrição:* Analisar os editais e orientações de cada matéria para consolidar os Épicos mestres e escopos funcionais.
* **Task 1.2:** [TASK-02] Estruturar as Features funcionais no Azure Boards alinhadas ao escopo de cada matéria. *(Activity: Documentation, Est: 2.5h)*
  * *Descrição:* Cadastrar e organizar as Features filhas dos Épicos no Azure Boards com datas-alvo e descrições de objetivos.

---

#### 🔹 [PBI-02] Estruturação Product Backlog Items (PBIs) e Redação das Histórias de Usuário
* **Work Item Type:** `Product Backlog Item`
* **Parent Feature:** `[FEATURE 01] Planejamento, Estruturação e Construção do Backlog Geral no Azure Boards`
* **State:** `Approved`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `3`
* **Tags:** `Sprint3, Compliance, UserStories, Scrum, AzureBoards, Requirements`

##### Descrição (História de Usuário)
> **Como** Scrum Master e Coordenador de Requisitos,  
> **Eu quero** decompor as Features em Product Backlog Items granulares e redigir Histórias de Usuário na narrativa canônica formal,  
> **Para que** cada desenvolvedor compreenda com exatidão o papel do usuário, a ação esperada e a justificativa de valor de cada funcionalidade desenvolvida.

##### Critérios de Aceite (Acceptance Criteria / Definition of Done)
- [ ] 100% dos PBIs documentados na estrutura canônica formal: `Como... Eu quero... Para que...`.
- [ ] Ausência de descrições vagas ou puramente técnicas no campo de Histórias de Usuário (`System.Description`).
- [ ] PBIs vinculados diretamente às Features correspondentes no Azure Boards.
- [ ] Histórias revisadas e aprovadas pelos responsáveis de cada frente técnica do time.

##### Tarefas Técnicas (Child Tasks)
* **Task 2.1:** [TASK-03] Redigir Histórias de Usuário no padrão canônico (Como/Quero/Para que) para todas as matérias. *(Activity: Requirements, Est: 2.5h)*
  * *Descrição:* Formular as narrativas de valor do tutor, pet e administradores para orientar o desenvolvimento de cada PBI.
* **Task 2.2:** [TASK-04] Cadastrar e organizar os PBIs no backlog do Azure Boards vinculando-os às Features pai. *(Activity: Documentation, Est: 2.5h)*
  * *Descrição:* Inserir os PBIs na nuvem do Azure DevOps, isolando a descrição da história no campo System.Description.

---

#### 🔹 [PBI-03] Padronização dos Critérios de Aceite Multidisciplinar
* **Work Item Type:** `Product Backlog Item`
* **Parent Feature:** `[FEATURE 01] Planejamento, Estruturação e Construção do Backlog Geral no Azure Boards`
* **State:** `Approved`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `3`
* **Tags:** `Sprint3, Compliance, QA, AcceptanceCriteria, DefinitionOfDone, Quality`

##### Descrição (História de Usuário)
> **Como** Líder de Garantia da Qualidade (QA Lead) e Compliance,  
> **Eu quero** definir critérios de aceite objetivos e estabelecer a Definition of Done (DoD) padronizada para todas as entregas do projeto,  
> **Para que** os itens de trabalho possuam metas claras de homologação, prevenindo retrabalhos e assegurando alta conformidade com as rubricas da FIAP.

##### Critérios de Aceite (Acceptance Criteria / Definition of Done)
- [ ] Critérios de aceitação formulados em formato de checklist objetivo e testável em cada PBI.
- [ ] Definition of Done formalizada contemplando compilação sem erros, testes executados e ausência de mocks em produção.
- [ ] Critérios registrados no campo nativo `Microsoft.VSTS.Common.AcceptanceCriteria` no Azure Boards.
- [ ] Padrão de qualidade acordado e compartilhado entre todos os membros do grupo.

##### Tarefas Técnicas (Child Tasks)
* **Task 3.1:** [TASK-05] Definir checklists de critérios de aceitação objetivos e testáveis por item de trabalho. *(Activity: Requirements, Est: 2.5h)*
  * *Descrição:* Elaborar condições auditáveis de conclusão funcional para cada PBI das frentes de software.
* **Task 3.2:** [TASK-06] Formalizar os critérios de Definition of Done (DoD) e qualidade contínua para o time. *(Activity: Documentation, Est: 2.5h)*
  * *Descrição:* Documentar os padrões de entrega (Clean Code, boas práticas e validações) exigidos para fechamento de itens de trabalho.

---

### 🏆 [FEATURE 02] Priorização, Gestão de Dependências, Release Planning e Detalhamento da Sprint
* **Work Item Type:** `Feature`
* **Parent:** `[EPIC] Sprint 3 - Compliance, Quality Assurance & Tests: Governança Scrum, Gestão do Backlog e Asseguração da Qualidade`
* **Title:** `[FEATURE 02] Priorização, Gestão de Dependências, Release Planning e Detalhamento da Sprint`
* **Tags:** `Sprint3, Compliance, ReleasePlan, Estimation, Dependencies, TaskBreakdown`
* **Start Date:** `2026-09-02`
* **Target Date:** `2026-09-05`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `9`
* **Description:** Condução do dimensionamento de esforço em Story Points, classificação de prioridades de negócio, mapeamento das dependências técnicas cruzadas entre disciplinas e detalhamento das Tasks técnicas da Sprint atual com controle de horas.

#### 🔹 [PBI-04] Dimensionamento de Esforço em Story Points e Apontamento de Prioridades de Negócio
* **Work Item Type:** `Product Backlog Item`
* **Parent Feature:** `[FEATURE 02] Priorização, Gestão de Dependências, Release Planning e Detalhamento da Sprint`
* **State:** `Approved`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `3`
* **Tags:** `Sprint3, Compliance, Estimation, StoryPoints, Priority, PlanningPoker`

##### Descrição (História de Usuário)
> **Como** Scrum Master e Product Owner,  
> **Eu quero** pontuar o esforço dos itens de backlog utilizando a escala Fibonacci e classificar as prioridades de negócio,  
> **Para que** o time possua clareza de capacidade produtiva, foco nas entregas de maior valor agregado e previsibilidade de cronograma.

##### Critérios de Aceite (Acceptance Criteria / Definition of Done)
- [ ] Pontuações de esforço atribuídas a todos os PBIs com base em complexidade e incerteza técnica.
- [ ] Prioridades normalizadas de 1 (Critical) a 4 (Low) com valor de negócio correspondente no Azure Boards.
- [ ] Backlog reordenado na sequência ótima de desenvolvimento e homologação.
- [ ] Consenso do grupo sobre as estimativas alcançado em dinâmicas de refinamento.

##### Tarefas Técnicas (Child Tasks)
* **Task 4.1:** [TASK-07] Conduzir sessões de Planning Poker para estimativa de Story Points dos PBIs do projeto. *(Activity: Requirements, Est: 2.5h)*
  * *Descrição:* Reunir o time para calibrar o esforço relativo dos itens de backlog utilizando a sequência Fibonacci.
* **Task 4.2:** [TASK-08] Classificar prioridades de negócio (1 - Critical a 4 - Low) e ordenar o backlog para entrega. *(Activity: Documentation, Est: 2.5h)*
  * *Descrição:* Ajustar os campos Priority e Business Value nos itens de trabalho no Azure Boards garantindo ordenação lógica.

---

#### 🔹 [PBI-05] Mapeamento da Matriz de Dependências Técnicas Cruzadas entre as Frentes
* **Work Item Type:** `Product Backlog Item`
* **Parent Feature:** `[FEATURE 02] Priorização, Gestão de Dependências, Release Planning e Detalhamento da Sprint`
* **State:** `Approved`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `3`
* **Tags:** `Sprint3, Compliance, Dependencies, Architecture, CrossDiscipline`

##### Descrição (História de Usuário)
> **Como** Arquiteto de Software e QA Lead,  
> **Eu quero** mapear exaustivamente as dependências técnicas cruzadas e os contratos de interface entre todas as frentes do projeto,  
> **Para que** sejam mitigados riscos de impedimentos, bloqueios de pipeline e incompatibilidades de esquemas entre banco, APIs e mobile.

##### Critérios de Aceite (Acceptance Criteria / Definition of Done)
- [ ] Matriz de dependências documentada cobrindo fluxos de dados do Banco Oracle para APIs Java, .NET e IA.
- [ ] Contratos de autenticação JWT e rotas REST validados entre backend e o aplicativo Mobile.
- [ ] Dependências de empacotamento Docker e esteira Azure CLI alinhadas com o código-fonte da aplicação.
- [ ] Relações de precedência comunicadas a todos os integrantes do grupo.

##### Tarefas Técnicas (Child Tasks)
* **Task 5.1:** [TASK-09] Mapear acoplamentos e contratos de dados entre Banco de Dados, APIs Backend e Frontend Mobile. *(Activity: Requirements, Est: 2.5h)*
  * *Descrição:* Levantar o modelo de dados 3FN e as rotas REST para documentar onde cada disciplina depende da entrega de outra.
* **Task 5.2:** [TASK-10] Documentar a matriz de dependências técnicas cruzadas para mitigar riscos de bloqueio. *(Activity: Documentation, Est: 2.5h)*
  * *Descrição:* Registrar a matriz comparativa e diagramas de fluxo de dados compartilhados no repositório do projeto.

---

#### 🔹 [PBI-06] Estruturação do Release Plan da Sprint 3 e Detalhamento das Tarefas Técnicas em Horas
* **Work Item Type:** `Product Backlog Item`
* **Parent Feature:** `[FEATURE 02] Priorização, Gestão de Dependências, Release Planning e Detalhamento da Sprint`
* **State:** `Approved`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `3`
* **Tags:** `Sprint3, Compliance, ReleasePlan, TaskBreakdown, HoursEstimation, SprintPlanning`

##### Descrição (História de Usuário)
> **Como** Scrum Master e Coordenador de Entregas,  
> **Eu quero** estruturar o Release Plan da Sprint 3 balanceando Story Points entre Semana 1 e Semana 2 e decompor os PBIs em Tarefas filhas com estimativas em horas,  
> **Para que** a equipe trabalhe com ritmo sustentável, metas intermediárias claras e visibilidade do esforço residual diário no Taskboard.

##### Critérios de Aceite (Acceptance Criteria / Definition of Done)
- [ ] Release Plan estruturado com divisão entre Semana 1 (64 SP / 180.0h) e Semana 2 (54 SP / 182.0h).
- [ ] Decomposição em Tarefas técnicas filhas contendo horas estimadas (`Remaining Work`) realistas (2.5h por tarefa).
- [ ] Tipos de atividade normalizados (`Requirements`, `Development`, `Documentation`).
- [ ] Itens alocados nos respectivos Iteration Paths no Azure DevOps.

##### Tarefas Técnicas (Child Tasks)
* **Task 6.1:** [TASK-11] Elaborar o cronograma de entregas balanceado entre Semana 1 e Semana 2 da Sprint 3. *(Activity: Requirements, Est: 2.5h)*
  * *Descrição:* Planejar o cronograma executivo de marcos para garantir a conclusão de arquitetura na Semana 1 e cloud/IA na Semana 2.
* **Task 6.2:** [TASK-12] Decompor os PBIs da disciplina em Tarefas filhas com estimativas em horas e tipos de atividade. *(Activity: Documentation, Est: 2.5h)*
  * *Descrição:* Especificar e vincular as 12 tarefas técnicas aos seus respectivos PBIs no Azure Boards preenchendo horas e atividades.

---

## 🌐 8. Acesso ao Azure Boards na Nuvem & Governança de Acesso do Professor

### 🔗 Link Direto de Acesso ao Azure DevOps
* **URL Oficial da Organização e Projeto:**  
  👉 [https://dev.azure.com/PetGuardian/Pet-Guardian-Sprint-3](https://dev.azure.com/PetGuardian/Pet-Guardian-Sprint-3)

---

### 🛡️ Passo a Passo para Cadastro do Professor como Administrador do Projeto

Conforme exigência mandatória do edital da disciplina (*"Garanta que o professor esteja cadastrado como membro da organização e administrador do projeto"*), o procedimento de concessão de permissões é realizado no painel administrativo do Azure DevOps:

#### Passo 1: Adicionar o Professor como Usuário da Organização
1. Acesse o Azure DevOps na URL: `https://dev.azure.com/PetGuardian/`.
2. No canto inferior esquerdo da tela, clique em **Organization Settings** (ícone de engrenagem ⚙️).
3. No menu lateral esquerdo, sob a seção **General**, selecione **Users**.
4. Clique no botão azul **Add users** no canto superior direito.
5. Digite o endereço de e-mail institucional do professor da FIAP.
6. Em **Access level**, selecione **Basic** (ou *Stakeholder/Visual Studio Subscriber*, conforme a licença institucional).
7. Em **Add to projects**, marque o projeto `Pet-Guardian-Sprint-3`.
8. Clique em **Add** para confirmar o convite e a inclusão.

#### Passo 2: Conceder Privilégios de Administrador do Projeto (`Project Administrator`)
1. Acesse o projeto: `https://dev.azure.com/PetGuardian/Pet-Guardian-Sprint-3`.
2. No canto inferior esquerdo, clique em **Project Settings** (⚙️).
3. No menu lateral, sob a seção **General**, selecione **Permissions**.
4. Na aba **Groups**, localize e clique no grupo **Project Administrators**.
5. Clique na aba **Members** no painel central.
6. Clique no botão **Add** e busque pelo nome ou e-mail do professor recém-adicionado.
7. Selecione o usuário do professor e clique em **Save**.
8. ✅ O professor agora possui acesso total de leitura, edição, gestão de Sprints, iterações e auditoria de todos os Work Items do projeto.

---

### 🧭 Navegação Recomendada no Azure Boards para a Banca Avaliadora

Para visualizar a rastreabilidade ponta a ponta implementada pela equipe:

1. **Visualização em Árvore Hierárquica:**
   - Acesse `Boards > Backlogs`.
   - No seletor de nível no canto superior direito, escolha **Epics** ou **Features**.
   - No botão de opções de visualização (ícone de engrenagem/colunas), ative **Parents: On**.
   - A visualização exibirá a árvore de decomposição completa: `Epic ➔ Feature ➔ Product Backlog Item ➔ Task`.

2. **Visualização por Sprints / Iterações:**
   - Acesse `Boards > Sprints`.
   - No menu seletor de Iteração, alterne entre:
     - `Pet-Guardian-Sprint-3\Release 1 - Sprint 3\Semana 1` (Mobile, Java, Database);
     - `Pet-Guardian-Sprint-3\Release 1 - Sprint 3\Semana 2` (.NET, DevOps, IA, Compliance).
   - Visualize o Taskboard com raias (Swimlanes) organizadas por PBI e acompanhe o `Remaining Work` das Tasks.

3. **Filtro por Disciplina (Tags):**
   - Utilize a barra de filtros (`Filter` - ícone de funil) e selecione a Tag correspondente:
     - `Mobile` | `JavaAdvanced` | `Database` | `DotNet` | `DevOps` | `DisruptiveArchitectures` | `Compliance`.
