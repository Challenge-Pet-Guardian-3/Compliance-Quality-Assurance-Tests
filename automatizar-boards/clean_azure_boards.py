import sys
import os
import json
import base64
import urllib.request
import urllib.parse
import urllib.error
import time

# Garante UTF-8 no Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def load_env():
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    env = {}
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    k, v = line.strip().split("=", 1)
                    env[k.strip()] = v.strip().strip("'\"")
    return env

def get_all_work_item_ids(org: str, project: str, auth: str):
    url = f"https://dev.azure.com/{org}/{project}/_apis/wit/wiql?api-version=7.1-preview.2"
    query = {"query": "Select [System.Id] From WorkItems Where [System.TeamProject] = @project"}
    req = urllib.request.Request(
        url,
        data=json.dumps(query).encode("utf-8"),
        headers={"Authorization": f"Basic {auth}", "Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        items = data.get("workItems", [])
        return [it["id"] for it in items]

def delete_work_item(org: str, project: str, auth: str, item_id: int, destroy: bool = True):
    destroy_str = "true" if destroy else "false"
    url = f"https://dev.azure.com/{org}/{project}/_apis/wit/workitems/{item_id}?destroy={destroy_str}&api-version=7.1-preview.3"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Basic {auth}"},
        method="DELETE"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status in (200, 204)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return True
        print(f"Erro ao deletar #{item_id} (HTTP {e.code})")
        return False
    except Exception as e:
        print(f"Exceção ao deletar #{item_id}: {e}")
        return False

def clean_boards(destroy: bool = True):
    env = load_env()
    org = env.get("AZURE_DEVOPS_ORG", "PetGuardian")
    project = env.get("AZURE_DEVOPS_PROJECT", "Pet-Guardian-Sprint-3")
    pat = env.get("AZURE_DEVOPS_PAT", "")

    if not pat:
        print("❌ PAT não configurado no .env!")
        return

    auth = base64.b64encode(f":{pat}".encode("utf-8")).decode("utf-8")
    
    print(f"🔍 Buscando work items existentes em {org}/{project}...")
    ids = get_all_work_item_ids(org, project, auth)
    print(f"📊 Encontrados {len(ids)} work items para remoção.")

    if not ids:
        print("✅ O Board já está completamente limpo!")
        return

    deleted = 0
    for idx, item_id in enumerate(ids, 1):
        ok = delete_work_item(org, project, auth, item_id, destroy=destroy)
        if ok:
            deleted += 1
        if idx % 20 == 0 or idx == len(ids):
            print(f"🗑️ Progresso: {idx}/{len(ids)} itens processados...")
        time.sleep(0.05)

    print(f"\n✨ Limpeza concluída: {deleted}/{len(ids)} itens removidos com sucesso!")

if __name__ == "__main__":
    clean_boards(destroy=True)
