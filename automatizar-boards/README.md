# 🚀 Automação de Backlog para o Azure Boards (Python)

Este módulo automatiza a leitura dos arquivos de Backlog em Markdown (`.md`) de todas as disciplinas da Sprint 3 (Challenge Clyvo 2026) e cria a estrutura hierárquica completa no **Azure Boards** seguindo o processo **Scrum**:

```
👑 Epic
│
└── 🏆 Feature (vinculada ao Epic via System.LinkTypes.Hierarchy-Reverse)
    │
    └── 📄 Product Backlog Item (PBI com Story Points, Prioridade, Tags e HTML)
        │
        └── 🔨 Task (Tarefas técnicas filhas vinculadas ao PBI)
```

---

## 🎯 Destaques do Automatizador

1. **Remoção Automática de Ícones/Emojis:** Títulos de Epics, Features, PBIs e Tasks são higienizados para o padrão profissional do Azure DevOps (`clean_title`).
2. **Campos Oficiais Mapeados:**
   - `System.Title`: Título limpo sem emojis.
   - `System.Description`: História de Usuário limpa em bloco `<div>` com `<br/>`, sem barras azuis e sem títulos redundantes.
   - `Microsoft.VSTS.Common.AcceptanceCriteria`: Critérios de aceite enviados no **campo próprio dedicado**.
   - `Microsoft.VSTS.Scheduling.Effort`: Story points numéricos calculados em todos os níveis.
   - `Microsoft.VSTS.Common.BusinessValue`: Valor de negócio mapeado pela prioridade.
   - `Microsoft.VSTS.Common.Priority`: Prioridade numérica de 1 (Crítica) a 4 (Baixa).
   - `System.Tags`: **Desativado** (nenhuma tag é enviada automaticamente, permitindo definição manual).
3. **Vínculos Hierárquicos Reais:** Criação dos links pai/filho nativos do Azure Boards (`System.LinkTypes.Hierarchy-Reverse`).
4. **Zero Dependências Obrigatórias:** Executa usando a biblioteca padrão do Python (`urllib.request`), funcionando direto no ambiente com `Python 3.8+` ou com o Python nativo do Azure CLI.
5. 📖 **Guia Completo para IAs:** Consulte [`INSTRUCOES_AUTOMACAO_AZURE_BOARDS.md`](file:///c:/Users/Enzo/new_backup/FIAP/_Projetos/Challenge%20Clyvo%203/Compliance-Quality-Assurance-Tests/automatizar-boards/INSTRUCOES_AUTOMACAO_AZURE_BOARDS.md) para detalhes arquiteturais e de governança.


---

## ⚙️ Configuração

1. Abra o arquivo [`.env`](file:///.env) e configure as credenciais:
```ini
AZURE_DEVOPS_ORG=PetGuardian
AZURE_DEVOPS_PROJECT=Pet-Guardian-Sprint-3
AZURE_DEVOPS_PAT=seu_personal_access_token_aqui
```

### 🔑 Como gerar o Personal Access Token (PAT) no Azure DevOps:
1. Acesse: `https://dev.azure.com/PetGuardian`
2. No canto superior direito, clique no **ícone de engrenagem / perfil de usuário** ➔ **Personal access tokens**.
3. Clique em **+ New Token**.
4. Defina o nome (ex: `Script-Boards-Sprint3`).
5. Em **Scopes**, selecione **Custom defined** ➔ **Work Items** ➔ Marque **Read & Write**.
6. Clique em **Create** e copie o token gerado para a variável `AZURE_DEVOPS_PAT=` no seu arquivo `.env`.

---

## 💻 Comandos de Execução

Abra o terminal dentro da pasta `Compliance-Quality-Assurance-Tests/automatizar-boards`:

### 1. Testar Conexão com o Azure DevOps:
```powershell
python run_sync.py --check-auth
```

### 2. Simulação Segura do Arquivo Piloto de Teste (Dry Run):
```powershell
python run_sync.py --file teste_backlog_exemplo.md --dry-run
```

### 3. Criar Itens do Arquivo Piloto de Teste no Azure Boards:
```powershell
python run_sync.py --file teste_backlog_exemplo.md
```

### 4. Importar uma Matéria Específica:
```powershell
# Mobile:
python run_sync.py --file ../../Mobile-Application-Development/BACKLOG_MOBILE.md

# Java Advanced:
python run_sync.py --file ../../Java-Advanced/BACKLOG_JAVA_ADVANCED.md

# .NET & Observabilidade:
python run_sync.py --file ../../Advanced-Business-Development-with-Dot-Net/BACKLOG_DOT_NET.md

# Database Advanced:
python run_sync.py --file ../../Database-Advanced/BACKLOG_DATABASE_ADVANCED.md

# DevOps Tools & Cloud:
python run_sync.py --file ../../DevOps-Tools-Cloud-Computing/BACKLOG_DEVOPS.md

# Disruptive Architectures (IA/IoT):
python run_sync.py --file ../../Disruptive-Architectures-IoT-IoB-IA/BACKLOG_DISRUPTIVE_ARCHITECTURES.md
```

### 5. Importar Todas as 6 Matérias de Uma Vez (Batch Carga Completa):
```powershell
python run_sync.py --all
```
