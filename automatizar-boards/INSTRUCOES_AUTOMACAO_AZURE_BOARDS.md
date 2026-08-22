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
AZURE_DEVOPS_PAT=SEU_TOKEN_AQUI
```

> ⚠️ **Nota de Autenticação:**  
> O script usa **HTTP Basic Auth** (`:PAT` codificado em Base64).  
> Se o PAT estiver em branco, o script tentará automaticamente extrair o Bearer Token da sessão ativa do Azure CLI (`az account get-access-token`).

---

## 🚨 3. Regras de Negócio e Diretrizes Estritas (NÃO QUEBRAR)

Ao manipular ou estender o parser/sincronizador, qualquer IA **deve respeitar rigorosamente** as seguintes regras:

1. **🚫 PROIBIDO Emojis / Ícones em Títulos:**
   - Todo título de Epic, Feature, PBI e Task deve passar pela função `clean_title(text)`.
   - Emojis (ex: 👑, 🏆, 🔹, 🧹, 🩺, 🗄️, ☁️, 🤖, 📱, etc.) e crases **devem ser 100% removidos**.
2. **🚫 PROIBIDO Envio de Tags Automáticas (`System.Tags`):**
   - O campo `System.Tags` **NÃO deve ser enviado** (deve permanecer `None`/vazio), pois o usuário define as tags manualmente no portal.
3. **📄 Separação Estrita de Campos no Azure DevOps:**
   - **`System.Description`**: Contém **estritamente a História de Usuário** (`<div><strong>Como</strong>...<br/><strong>Eu quero</strong>...<br/><strong>Para que</strong>...</div>`).
     - **NUNCA** adicionar barras laterais azuis (`<blockquote>`).
     - **NUNCA** adicionar títulos redundantes como `<h3>História de Usuário</h3>`.
     - Usar tags `<div>` e `<br/>` para evitar espaçamento vertical excessivo entre linhas.
   - **`Microsoft.VSTS.Common.AcceptanceCriteria`**: Deve ser enviado no **campo próprio nativo**, contendo apenas a lista `<ul><li>...</li></ul>` sem títulos extras.
4. **🚫 ZERO Textos Sintéticos / Inventados:**
   - **NUNCA** inventar frases automáticas como *"Critérios para conclusão e homologação da Feature:"*.
   - Se o Markdown não tiver Acceptance Criteria para Epic ou Feature, o campo deve ser enviado vazio (`None`).
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

## 📁 4. Estrutura dos Arquivos do Módulo

Diretório: `Compliance-Quality-Assurance-Tests/automatizar-boards/`

| Arquivo | Descrição |
| :--- | :--- |
| [`parser_backlog.py`](file:///c:/Users/Enzo/new_backup/FIAP/_Projetos/Challenge%20Clyvo%203/Compliance-Quality-Assurance-Tests/automatizar-boards/parser_backlog.py) | Parser robusto em Python. Lê os arquivos `.md`, extrai nós hierárquicos, remove ícones com `clean_title()`, calcula esforços e formata HTML limpo. |
| [`azure_boards_sync.py`](file:///c:/Users/Enzo/new_backup/FIAP/_Projetos/Challenge%20Clyvo%203/Compliance-Quality-Assurance-Tests/automatizar-boards/azure_boards_sync.py) | Cliente REST API do Azure DevOps (`_apis/wit/workitems`). Faz chamadas JSON Patch e cria os vínculos `Hierarchy-Reverse`. |
| [`run_sync.py`](file:///c:/Users/Enzo/new_backup/FIAP/_Projetos/Challenge%20Clyvo%203/Compliance-Quality-Assurance-Tests/automatizar-boards/run_sync.py) | CLI com suporte aos parâmetros `--file`, `--all`, `--dry-run`, `--check-auth`, `--org`, `--project`, `--pat`. |
| [`teste_backlog_exemplo.md`](file:///c:/Users/Enzo/new_backup/FIAP/_Projetos/Challenge%20Clyvo%203/Compliance-Quality-Assurance-Tests/automatizar-boards/teste_backlog_exemplo.md) | Backlog piloto seguro com 1 Epic, 1 Feature, 2 PBIs e 2 Tasks para validações rápidas. |
| [`.env`](file:///c:/Users/Enzo/new_backup/FIAP/_Projetos/Challenge%20Clyvo%203/Compliance-Quality-Assurance-Tests/automatizar-boards/.env) | Credenciais ativas da organização `PetGuardian`. |

---

## 🗺️ 5. Mapeamento das 6 Disciplinas do Projeto

Os arquivos de backlog de cada matéria estão localizados nos seguintes caminhos relativos:

```python
ALL_DISCIPLINE_FILES = [
    ("../../Mobile-Application-Development/BACKLOG_MOBILE.md", "Mobile Application Development"),
    ("../../Java-Advanced/BACKLOG_JAVA_ADVANCED.md", "Java Advanced"),
    ("../../Advanced-Business-Development-with-Dot-Net/BACKLOG_DOT_NET.md", ".NET & Observabilidade"),
    ("../../Database-Advanced/BACKLOG_DATABASE_ADVANCED.md", "Database Advanced"),
    ("../../DevOps-Tools-Cloud-Computing/BACKLOG_DEVOPS.md", "DevOps Tools & Cloud"),
    ("../../Disruptive-Architectures-IoT-IoB-IA/BACKLOG_DISRUPTIVE_ARCHITECTURES.md", "Disruptive Architectures (IA/IoT)")
]
```

---

## 💻 6. Comandos de Execução (Powershell / Windows)

> 💡 **Nota sobre o Interpretador Python:**  
> No ambiente Windows desta máquina, o Python pode ser executado via `python` ou diretamente pelo binário:  
> `& "C:\Program Files\Microsoft SDKs\Azure\CLI2\python.exe"`

### A. Testar Autenticação e Conexão:
```powershell
python run_sync.py --check-auth
```

### B. Simulação Segura (Dry Run - Não cria nada no Azure):
```powershell
# Simular arquivo de teste:
python run_sync.py --file teste_backlog_exemplo.md --dry-run

# Simular todas as 6 matérias:
python run_sync.py --all --dry-run
```

### C. Importar Disciplina Específica:
```powershell
# Exemplo: Importar Mobile
python run_sync.py --file ../../Mobile-Application-Development/BACKLOG_MOBILE.md

# Exemplo: Importar Java Advanced
python run_sync.py --file ../../Java-Advanced/BACKLOG_JAVA_ADVANCED.md

# Exemplo: Importar .NET
python run_sync.py --file ../../Advanced-Business-Development-with-Dot-Net/BACKLOG_DOT_NET.md

# Exemplo: Importar Database Oracle
python run_sync.py --file ../../Database-Advanced/BACKLOG_DATABASE_ADVANCED.md

# Exemplo: Importar DevOps
python run_sync.py --file ../../DevOps-Tools-Cloud-Computing/BACKLOG_DEVOPS.md

# Exemplo: Importar Disruptive IA/IoT
python run_sync.py --file ../../Disruptive-Architectures-IoT-IoB-IA/BACKLOG_DISRUPTIVE_ARCHITECTURES.md
```

### D. Importação em Lote de Todas as Matérias:
```powershell
python run_sync.py --all
```

---

## 🧹 7. Script de Limpeza de Itens de Teste (Cheat Sheet)

Se precisar deletar work items por ID via terminal:

```python
import base64, json, urllib.request

pat = "SEU_PAT"
auth = base64.b64encode(f":{pat}".encode()).decode()
headers = {"Authorization": f"Basic {auth}"}

# Exemplo para deletar lista de IDs
ids_para_deletar = [80, 81, 82]
for item_id in ids_para_deletar:
  url = f"https://dev.azure.com/PetGuardian/Pet-Guardian-Sprint-3/_apis/wit/workitems/{item_id}?destroy=true&api-version=7.0"
  req = urllib.request.Request(url, headers=headers, method="DELETE")
  with urllib.request.urlopen(req) as resp:
    print(f"Deletado #{item_id}: {resp.status}")
```
