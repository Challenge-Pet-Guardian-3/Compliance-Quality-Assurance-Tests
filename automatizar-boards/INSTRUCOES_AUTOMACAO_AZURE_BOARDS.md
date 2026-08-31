# 🤖 Guia Técnico para Agentes de IA: Automação do Azure Boards

> **Documento de Governança e Operação Técnica**  
> **Objetivo:** Orientar qualquer agente de IA ou desenvolvedor sobre a arquitetura, regras de negócio e execução dos scripts de sincronização de Backlog Markdown (`.md`) para o **Azure DevOps / Azure Boards** do projeto PetGuardian.

---

## 🎯 1. Visão Geral e Objetivo

Este ecossistema automatiza a leitura e o parsing dos arquivos de Backlog em Markdown das 6 disciplinas do Challenge Sprint 3 e cria a estrutura hierárquica nativa no Azure Boards seguindo o **Processo Scrum**:

$$\text{Epic} \xrightarrow{\text{Hierarchy-Reverse}} \text{Feature} \xrightarrow{\text{Hierarchy-Reverse}} \text{Product Backlog Item (PBI)} \xrightarrow{\text{Hierarchy-Reverse}} \text{Task}$$

---

## 🏛️ 2. Configurações de Ambiente (`.env`)

Localização do arquivo: [`Compliance-Quality-Assurance-Tests/automatizar-boards/.env`](file:///c:/Users/Enzo/new_backup/FIAP/_Projetos/Challenge%20Clyvo%203/Compliance-Quality-Assurance-Tests/automatizar-boards/.env)

```ini
# Organização e Projeto no Azure DevOps
AZURE_DEVOPS_ORG=PetGuardian
AZURE_DEVOPS_PROJECT=Pet-Guardian-Sprint-3

# Personal Access Token (PAT) com escopo "Work Items (Read & Write)"
AZURE_DEVOPS_PAT=
```

> ⚠️ **Nota de Autenticação:**  
> O script usa **HTTP Basic Auth** (`:PAT` codificado em Base64).  
> Se o PAT estiver em branco, o script tentará automaticamente extrair o Bearer Token da sessão ativa do Azure CLI (`az account get-access-token`).

---

## 📅 3. Mapeamento Oficial de Iteration Paths (Sprints / Semanas)

No Azure Boards, cada disciplina está vinculada a uma iteração específica da Sprint 3:

| Disciplina | Tag no Azure Boards | Iteration Path Alvo | Período Oficial |
| :--- | :--- | :--- | :---: |
| 📱 **Mobile Application Development** | `Mobile` | `Pet-Guardian-Sprint-3\Release 1 - Sprint 3\Semana 1` | 2026-08-23 a 2026-08-29 |
| ☕ **Java Advanced** | `JavaAdvanced` | `Pet-Guardian-Sprint-3\Release 1 - Sprint 3\Semana 1` | 2026-08-23 a 2026-08-29 |
| 🗄️ **Database Advanced** | `Database` | `Pet-Guardian-Sprint-3\Release 1 - Sprint 3\Semana 1` | 2026-08-23 a 2026-08-29 |
| ☁️ **DevOps Tools & Cloud Computing** | `DevOps` | `Pet-Guardian-Sprint-3\Release 1 - Sprint 3\Semana 2` | 2026-08-30 a 2026-09-05 |
| 🤖 **Disruptive Architectures (IoT/IA)** | `DisruptiveArchitectures` | `Pet-Guardian-Sprint-3\Release 1 - Sprint 3\Semana 2` | 2026-08-30 a 2026-09-05 |
| 💻 **.NET & Observabilidade** | `DotNet` | `Pet-Guardian-Sprint-3\Release 1 - Sprint 3\Semana 2` | 2026-08-30 a 2026-09-05 |

---

## 🚨 4. Regras de Negócio e Diretrizes Estritas (NÃO QUEBRAR)

Ao manipular ou estender o parser/sincronizador, qualquer IA **deve respeitar rigorosamente** as seguintes regras:

1. **🚫 PROIBIDO Emojis / Ícones em Títulos:**
   - Todo título de Epic, Feature, PBI e Task deve passar pela função `clean_title(text)`.
   - Emojis (ex: 👑, 🏆, 🔹, 🧹, 🩺, 🗄️, ☁️, 🤖, 📱, etc.) e crases **devem ser 100% removidos**.
2. **🏷️ Uma Única Tag Padronizada por Disciplina (`System.Tags`):**
   - Cada item de trabalho recebe estritamente a tag correspondente (`Mobile`, `JavaAdvanced`, `DotNet`, `Database`, `DevOps`, `DisruptiveArchitectures`).
3. **📅 Atribuição Automática de IterationPath (`System.IterationPath`):**
   - O `azure_boards_sync.py` injeta o caminho da `Semana 1` ou `Semana 2` automaticamente em todos os níveis (Epic, Feature, PBI, Task).
4. **📄 Separação Estrita de Campos no Azure DevOps:**
   - **`System.Description`**: Contém **estritamente a História de Usuário** (`<div><strong>Como</strong>...<br/><strong>Eu quero</strong>...<br/><strong>Para que</strong>...</div>`).
     - **NUNCA** adicionar barras laterais azuis (`<blockquote>`).
     - **NUNCA** adicionar títulos redundantes como `<h3>História de Usuário</h3>`.
     - Usar tags `<div>` e `<br/>` para evitar espaçamento vertical excessivo entre linhas.
   - **`Microsoft.VSTS.Common.AcceptanceCriteria`**: Deve ser enviado no **campo próprio nativo**, contendo apenas a lista `<ul><li>...</li></ul>` sem títulos extras.
5. **📊 Mapeamento de Métricas Scrum:**
   - **`Microsoft.VSTS.Scheduling.Effort`**:
     - No **PBI**: valor numérico exato do Story Points (ex: `5.0`).
     - Na **Feature**: soma automática do `Effort` de todos os PBIs filhos.
     - No **Epic**: soma automática de todo o `Effort` da disciplina.
   - **`Microsoft.VSTS.Common.BusinessValue`**:
     - Prioridade 1 (Critical) ➔ `100`
     - Prioridade 2 (High) ➔ `80`
     - Prioridade 3 (Medium) ➔ `50`
   - **`Microsoft.VSTS.Common.Priority`**: Número inteiro de 1 a 4.
   - **`Microsoft.VSTS.Common.ValueArea`**: `"Business"`.

---

## 📁 5. Estrutura dos Arquivos do Módulo

Diretório: `Compliance-Quality-Assurance-Tests/automatizar-boards/`

| Arquivo | Descrição |
| :--- | :--- |
| [`parser_backlog.py`](file:///c:/Users/Enzo/new_backup/FIAP/_Projetos/Challenge%20Clyvo%203/Compliance-Quality-Assurance-Tests/automatizar-boards/parser_backlog.py) | Parser robusto em Python. Lê os arquivos `.md`, extrai nós hierárquicos, remove ícones com `clean_title()`, calcula esforços e formata HTML limpo. |
| [`azure_boards_sync.py`](file:///c:/Users/Enzo/new_backup/FIAP/_Projetos/Challenge%20Clyvo%203/Compliance-Quality-Assurance-Tests/automatizar-boards/azure_boards_sync.py) | Cliente REST API do Azure DevOps (`_apis/wit/workitems`). Cria work items com IterationPath automático e vínculos `Hierarchy-Reverse`. |
| [`run_sync.py`](file:///c:/Users/Enzo/new_backup/FIAP/_Projetos/Challenge%20Clyvo%203/Compliance-Quality-Assurance-Tests/automatizar-boards/run_sync.py) | CLI com suporte aos parâmetros `--file`, `--all`, `--dry-run`, `--check-auth`, `--org`, `--project`, `--pat`. |
| [`update_azure_descriptions.py`](file:///c:/Users/Enzo/new_backup/FIAP/_Projetos/Challenge%20Clyvo%203/Compliance-Quality-Assurance-Tests/automatizar-boards/update_azure_descriptions.py) | Utilitário CLI para sincronizar e preencher o `System.Description` de todos os 6 Épicos e 30 Features no Azure Boards. |
| [`update_azure_iterations.py`](file:///c:/Users/Enzo/new_backup/FIAP/_Projetos/Challenge%20Clyvo%203/Compliance-Quality-Assurance-Tests/automatizar-boards/update_azure_iterations.py) | Utilitário CLI para auditar e sincronizar em lote os `IterationPath` de todos os 282 Work Items existentes no Azure Boards. |
| [`update_azure_epics.py`](file:///c:/Users/Enzo/new_backup/FIAP/_Projetos/Challenge%20Clyvo%203/Compliance-Quality-Assurance-Tests/automatizar-boards/update_azure_epics.py) | Utilitário CLI para atualizar e padronizar os títulos dos 6 Épicos oficiais no Azure Boards. |
| [`verify_epics.py`](file:///c:/Users/Enzo/new_backup/FIAP/_Projetos/Challenge%20Clyvo%203/Compliance-Quality-Assurance-Tests/automatizar-boards/verify_epics.py) | Auditor de Story Points consolidados dos Épicos na nuvem. |
| [`.env`](file:///c:/Users/Enzo/new_backup/FIAP/_Projetos/Challenge%20Clyvo%203/Compliance-Quality-Assurance-Tests/automatizar-boards/.env) | Credenciais ativas da organização `PetGuardian`. |

---

## 💻 6. Comandos de Execução (PowerShell / Windows)

> 💡 **Nota sobre o Interpretador Python:**  
> No ambiente Windows, utilize o Python do Azure CLI caso o `python` não esteja no PATH global:  
> `& "C:\Program Files\Microsoft SDKs\Azure\CLI2\python.exe" <script.py>`

### A. Testar Autenticação e Conexão:
```powershell
python run_sync.py --check-auth
```

### B. Simulação Segura (Dry Run - Não cria nada no Azure):
```powershell
python run_sync.py --all --dry-run
```

### C. Importar Disciplina Específica:
```powershell
# Mobile (Semana 1)
python run_sync.py --file ../../Mobile-Application-Development/BACKLOG_MOBILE.md

# Java Advanced (Semana 1)
python run_sync.py --file ../../Java-Advanced/BACKLOG_JAVA_ADVANCED.md

# .NET & Observabilidade (Semana 2)
python run_sync.py --file ../../Advanced-Business-Development-with-Dot-Net/BACKLOG_DOT_NET.md

# Database Advanced (Semana 1)
python run_sync.py --file ../../Database-Advanced/BACKLOG_DATABASE_ADVANCED.md

# DevOps Tools & Cloud (Semana 2)
python run_sync.py --file ../../DevOps-Tools-Cloud-Computing/BACKLOG_DEVOPS.md

# Disruptive Architectures (Semana 2)
python run_sync.py --file ../../Disruptive-Architectures-IoT-IoB-IA/BACKLOG_DISRUPTIVE_ARCHITECTURES.md
```

### D. Importação em Lote de Todas as Matérias:
```powershell
python run_sync.py --all
```

### E. Sincronizar e Auditar Iteration Paths no Azure Boards:
```powershell
# Auditar / Simular:
python update_azure_iterations.py --dry-run

# Executar sincronização de Iterations na nuvem:
python update_azure_iterations.py
```

### F. Sincronizar Descrições de Épicos e Features:
```powershell
# Simular:
python update_azure_descriptions.py --dry-run

# Executar atualização das descrições na nuvem:
python update_azure_descriptions.py
```
