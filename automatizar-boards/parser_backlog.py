import sys
import os
import re
import html
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

# Garante suporte a UTF-8 no terminal Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def clean_title(text: str) -> str:
    """
    Remove qualquer emoji, ícone, crases, asteriscos ou símbolo decorativo de títulos para o Azure Boards.
    Garante títulos 100% limpos e formais.
    """
    if not text:
        return ""
    # Remove faixa completa de emojis e símbolos especiais Unicode
    cleaned = re.sub(r"[\U00010000-\U0010ffff]", "", text)  # Emojis 4-byte
    cleaned = re.sub(r"[\u2600-\u27BF\u2300-\u23FF\u2B50-\u2B55\u200d\uFE0F\u00A9\u00AE]", "", cleaned)  # Símbolos, dingbats
    cleaned = cleaned.replace("`", "").replace("'", "").replace('"', "").replace("**", "").replace("*", "")
    cleaned = re.sub(r"^\s*-\s*", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


@dataclass
class TaskItem:
    title: str
    description: str = ""
    work_item_type: str = "Task"
    activity: str = "Development"
    remaining_work: Optional[float] = None
    tags: List[str] = field(default_factory=list)


@dataclass
class PBIItem:
    title: str
    description: str = ""
    acceptance_criteria: str = ""
    story_points: float = 0.0
    priority: int = 2
    business_value: int = 80
    tags: List[str] = field(default_factory=list)
    work_item_type: str = "Product Backlog Item"
    parent_feature_ref: str = ""
    tasks: List[TaskItem] = field(default_factory=list)


@dataclass
class FeatureItem:
    title: str
    code: str = ""
    description: str = ""
    acceptance_criteria: str = ""
    start_date: Optional[str] = None
    target_date: Optional[str] = None
    effort: float = 0.0
    priority: int = 1
    business_value: int = 100
    tags: List[str] = field(default_factory=list)
    work_item_type: str = "Feature"
    pbis: List[PBIItem] = field(default_factory=list)


@dataclass
class EpicItem:
    title: str
    description: str = ""
    acceptance_criteria: str = ""
    start_date: Optional[str] = None
    target_date: Optional[str] = None
    effort: float = 0.0
    priority: int = 1
    business_value: int = 100
    tags: List[str] = field(default_factory=list)
    work_item_type: str = "Epic"
    features: List[FeatureItem] = field(default_factory=list)


@dataclass
class BacklogDocument:
    discipline: str
    epic: EpicItem
    raw_file_path: str = ""


def _markdown_to_clean_html(text: str) -> str:
    """
    Converte markdown para HTML limpo sem estilizações invasivas (sem barras azuis, sem títulos extras).
    """
    if not text:
        return ""
    
    clean_lines = []
    in_user_story = False
    story_lines = []
    
    for raw_line in text.split("\n"):
        line = raw_line.strip()
        if not line:
            if story_lines:
                clean_lines.append("<div>" + "<br/>".join(story_lines) + "</div>")
                story_lines = []
                in_user_story = False
            continue
            
        # Ignora linhas decorativas ou títulos redundantes
        if line.startswith("---") or line.startswith("===") or re.match(r"^#{1,6}\s+", line):
            continue
            
        # Remove marcas de citação (>)
        line = re.sub(r"^>\s*", "", line).strip()
        
        # Detecta linhas de História de Usuário (Como / Eu quero / Para que)
        if re.match(r"^\*\*(?:Como|Eu quero|Para que|Para)\*\*", line, re.IGNORECASE) or \
           re.match(r"^(?:Como|Eu quero|Para que|Para)\b", line, re.IGNORECASE):
            in_user_story = True
            story_lines.append(_format_inline_markdown(line))
            continue
            
        if in_user_story and story_lines:
            story_lines.append(_format_inline_markdown(line))
            continue
            
        # Linhas de lista com checkboxes ou marcadores
        if re.match(r"^[-\*]\s*\[[ xX]\]\s*", line):
            content = re.sub(r"^[-\*]\s*\[[ xX]\]\s*", "", line)
            clean_lines.append(f"<li>{_format_inline_markdown(content)}</li>")
        elif re.match(r"^[-\*]\s+", line):
            content = re.sub(r"^[-\*]\s+", "", line)
            clean_lines.append(f"<li>{_format_inline_markdown(content)}</li>")
        elif re.match(r"^\d+\.\s+", line):
            content = re.sub(r"^\d+\.\s+", "", line)
            clean_lines.append(f"<li>{_format_inline_markdown(content)}</li>")
        else:
            clean_lines.append(f"<p>{_format_inline_markdown(line)}</p>")
            
    if story_lines:
        clean_lines.append("<div>" + "<br/>".join(story_lines) + "</div>")
        
    result = "\n".join(clean_lines)
    # Envelopa listas <li> consecutivas em <ul>
    if "<li>" in result:
        result = re.sub(r"((?:<li>.*?</li>\n?)+)", r"<ul>\n\1</ul>", result, flags=re.DOTALL)
        
    return result.strip()


def _format_inline_markdown(text: str) -> str:
    """Formata tags inline como negrito, itálico e código."""
    t = html.escape(text)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"__(.+?)__", r"<strong>\1</strong>", t)
    t = re.sub(r"\*(.+?)\*", r"<em>\1</em>", t)
    t = re.sub(r"_(.+?)_", r"<em>\1</em>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    return t


def _parse_priority(raw_priority: str) -> int:
    """Converte strings de prioridade em inteiros de 1 a 4."""
    if not raw_priority:
        return 2
    raw = raw_priority.lower().replace("`", "").replace("'", "").replace('"', "").strip()
    if "1" in raw or "crit" in raw or "urgent" in raw:
        return 1
    elif "2" in raw or "high" in raw or "alta" in raw:
        return 2
    elif "3" in raw or "medium" in raw or "media" in raw or "média" in raw:
        return 3
    elif "4" in raw or "low" in raw or "baixa" in raw:
        return 4
    return 2


def _priority_to_business_value(priority: int) -> int:
    """Mapeia prioridade para Business Value no Scrum."""
    if priority == 1:
        return 100
    elif priority == 2:
        return 80
    elif priority == 3:
        return 50
    return 20


def _parse_story_points(raw_effort: str) -> float:
    """Extrai valor numérico de Story Points."""
    if not raw_effort:
        return 0.0
    cleaned = raw_effort.replace("`", "").replace("'", "").replace('"', "")
    match = re.search(r"(\d+(?:\.\d+)?)", cleaned)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return 0.0
    return 0.0


def _parse_date(text: str) -> Optional[str]:
    """Converte datas em formatos comuns (YYYY-MM-DD, DD/MM/YYYY, DD-MM-YYYY) para YYYY-MM-DD."""
    if not text:
        return None
    cleaned = text.strip().strip("`").strip('"').strip("'")
    
    # YYYY-MM-DD
    m_iso = re.search(r"(\d{4})[/-](\d{1,2})[/-](\d{1,2})", cleaned)
    if m_iso:
        y, m, d = m_iso.groups()
        return f"{int(y):04d}-{int(m):02d}-{int(d):02d}"
    
    # DD/MM/YYYY
    m_br = re.search(r"(\d{1,2})[/-](\d{1,2})[/-](\d{4})", cleaned)
    if m_br:
        d, m, y = m_br.groups()
        return f"{int(y):04d}-{int(m):02d}-{int(d):02d}"
    
    return None


def _normalize_activity(text: str) -> str:
    """Normaliza o tipo de atividade para os padrões oficiais do Scrum Process Template no Azure Boards."""
    if not text:
        return "Development"
    t = text.strip().lower()
    if any(k in t for k in ["req", "requisito", "planejamento", "analise", "análise"]):
        return "Requirements"
    if any(k in t for k in ["test", "qa", "valida", "homologa"]):
        return "Testing"
    if any(k in t for k in ["doc", "readme", "apresenta", "vídeo", "video", "pitch", "relat"]):
        return "Documentation"
    if any(k in t for k in ["design", "layout", "protótipo", "prototipo"]) or re.search(r"\b(ui|ux)\b", t):
        return "Design"
    if any(k in t for k in ["deploy", "infra", "cloud", "iac", "pipeline", "ci/cd", "azure", "docker"]):
        return "Deployment"
    if any(k in t for k in ["dev", "desenvolvimento", "código", "backend", "frontend", "api", "crud", "refator"]):
        return "Development"
    return "Development"


def _parse_task_line(task_line: str, default_tags: List[str]) -> Optional[TaskItem]:
    """
    Extrai título limpo, Activity e Remaining Work (horas) a partir de uma linha de Task.
    Formatos suportados:
    - * **Task 1.1:** [TASK-01] Executar script. *(Activity: Testing, Est: 1.0h)*
    - * **Task 1.1:** Criar endpoints. *(2.0h)*
    - - [ ] [TASK-01] Executar script *(Activity: Testing)*
    """
    clean_line = re.sub(r"^(-\s*\[[ xX]\]\s*|[\*\-]\s*)", "", task_line).strip()
    if not clean_line:
        return None

    # Extrai horas estimadas
    remaining_work = None
    hours_match = re.search(r"(?:Est(?:imativa)?:?\s*|\b)(\d+(?:\.\d+)?)\s*h(?:oras?)?", clean_line, re.IGNORECASE)
    if hours_match:
        try:
            remaining_work = float(hours_match.group(1))
        except ValueError:
            pass

    # Extrai atividade
    activity = "Development"
    activity_match = re.search(r"Activity:\s*([A-Za-z]+)", clean_line, re.IGNORECASE)
    if activity_match:
        activity = _normalize_activity(activity_match.group(1))
    else:
        activity = _normalize_activity(clean_line)

    # Limpa o título da task removendo sufixos de anotações
    title_part = re.sub(r"\*?\([^\)]*(?:h|Activity|Est)[^\)]*\)\*?", "", clean_line).strip()
    title_part = clean_title(title_part)

    if not title_part:
        return None

    return TaskItem(
        title=title_part,
        description="",
        work_item_type="Task",
        activity=activity,
        remaining_work=remaining_work,
        tags=list(default_tags)
    )


def _parse_tags(raw_tags: str) -> List[str]:
    """Separa tags por vírgula ou ponto-e-vírgula e limpa crases/espaços."""
    if not raw_tags:
        return []
    cleaned = raw_tags.replace("`", "").replace("'", "").replace('"', "").replace(";", ",")
    tags = [t.strip() for t in cleaned.split(",") if t.strip()]
    return tags


def parse_backlog_markdown(file_path: str) -> BacklogDocument:
    """
    Lê um arquivo Markdown e extrai a hierarquia de Epics, Features, PBIs e Tasks,
    separando estritamente Description de Acceptance Criteria e calculando Effort/Business Value.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")

    discipline = "Geral"
    epic_title = ""
    epic_tags = []

    # 1. Procura metadados do cabeçalho
    for line in lines[:30]:
        disc_match = re.search(r">\s*\*\*Disciplina:\*\*\s*(.+)", line, re.IGNORECASE)
        if disc_match:
            discipline = disc_match.group(1).strip()

        epic_match = re.search(r">\s*\*\*Epic Principal:\*\*\s*`?([^`\n]+)`?", line, re.IGNORECASE)
        if epic_match:
            epic_title = epic_match.group(1).strip()

    if not epic_title:
        for line in lines:
            m = re.search(r"^#+\s*(?:[^\w\s\[]*\s*)?(?:\[EPIC\]|\[EPIC-[^\]]+\]|Epic:?)\s*(.+)", line, re.IGNORECASE)
            if m:
                epic_title = m.group(1).strip()
                break

    if not epic_title:
        for line in lines:
            if line.startswith("# "):
                epic_title = line.replace("# ", "").strip()
                break
        if not epic_title:
            epic_title = f"Epic Backlog Sprint 3 - {discipline}"

    epic_title = clean_title(epic_title)

    epic_item = EpicItem(
        title=epic_title,
        description="",
        acceptance_criteria="",
        priority=1,
        business_value=100,
        tags=epic_tags
    )

    for line in lines[:30]:
        start_m = re.search(r">\s*\*\*(?:Start Date|Data de In[íi]cio)[^\*]*:?\*\*:?\s*`?([^`\n]+)`?", line, re.IGNORECASE)
        if start_m:
            epic_item.start_date = _parse_date(start_m.group(1))

        target_m = re.search(r">\s*\*\*(?:Target Date|End Date|Data de T[ée]rmino|Data Alvo)[^\*]*:?\*\*:?\s*`?([^`\n]+)`?", line, re.IGNORECASE)
        if target_m:
            epic_item.target_date = _parse_date(target_m.group(1))

    # 2. Pré-mapeamento de Features da árvore se existir
    feature_map: Dict[str, FeatureItem] = {}

    tree_in_progress = False
    for line in lines:
        if "```" in line:
            tree_in_progress = not tree_in_progress
            continue
        if tree_in_progress:
            feat_tree_match = re.search(r"[├└]──\s*(?:[^\w\s\[]*\s*)?\[?(?:FEATURE|FEAT)[-:\s]*(\d+|[A-Z0-9_-]+)\]?[:\s]*(.+)", line, re.IGNORECASE)
            if feat_tree_match:
                raw_num = feat_tree_match.group(1).strip()
                name_raw = clean_title(feat_tree_match.group(2).strip())
                if raw_num.isdigit():
                    code_norm = f"feature{int(raw_num):02d}"
                    code_display = f"FEATURE {int(raw_num):02d}"
                else:
                    code_norm = re.sub(r"[^a-zA-Z0-9]", "", f"feature{raw_num}").lower()
                    code_display = f"FEATURE {raw_num.upper()}"
                full_feat_title = clean_title(f"[{code_display}] {name_raw}")
                if code_norm not in feature_map:
                    f_item = FeatureItem(title=full_feat_title, code=code_norm)
                    feature_map[code_norm] = f_item
                    epic_item.features.append(f_item)

    # 3. Processa detalhamento de Features e PBIs
    current_feature: Optional[FeatureItem] = None
    current_pbi: Optional[PBIItem] = None
    current_section = None
    desc_buffer = []
    acceptance_buffer = []
    task_buffer = []

    def get_or_create_feature(parent_ref: str) -> FeatureItem:
        clean_ref = clean_title(parent_ref)
        
        # 1. Procura número da Feature (ex: Feature 01, FEAT-02, etc.)
        code_match = re.search(r"(?:FEATURE|FEAT)\s*[-:\s]*\s*(\d+)", clean_ref, re.IGNORECASE)
        code_norm = ""
        if code_match:
            code_norm = f"feature{int(code_match.group(1)):02d}"
        else:
            code_alt = re.search(r"(?:FEATURE|FEAT)\s*[-:\s]*\s*([A-Z0-9_-]+)", clean_ref, re.IGNORECASE)
            if code_alt:
                code_norm = re.sub(r"[^a-zA-Z0-9]", "", code_alt.group(0)).lower()

        if code_norm and code_norm in feature_map:
            return feature_map[code_norm]

        for f in epic_item.features:
            if f.code and code_norm and f.code == code_norm:
                return f
            if clean_ref.lower() in f.title.lower() or f.title.lower() in clean_ref.lower():
                return f

        new_f = FeatureItem(title=clean_ref, code=code_norm)
        if code_norm:
            feature_map[code_norm] = new_f
        epic_item.features.append(new_f)
        return new_f

    def flush_pbi():
        nonlocal current_pbi, desc_buffer, acceptance_buffer, task_buffer
        if current_pbi:
            # Separação estrita: Description contém User Story; AcceptanceCriteria vai no campo próprio
            current_pbi.description = _markdown_to_clean_html("\n".join(desc_buffer))
            current_pbi.acceptance_criteria = _markdown_to_clean_html("\n".join(acceptance_buffer))
            current_pbi.business_value = _priority_to_business_value(current_pbi.priority)

            parsed_tasks = []
            current_task_item = None
            for raw_t_line in task_buffer:
                stripped_t = raw_t_line.strip()
                desc_match = re.search(r"^\*?\s*\*?Descri[çc][ãa]o:?\*?\s*(.+)", stripped_t, re.IGNORECASE)
                if desc_match:
                    desc_content = desc_match.group(1).strip().strip("*_").strip()
                    if current_task_item:
                        current_task_item.description = _markdown_to_clean_html(desc_content)
                elif stripped_t.startswith("- [ ]") or stripped_t.startswith("* [ ]") or stripped_t.startswith("- ") or stripped_t.startswith("* **Task") or stripped_t.startswith("* **[TASK") or stripped_t.startswith("* **TASK"):
                    current_task_item = _parse_task_line(stripped_t, current_pbi.tags)
                    if current_task_item:
                        parsed_tasks.append(current_task_item)

            current_pbi.tasks.extend(parsed_tasks)

            target_feature = None
            if current_pbi.parent_feature_ref:
                target_feature = get_or_create_feature(current_pbi.parent_feature_ref)
            elif current_feature:
                target_feature = current_feature
            elif epic_item.features:
                target_feature = epic_item.features[-1]
            else:
                target_feature = FeatureItem(title="Feature Geral da Sprint 3")
                epic_item.features.append(target_feature)

            target_feature.pbis.append(current_pbi)

            current_pbi = None
            desc_buffer = []
            acceptance_buffer = []
            task_buffer = []

    def flush_feature():
        nonlocal current_feature
        flush_pbi()
        if current_feature and current_feature not in epic_item.features:
            epic_item.features.append(current_feature)
            current_feature = None

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Detecção de Cabeçalho do Épico na Seção 4 (ex: ### 🏛️ ÉPICO)
        if re.search(r"^#{2,3}\s+.*(?:[ÉE]PICO|EPIC)\b", stripped, re.IGNORECASE) and not any(k in stripped.lower() for k in ["feature", "detalhamento", "tabela resumo", "painel geral"]):
            flush_feature()
            current_feature = None
            current_pbi = None
            current_section = None
            i += 1
            continue

        # Detecção de Nova Seção de Nível 1 ou 2 que encerra o detalhamento de Work Items
        if re.match(r"^#{1,2}\s+", stripped) and not any(k in stripped.lower() for k in ["[epic", "épico", "epic:", "feature", "feat"]):
            flush_feature()
            current_feature = None
            current_pbi = None
            current_section = None
            i += 1
            continue

        # Detecção de Nova Feature no corpo
        feat_match = re.search(r"^#{2,3}\s+(?:[^\w\s\[]*\s*)?\[?(?:FEATURE|FEAT)[-:\s]*(\d+|[A-Z0-9_-]+)?\]?[:\s]*(.+)", stripped, re.IGNORECASE)
        if feat_match and not any(k in stripped.lower() for k in ["tabela resumo", "painel geral", "resumo executivo", "estrutura hierárquica", "estrutura do backlog"]):
            flush_feature()
            feat_num = feat_match.group(1) or ""
            feat_name = clean_title(feat_match.group(2).strip())
            feat_name = re.sub(r"^\[.*?\]\s*", "", feat_name).strip()
            
            if feat_num and feat_num.isdigit():
                title = f"[FEATURE {int(feat_num):02d}] {feat_name}"
            elif feat_num:
                title = f"[FEATURE {feat_num}] {feat_name}"
            elif feat_name.lower().startswith("feature"):
                title = feat_name
            else:
                title = f"Feature: {feat_name}"
            
            clean_feat_title = clean_title(title)
            current_feature = get_or_create_feature(clean_feat_title)
            current_section = None
            i += 1
            continue

        # Detecção de Novo PBI
        pbi_match = re.search(r"^#{3,4}\s+(?:[^\w\s\[]*\s*)?\[?(PBI(?:-[A-Z0-9_-]+|\d+)?)\]?[:\s]*(.+)", stripped, re.IGNORECASE)
        if pbi_match:
            flush_pbi()
            pbi_code = pbi_match.group(1).strip()
            pbi_title = clean_title(pbi_match.group(2).strip())
            pbi_title = re.sub(r"^\[.*?\]\s*", "", pbi_title).strip()
            if not pbi_code.startswith("["):
                pbi_code = f"[{pbi_code}]"
            full_pbi_title = clean_title(f"{pbi_code} {pbi_title}")
            current_pbi = PBIItem(title=full_pbi_title)
            current_section = None
            i += 1
            continue

        # Se estamos dentro de um PBI
        if current_pbi is not None:
            prio_match = re.search(r"^\*?\s*\*\*Priorit[yáe][^\*]*:?\*\*:?\s*(.+)", stripped, re.IGNORECASE)
            if prio_match:
                current_pbi.priority = _parse_priority(prio_match.group(1))
                i += 1
                continue

            effort_match = re.search(r"^\*?\s*\*\*(?:Effort|Story Points|Pontos|Esforço)[^\*]*:?\*\*:?\s*(.+)", stripped, re.IGNORECASE)
            if effort_match:
                current_pbi.story_points = _parse_story_points(effort_match.group(1))
                i += 1
                continue

            tags_match = re.search(r"^\*?\s*\*\*Tags?:?\*\*:?\s*(.+)", stripped, re.IGNORECASE)
            if tags_match:
                current_pbi.tags = _parse_tags(tags_match.group(1))
                i += 1
                continue

            parent_match = re.search(r"^\*?\s*\*\*Parent\s*Feature:?\*\*:?\s*(.+)", stripped, re.IGNORECASE)
            if parent_match:
                current_pbi.parent_feature_ref = parent_match.group(1).strip()
                i += 1
                continue

            # Cabeçalhos de Seções internas do PBI
            if re.search(r"^#{4,5}\s+.*(?:Descri[çc][ãa]o|Description|User Story|Hist[óo]ria)", stripped, re.IGNORECASE):
                current_section = 'desc'
                i += 1
                continue
            elif re.search(r"^#{4,5}\s+.*(?:Crit[ée]rios de Aceite|Acceptance Criteria)", stripped, re.IGNORECASE):
                current_section = 'acceptance'
                i += 1
                continue
            elif re.search(r"^#{4,5}\s+.*(?:Tarefas T[ée]cnicas|Tasks|Child Tasks)", stripped, re.IGNORECASE):
                current_section = 'tasks'
                i += 1
                continue

            # Acumula linhas de acordo com a seção atual
            if current_section == 'desc':
                if not stripped.startswith("---") and not stripped.startswith("* **"):
                    desc_buffer.append(line)
            elif current_section == 'acceptance':
                if not stripped.startswith("---") and not stripped.startswith("* **"):
                    acceptance_buffer.append(line)
            elif current_section == 'tasks':
                if stripped.startswith("- [ ]") or stripped.startswith("* [ ]") or stripped.startswith("- ") or stripped.startswith("* **Task") or stripped.startswith("* **[TASK") or stripped.startswith("* *Descri") or "descrição:" in stripped.lower() or "descricao:" in stripped.lower():
                    task_buffer.append(stripped)

        # Se estamos dentro de uma Feature
        elif current_feature is not None:
            start_date_match = re.search(r"^(?:[>\*\s]*)\*\*(?:Start Date|Data de In[íi]cio)[^\*]*:?\*\*:?\s*`?([^`\n]+)`?", stripped, re.IGNORECASE)
            if start_date_match:
                current_feature.start_date = _parse_date(start_date_match.group(1))
                i += 1
                continue

            target_date_match = re.search(r"^(?:[>\*\s]*)\*\*(?:Target Date|End Date|Data de T[ée]rmino|Data Alvo)[^\*]*:?\*\*:?\s*`?([^`\n]+)`?", stripped, re.IGNORECASE)
            if target_date_match:
                current_feature.target_date = _parse_date(target_date_match.group(1))
                i += 1
                continue

            tags_match = re.search(r"^\*?\s*\*\*Tags?:?\*\*:?\s*(.+)", stripped, re.IGNORECASE)
            if tags_match:
                current_feature.tags = _parse_tags(tags_match.group(1))
                i += 1
                continue

            desc_match = re.search(r"^\*?\s*\*\*(?:Descri[çc][ãa]o|Description)[^\*]*:?\*\*:?\s*(.+)", stripped, re.IGNORECASE)
            if desc_match:
                current_feature.description = _markdown_to_clean_html(desc_match.group(1))
                i += 1
                continue

        # Se estamos no cabeçalho do Epic (antes da primeira feature)
        elif current_feature is None and current_pbi is None:
            start_date_match = re.search(r"^(?:[>\*\s]*)\*\*(?:Start Date|Data de In[íi]cio)[^\*]*:?\*\*:?\s*`?([^`\n]+)`?", stripped, re.IGNORECASE)
            if start_date_match:
                epic_item.start_date = _parse_date(start_date_match.group(1))
                i += 1
                continue

            target_date_match = re.search(r"^(?:[>\*\s]*)\*\*(?:Target Date|End Date|Data de T[ée]rmino|Data Alvo)[^\*]*:?\*\*:?\s*`?([^`\n]+)`?", stripped, re.IGNORECASE)
            if target_date_match:
                epic_item.target_date = _parse_date(target_date_match.group(1))
                i += 1
                continue

            tags_match = re.search(r"^\*?\s*\*\*Tags?:?\*\*:?\s*(.+)", stripped, re.IGNORECASE)
            if tags_match:
                epic_item.tags = _parse_tags(tags_match.group(1))
                i += 1
                continue

            desc_match = re.search(r"^\*?\s*\*\*(?:Descri[çc][ãa]o|Description)[^\*]*:?\*\*:?\s*(.+)", stripped, re.IGNORECASE)
            if desc_match:
                epic_item.description = _markdown_to_clean_html(desc_match.group(1))
                i += 1
                continue

        i += 1

    # Fecha o último PBI e Feature
    flush_feature()

    # Remove features vazias
    epic_item.features = [f for f in epic_item.features if f.pbis]

    # Calcula agregações para Features e Epic
    total_epic_effort = 0.0
    for feat in epic_item.features:
        feat_effort = sum(p.story_points for p in feat.pbis)
        feat.effort = feat_effort
        total_epic_effort += feat_effort

        # Prioridade da Feature = maior prioridade (menor número) dos seus PBIs
        if feat.pbis:
            feat.priority = min(p.priority for p in feat.pbis)
            feat.business_value = _priority_to_business_value(feat.priority)

    epic_item.effort = total_epic_effort

    return BacklogDocument(
        discipline=discipline,
        epic=epic_item,
        raw_file_path=file_path
    )
