import urllib.request
import json
import base64
import os
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def main():
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    env = {}
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    k, v = line.strip().split("=", 1)
                    env[k.strip()] = v.strip().strip("'\"")

    org = env.get("AZURE_DEVOPS_ORG", "PetGuardian")
    proj = env.get("AZURE_DEVOPS_PROJECT", "Pet-Guardian-Sprint-3")
    pat = env.get("AZURE_DEVOPS_PAT", "")

    auth = base64.b64encode(f":{pat}".encode("utf-8")).decode("utf-8")
    url = f"https://dev.azure.com/{org}/{proj}/_apis/wit/wiql?api-version=7.1-preview.2"
    query = {"query": "Select [System.Id], [System.Title], [System.WorkItemType] From WorkItems Where [System.TeamProject] = @project and [System.WorkItemType] = 'Epic'"}
    req = urllib.request.Request(
        url,
        data=json.dumps(query).encode("utf-8"),
        headers={"Authorization": f"Basic {auth}", "Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        ids = [it["id"] for it in data.get("workItems", [])]
        batch_url = f"https://dev.azure.com/{org}/{proj}/_apis/wit/workitemsbatch?api-version=7.1-preview.1"
        batch_req = urllib.request.Request(
            batch_url,
            data=json.dumps({"ids": ids, "fields": ["System.Id", "System.Title", "Microsoft.VSTS.Scheduling.Effort"]}).encode("utf-8"),
            headers={"Authorization": f"Basic {auth}", "Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(batch_req, timeout=15) as b_resp:
            b_data = json.loads(b_resp.read().decode("utf-8"))
            total = 0.0
            print("\n--- 👑 ÉPICOS SINCRONIZADOS NO AZURE BOARDS ---")
            for it in b_data.get("value", []):
                f = it.get("fields", {})
                eff = f.get("Microsoft.VSTS.Scheduling.Effort") or 0.0
                total += eff
                print(f"#{it['id']} | Effort: {eff:4.1f} SP | {f.get('System.Title')}")
            print("==========================================================================")
            print(f"🎯 TOTAL DE STORY POINTS NO AZURE BOARDS: {total:4.1f} SP")
            print("==========================================================================\n")

if __name__ == "__main__":
    main()