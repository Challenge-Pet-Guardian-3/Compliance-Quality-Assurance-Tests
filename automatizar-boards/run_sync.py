import sys
import os
import argparse
from typing import List

# Garante suporte a UTF-8 no terminal Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Adiciona diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parser_backlog import parse_backlog_markdown
from azure_boards_sync import AzureBoardsClient


def load_env_file(env_path: str = ".env") -> dict:
    """Lê arquivo .env simples sem depender de bibliotecas externas."""
    env_vars = {}
    if not os.path.exists(env_path):
        return env_vars
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env_vars[k.strip()] = v.strip().strip("'").strip('"')
    return env_vars


ALL_DISCIPLINE_FILES = [
    ("../../Mobile-Application-Development/BACKLOG_MOBILE.md", "Mobile Application Development"),
    ("../../Java-Advanced/BACKLOG_JAVA_ADVANCED.md", "Java Advanced"),
    ("../../Advanced-Business-Development-with-Dot-Net/BACKLOG_DOT_NET.md", ".NET & Observabilidade"),
    ("../../Database-Advanced/BACKLOG_DATABASE_ADVANCED.md", "Database Advanced"),
    ("../../DevOps-Tools-Cloud-Computing/BACKLOG_DEVOPS.md", "DevOps Tools & Cloud"),
    ("../../Disruptive-Architectures-IoT-IoB-IA/BACKLOG_DISRUPTIVE_ARCHITECTURES.md", "Disruptive Architectures (IA/IoT)"),
    ("../BACKLOG_COMPLIANCE.md", "Compliance, Quality Assurance & Tests")
]


def main():
    parser = argparse.ArgumentParser(
        description="Automação de Importação de Backlog para o Azure Boards (Scrum Process: Epic -> Feature -> PBI -> Task)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  1. Testar conexão com Azure DevOps:
     python run_sync.py --check-auth

  2. Simular importação do arquivo de teste piloto (sem criar nada na nuvem):
     python run_sync.py --file teste_backlog_exemplo.md --dry-run

  3. Importar arquivo de teste piloto no Azure Boards:
     python run_sync.py --file teste_backlog_exemplo.md

  4. Importar uma matéria específica:
     python run_sync.py --file ../../Mobile-Application-Development/BACKLOG_MOBILE.md
     python run_sync.py --file ../BACKLOG_COMPLIANCE.md

  5. Importar todas as matérias de uma vez no Board unificado:
     python run_sync.py --all
        """
    )

    parser.add_argument("--file", "-f", type=str, default="teste_backlog_exemplo.md", help="Caminho do arquivo .md a importar (Padrão: teste_backlog_exemplo.md)")
    parser.add_argument("--all", "-a", action="store_true", help="Importar backlogs de todas as 7 disciplinas do Challenge Sprint 3")
    parser.add_argument("--dry-run", "-d", action="store_true", help="Modo simulação: executa o parser e exibe a hierarquia sem criar work items na nuvem")
    parser.add_argument("--check-auth", "-c", action="store_true", help="Valida se as credenciais e o projeto do Azure DevOps estão acessíveis")
    parser.add_argument("--org", type=str, default=None, help="Nome da organização Azure DevOps (Ex: PetGuardian)")
    parser.add_argument("--project", type=str, default=None, help="Nome do projeto Azure DevOps (Ex: Pet-Guardian-Sprint-3)")
    parser.add_argument("--pat", type=str, default=None, help="Personal Access Token (PAT) do Azure DevOps")

    args = parser.parse_args()

    # Carrega variáveis do arquivo .env se existirem
    env_vars = load_env_file()
    org = args.org or os.getenv("AZURE_DEVOPS_ORG") or env_vars.get("AZURE_DEVOPS_ORG", "PetGuardian")
    project = args.project or os.getenv("AZURE_DEVOPS_PROJECT") or env_vars.get("AZURE_DEVOPS_PROJECT", "Pet-Guardian-Sprint-3")
    pat = args.pat or os.getenv("AZURE_DEVOPS_PAT") or env_vars.get("AZURE_DEVOPS_PAT", "")

    client = AzureBoardsClient(organization=org, project=project, pat=pat)

    if args.check_auth:
        print(f"\n🔍 Verificando conexão com Azure DevOps...")
        print(f"🏛️ Organização: {org}")
        print(f"📁 Projeto: {project}")
        ok, msg = client.check_connection()
        if ok:
            print(f"✅ {msg}")
        else:
            print(f"❌ Falha de autenticação / conexão:\n{msg}")
            print("\n💡 Dica: Verifique se o seu PAT está preenchido no arquivo .env com permissão 'Work Items (Read & Write)'.")
        return

    # Modo de execução: Todos ou Arquivo Único
    if args.all:
        print(f"\n🚀 Modo Selecionado: IMPORTAÇÃO TOTAL DE TODAS AS 7 DISCIPLINAS")
        total_stats = {"epics": 0, "features": 0, "pbis": 0, "tasks": 0}
        
        for rel_path, disc_name in ALL_DISCIPLINE_FILES:
            full_path = os.path.normpath(os.path.join(os.path.dirname(__file__), rel_path))
            if not os.path.exists(full_path):
                print(f"⚠️ Arquivo não encontrado: {full_path} (pulando...)")
                continue
            
            doc = parse_backlog_markdown(full_path)
            stats = client.sync_backlog(doc, dry_run=args.dry_run)
            for k in total_stats:
                total_stats[k] += stats.get(k, 0)

        print(f"\n========================================================")
        print(f"🎉 FINAL DA CARGA TOTAL CONSOLIDADA!")
        print(f"👑 Epics: {total_stats['epics']}")
        print(f"🏆 Features: {total_stats['features']}")
        print(f"📄 PBIs: {total_stats['pbis']}")
        print(f"🔨 Tasks: {total_stats['tasks']}")
        print(f"========================================================\n")
    else:
        target_path = os.path.normpath(os.path.join(os.path.dirname(__file__), args.file))
        if not os.path.exists(target_path):
            # Tenta caminho absoluto direto
            if os.path.exists(args.file):
                target_path = args.file
            else:
                print(f"❌ Erro: Arquivo de backlog não encontrado: {args.file}")
                return

        doc = parse_backlog_markdown(target_path)
        client.sync_backlog(doc, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
