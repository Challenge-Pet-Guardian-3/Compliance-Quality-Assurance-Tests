import sys
import os
import re
import json
import base64
import argparse
import subprocess
import urllib.request
import urllib.parse
import urllib.error
from typing import Dict, Any, Optional, List

# Adiciona diretório do script ao sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parser_backlog import parse_backlog_markdown, clean_title

# Garante suporte a UTF-8 no terminal Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


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


class AzureDescriptionsUpdater:
    def __init__(self, organization: str, project: str, pat: Optional[str] = None):
        self.organization = organization.strip()
        self.project = project.strip()
        self.pat = (pat or "").strip()
        self.bearer_token: Optional[str] = None

    def _get_auth_headers(self, is_patch: bool = False) -> Dict[str, str]:
        content_type = "application/json-patch+json" if is_patch else "application/json"
        
        if self.pat:
            auth_str = f":{self.pat}"
            b64_auth = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")
            return {
                "Authorization": f"Basic {b64_auth}",
                "Content-Type": content_type,
                "Accept": "application/json"
            }
        
        if not self.bearer_token:
            try:
                cmd = ["az", "account", "get-access-token", "--resource", "499b84ac-1321-427f-aa17-267ca6975798", "-o", "json"]
                result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
                data = json.loads(result.stdout)
                self.bearer_token = data.get("accessToken")
            except Exception:
                pass

        if self.bearer_token:
            return {
                "Authorization": f"Bearer {self.bearer_token}",
                "Content-Type": content_type,
                "Accept": "application/json"
            }

        raise ValueError(
            "Nenhuma credencial configurada!\n"
            "Preencha o PAT no .env ou faça login no terminal com 'az login'."
        )

    def fetch_all_epics_and_features(self) -> List[Dict[str, Any]]:
        wiql_url = f"https://dev.azure.com/{self.organization}/{self.project}/_apis/wit/wiql?api-version=7.1-preview.2"
        headers = self._get_auth_headers(is_patch=False)
        query = {
            "query": "SELECT [System.Id], [System.WorkItemType], [System.Title], [System.Description], [System.Tags] FROM WorkItems WHERE [System.TeamProject] = @project AND [System.WorkItemType] IN ('Epic', 'Feature') ORDER BY [System.Id]"
        }
        
        req = urllib.request.Request(wiql_url, data=json.dumps(query).encode("utf-8"), headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=25) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            work_items = data.get("workItems", [])
            if not work_items:
                return []
            
            ids = [item["id"] for item in work_items]
            
            # Buscar detalhes em batch
            batch_url = f"https://dev.azure.com/{self.organization}/{self.project}/_apis/wit/workitemsbatch?api-version=7.1-preview.1"
            batch_body = {
                "ids": ids,
                "fields": ["System.Id", "System.WorkItemType", "System.Title", "System.Description", "System.Tags"]
            }
            b_req = urllib.request.Request(batch_url, data=json.dumps(batch_body).encode("utf-8"), headers=headers, method="POST")
            with urllib.request.urlopen(b_req, timeout=25) as b_resp:
                b_data = json.loads(b_resp.read().decode("utf-8"))
                return b_data.get("value", [])

    def update_description(self, item_id: int, description: str, dry_run: bool = False) -> bool:
        if dry_run:
            return True
            
        url = f"https://dev.azure.com/{self.organization}/{self.project}/_apis/wit/workitems/{item_id}?api-version=7.1-preview.3"
        headers = self._get_auth_headers(is_patch=True)
        patch_doc = [
            {
                "op": "replace",
                "path": "/fields/System.Description",
                "value": description
            }
        ]
        
        req = urllib.request.Request(url, data=json.dumps(patch_doc).encode("utf-8"), headers=headers, method="PATCH")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.status == 200
        except Exception as e:
            print(f"      ❌ Erro ao atualizar item #{item_id}: {e}")
            return False

    def sync_descriptions(self, dry_run: bool = False):
        prefix = "[DRY-RUN] " if dry_run else ""
        print(f"\n========================================================")
        print(f"📝 {prefix}Sincronizador de Descriptions de Epics e Features")
        print(f"🏛️ Organização: {self.organization} | Projeto: {self.project}")
        print(f"========================================================\n")

        # 1. Carrega todos os backlogs e mapeia por título limpo
        descriptions_map: Dict[str, str] = {}
        for rel_path, disc_name in ALL_DISCIPLINE_FILES:
            full_path = os.path.normpath(os.path.join(os.path.dirname(__file__), rel_path))
            if not os.path.exists(full_path):
                continue
            doc = parse_backlog_markdown(full_path)
            
            # Epic
            cleaned_epic_title = clean_title(doc.epic.title).lower()
            if doc.epic.description:
                descriptions_map[cleaned_epic_title] = doc.epic.description
                
            # Features
            for feat in doc.epic.features:
                cleaned_feat_title = clean_title(feat.title).lower()
                if feat.description:
                    descriptions_map[cleaned_feat_title] = feat.description

        print(f"📖 Carregadas {len(descriptions_map)} descrições dos arquivos Markdown.")

        # 2. Busca todos os Epics e Features no Azure Boards
        azure_items = self.fetch_all_epics_and_features()
        print(f"🔍 Encontrados {len(azure_items)} Épicos/Features no Azure Boards.\n")

        updated_count = 0
        already_ok_count = 0
        not_found_count = 0

        for it in azure_items:
            i_id = it["id"]
            fields = it.get("fields", {})
            w_type = fields.get("System.WorkItemType", "Item")
            title = fields.get("System.Title", "")
            current_desc = fields.get("System.Description", "")
            
            cleaned_title = clean_title(title).lower()
            target_desc = descriptions_map.get(cleaned_title)

            # Se não encontrou exato, tenta correspondência parcial (ex: FEATURE 01)
            if not target_desc:
                for k, v in descriptions_map.items():
                    if (cleaned_title in k or k in cleaned_title) and len(cleaned_title) > 10:
                        target_desc = v
                        break

            if not target_desc:
                print(f"⚠️ #{i_id} ({w_type}): '{title}' -> Nenhuma descrição encontrada nos arquivos.")
                not_found_count += 1
                continue

            if current_desc and current_desc.strip() == target_desc.strip():
                already_ok_count += 1
                continue

            if dry_run:
                print(f"   [DRY-RUN] #{i_id} ({w_type}): '{title[:60]}...' ➔ Preencher Description ({len(target_desc)} chars)")
                updated_count += 1
            else:
                ok = self.update_description(i_id, target_desc, dry_run=False)
                if ok:
                    print(f"   ✅ #{i_id} ({w_type}): '{title[:60]}...' ➔ Description atualizada!")
                    updated_count += 1

        print(f"\n========================================================")
        print(f"✨ {prefix}Relatório Final de Atualização de Descriptions:")
        print(f"   • Atualizados: {updated_count}")
        print(f"   • Já estavam corretos: {already_ok_count}")
        print(f"   • Não encontrados: {not_found_count}")
        print(f"========================================================\n")


def main():
    parser = argparse.ArgumentParser(description="Atualiza as descrições de Épicos e Features no Azure Boards")
    parser.add_argument("--dry-run", "-d", action="store_true", help="Simula a execução sem alterar o Azure")
    parser.add_argument("--org", type=str, default=None, help="Organização do Azure DevOps")
    parser.add_argument("--project", type=str, default=None, help="Projeto do Azure DevOps")
    parser.add_argument("--pat", type=str, default=None, help="Personal Access Token (PAT)")

    args = parser.parse_args()
    env = load_env_file()

    org = args.org or os.getenv("AZURE_DEVOPS_ORG") or env.get("AZURE_DEVOPS_ORG", "PetGuardian")
    proj = args.project or os.getenv("AZURE_DEVOPS_PROJECT") or env.get("AZURE_DEVOPS_PROJECT", "Pet-Guardian-Sprint-3")
    pat = args.pat or os.getenv("AZURE_DEVOPS_PAT") or env.get("AZURE_DEVOPS_PAT", "")

    updater = AzureDescriptionsUpdater(organization=org, project=proj, pat=pat)
    updater.sync_descriptions(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
