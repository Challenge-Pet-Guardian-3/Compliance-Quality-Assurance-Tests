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
from typing import Dict, Any, Optional, List, Tuple

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


# Mapeamento Oficial das Iterações por Matéria / Tag da Sprint 3
DISCIPLINE_ITERATION_MAP = {
    # Semana 1 (2026-08-23 a 2026-08-29)
    "mobile": "Release 1 - Sprint 3\\Semana 1",
    "java": "Release 1 - Sprint 3\\Semana 1",
    "database": "Release 1 - Sprint 3\\Semana 1",
    
    # Semana 2 (2026-08-30 a 2026-09-05)
    "devops": "Release 1 - Sprint 3\\Semana 2",
    "disruptive": "Release 1 - Sprint 3\\Semana 2",
    "dotnet": "Release 1 - Sprint 3\\Semana 2",
    "compliance": "Release 1 - Sprint 3\\Semana 2",
}


def classify_discipline_from_tags_or_title(tags: str, title: str) -> Optional[str]:
    """
    Identifica a matéria a partir das tags oficiais (prioridade absoluta)
    ou secundariamente a partir do título do Work Item.
    """
    t_str = (tags or "").lower()
    
    # 1. Prioridade Máxima: Tags padronizadas do Azure Boards
    if "mobile" in t_str:
        return "mobile"
    if "javaadvanced" in t_str or "java" in t_str:
        return "java"
    if "database" in t_str:
        return "database"
    if "devops" in t_str:
        return "devops"
    if "disruptivearchitectures" in t_str or "disruptive" in t_str:
        return "disruptive"
    if "dotnet" in t_str or ".net" in t_str:
        return "dotnet"
    if "compliance" in t_str or "qa" in t_str:
        return "compliance"
        
    # 2. Fallback: Prefixo / Palavras-chave no Título
    title_lower = (title or "").lower()
    if "mobile" in title_lower:
        return "mobile"
    if "java" in title_lower or "spring" in title_lower:
        return "java"
    if "database" in title_lower or "pl/sql" in title_lower or "plsql" in title_lower:
        return "database"
    if "devops" in title_lower or "acr" in title_lower or "aci" in title_lower or "azure cli" in title_lower:
        return "devops"
    if "disruptive" in title_lower or "fastapi" in title_lower or "rag" in title_lower or "ia generativa" in title_lower:
        return "disruptive"
    if ".net" in title_lower or "dotnet" in title_lower or "csharp" in title_lower:
        return "dotnet"
    if "compliance" in title_lower or "quality assurance" in title_lower or "governança scrum" in title_lower:
        return "compliance"
        
    return None


class AzureIterationManager:
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

    def fetch_all_work_items(self) -> List[Dict[str, Any]]:
        """Recupera todos os Work Items do projeto via WIQL e batch API."""
        wiql_url = f"https://dev.azure.com/{self.organization}/{self.project}/_apis/wit/wiql?api-version=7.1-preview.2"
        headers = self._get_auth_headers(is_patch=False)
        query = {
            "query": "SELECT [System.Id], [System.WorkItemType], [System.Title], [System.IterationPath], [System.Tags] FROM WorkItems WHERE [System.TeamProject] = @project ORDER BY [System.Id]"
        }
        
        req = urllib.request.Request(wiql_url, data=json.dumps(query).encode("utf-8"), headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=25) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            work_items = data.get("workItems", [])
            if not work_items:
                return []
            
            ids = [item["id"] for item in work_items]
            
            # Buscar detalhes em chunks de 100
            detailed_items = []
            chunk_size = 100
            for i in range(0, len(ids), chunk_size):
                chunk = ids[i:i + chunk_size]
                batch_url = f"https://dev.azure.com/{self.organization}/{self.project}/_apis/wit/workitemsbatch?api-version=7.1-preview.1"
                batch_body = {
                    "ids": chunk,
                    "fields": ["System.Id", "System.WorkItemType", "System.Title", "System.IterationPath", "System.Tags"]
                }
                b_req = urllib.request.Request(batch_url, data=json.dumps(batch_body).encode("utf-8"), headers=headers, method="POST")
                with urllib.request.urlopen(b_req, timeout=25) as b_resp:
                    b_data = json.loads(b_resp.read().decode("utf-8"))
                    detailed_items.extend(b_data.get("value", []))
                    
            return detailed_items

    def update_item_iteration(self, item_id: int, target_iteration_path: str, dry_run: bool = False) -> bool:
        """Atualiza o IterationPath de um Work Item específico."""
        if dry_run:
            return True
            
        url = f"https://dev.azure.com/{self.organization}/{self.project}/_apis/wit/workitems/{item_id}?api-version=7.1-preview.3"
        headers = self._get_auth_headers(is_patch=True)
        patch_doc = [
            {
                "op": "replace",
                "path": "/fields/System.IterationPath",
                "value": target_iteration_path
            }
        ]
        
        req = urllib.request.Request(url, data=json.dumps(patch_doc).encode("utf-8"), headers=headers, method="PATCH")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.status == 200
        except Exception as e:
            print(f"      ❌ Erro ao atualizar item #{item_id}: {e}")
            return False

    def sync_all_iterations(self, filter_discipline: Optional[str] = None, dry_run: bool = False) -> Dict[str, int]:
        """Sincroniza todos os Work Items atribuindo o IterationPath correto conforme a matéria."""
        prefix = "[DRY-RUN] " if dry_run else ""
        print(f"\n========================================================")
        print(f"🔄 {prefix}Sincronizador de Iteration Paths no Azure Boards")
        print(f"🏛️ Organização: {self.organization} | Projeto: {self.project}")
        print(f"📅 Semana 1 (2026-08-23 a 2026-08-29): Mobile, Java Advanced, Database Advanced")
        print(f"📅 Semana 2 (2026-08-30 a 2026-09-05): DevOps Tools, Disruptive Architectures, .NET")
        print(f"========================================================\n")
        
        items = self.fetch_all_work_items()
        print(f"🔍 Total de Work Items encontrados no projeto: {len(items)}\n")
        
        stats = {
            "semana1_updated": 0,
            "semana2_updated": 0,
            "already_correct": 0,
            "unmapped": 0,
            "errors": 0
        }
        
        for idx, item in enumerate(items, 1):
            i_id = item["id"]
            fields = item.get("fields", {})
            w_type = fields.get("System.WorkItemType", "Item")
            title = fields.get("System.Title", "")
            tags = fields.get("System.Tags", "")
            current_path = fields.get("System.IterationPath", "")
            
            disc = classify_discipline_from_tags_or_title(tags, title)
            if not disc or disc not in DISCIPLINE_ITERATION_MAP:
                print(f"⚠️ [{idx}/{len(items)}] Item #{i_id} ({w_type}): '{title}' (sem matéria identificada)")
                stats["unmapped"] += 1
                continue
                
            if filter_discipline and filter_discipline.lower() not in disc:
                continue
                
            rel_iter = DISCIPLINE_ITERATION_MAP[disc]
            target_path = f"{self.project}\\{rel_iter}"
            
            if current_path == target_path:
                stats["already_correct"] += 1
                continue
                
            is_sem1 = "Semana 1" in target_path
            target_label = "Semana 1" if is_sem1 else "Semana 2"
            
            if dry_run:
                print(f"   [DRY-RUN] #{i_id} ({w_type}): '{title[:50]}...' ➔ {target_label} ({target_path})")
                if is_sem1:
                    stats["semana1_updated"] += 1
                else:
                    stats["semana2_updated"] += 1
            else:
                ok = self.update_item_iteration(i_id, target_path, dry_run=False)
                if ok:
                    print(f"   ✅ #{i_id} ({w_type}): '{title[:50]}...' ➔ {target_label}")
                    if is_sem1:
                        stats["semana1_updated"] += 1
                    else:
                        stats["semana2_updated"] += 1
                else:
                    stats["errors"] += 1
                    
        print(f"\n========================================================")
        print(f"✨ {prefix}Relatório Final de Sincronização de Iterações:")
        print(f"   • Atualizados para Semana 1: {stats['semana1_updated']}")
        print(f"   • Atualizados para Semana 2: {stats['semana2_updated']}")
        print(f"   • Já estavam no caminho correto: {stats['already_correct']}")
        print(f"   • Não mapeados / Ignorados: {stats['unmapped']}")
        print(f"   • Erros de atualização: {stats['errors']}")
        print(f"========================================================\n")
        return stats


def main():
    parser = argparse.ArgumentParser(description="Atualiza e padroniza os IterationPaths no Azure Boards")
    parser.add_argument("--dry-run", "-d", action="store_true", help="Simula as alterações sem modificar a nuvem")
    parser.add_argument("--discipline", "-m", type=str, default=None, help="Filtra por matéria específica (ex: mobile, devops, dotnet, java)")
    parser.add_argument("--org", type=str, default=None, help="Organização do Azure DevOps")
    parser.add_argument("--project", type=str, default=None, help="Projeto do Azure DevOps")
    parser.add_argument("--pat", type=str, default=None, help="Personal Access Token (PAT)")
    
    args = parser.parse_args()
    env = load_env_file()
    
    org = args.org or os.getenv("AZURE_DEVOPS_ORG") or env.get("AZURE_DEVOPS_ORG", "PetGuardian")
    proj = args.project or os.getenv("AZURE_DEVOPS_PROJECT") or env.get("AZURE_DEVOPS_PROJECT", "Pet-Guardian-Sprint-3")
    pat = args.pat or os.getenv("AZURE_DEVOPS_PAT") or env.get("AZURE_DEVOPS_PAT", "")
    
    manager = AzureIterationManager(organization=org, project=proj, pat=pat)
    manager.sync_all_iterations(filter_discipline=args.discipline, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
