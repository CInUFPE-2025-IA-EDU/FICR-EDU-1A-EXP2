#!/usr/bin/env python3
import argparse, os, sys
import pandas as pd
import yaml
from github import Github

DEFAULTS = {
    "Descricao": "Descreva brevemente o objetivo desta tarefa.",
    "Entregaveis": "- Código funcional\n- Prints ou GIF breve\n- README atualizado (se aplicável)",
    "Criterios": "- Passar nos checks: ESLint, Prettier e html-validate\n- Atender aos requisitos funcionais\n- Seguir padrão de branch e PR",
    "Arquivos": "src/index.html, src/styles.css, src/main.js",
    "Comando": "npm run check",
    "Branch": "feat/aluno-<IdAluno>-<slug>-<COMIA|SEMIA>",
    "TituloPR": "[Semana {Semana}] {Tarefa} ({Id} - Squad {Squad} - {IA})",
    "Revisor": "@wagnerjohnatan",
    "Obs": "Preencha Id Aluno, Squad e IA no PR template."
}

def load_mapping(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        y = yaml.safe_load(f) or {}
    return y.get("mappings", {})

def slugify(text):
    import re
    s = re.sub(r"[^a-zA-Z0-9]+", "-", str(text).strip().lower())
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "tarefa"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--token", required=True)
    ap.add_argument("--excel", required=True)
    ap.add_argument("--students", default=None)
    ap.add_argument("--ia-default", default="SEMIA")
    args = ap.parse_args()

    g = Github(args.token)
    repo = g.get_repo(args.repo)

    mapping = load_mapping(args.students) if args.students else {}

    if not os.path.exists(args.excel):
        print(f"[ERRO] Excel não encontrado: {args.excel}", file=sys.stderr)
        sys.exit(1)

    df = pd.read_excel(args.excel)
    required = ["Semana","Id Aluno","SQUAD","Tarefa"]
    miss = [c for c in required if c not in df.columns]
    if miss:
        print(f"[ERRO] Faltam colunas no Excel: {miss}", file=sys.stderr)
        sys.exit(1)

    # cria extras se faltarem
    extras = ["Descrição","Entregáveis","Critérios de Aceite","Arquivos Sugeridos","Comando de Verificação","Branch Sugerida","Título do PR","Revisor","Observações","IA"]
    for c in extras:
        if c not in df.columns:
            df[c] = None

    for _, r in df.iterrows():
        semana = str(r.get("Semana","")).strip()
        idaluno = str(r.get("Id Aluno","")).strip()
        squad = str(r.get("SQUAD","")).strip()
        tarefa = str(r.get("Tarefa","")).strip()
        ia = str(r.get("IA") or args.ia_default).strip().upper()
        if ia not in ("COMIA","SEMIA"):
            ia = args.ia_default.upper()

        desc = r.get("Descrição") or DEFAULTS["Descricao"]
        entreg = r.get("Entregáveis") or DEFAULTS["Entregaveis"]
        crit = r.get("Critérios de Aceite") or DEFAULTS["Criterios"]
        arq = r.get("Arquivos Sugeridos") or DEFAULTS["Arquivos"]
        cmd = r.get("Comando de Verificação") or DEFAULTS["Comando"]
        branch_sug = r.get("Branch Sugerida") or DEFAULTS["Branch"]
        pr_title = r.get("Título do PR") or DEFAULTS["TituloPR"].format(Semana=semana, Tarefa=tarefa, Id=idaluno, Squad=squad, IA=ia)
        revisor = r.get("Revisor") or DEFAULTS["Revisor"]
        obs = r.get("Observações") or DEFAULTS["Obs"]

        labels = ["tarefa", f"Semana:{semana}", f"SQUAD:{squad}", f"IdAluno:{idaluno}", f"IA:{ia}"]

        # ensure labels
        for lb in labels:
            try:
                repo.get_label(lb)
            except:
                try:
                    repo.create_label(name=lb, color="6E5494")
                except Exception as e:
                    print(f"[WARN] Label {lb}: {e}")

        assignees = []
        mp = mapping.get(str(idaluno))
        if isinstance(mp, dict) and mp.get("login"):
            assignees = [mp["login"]]

        body = (
            f"**Descrição**\n{desc}\n\n"
            f"**Entregáveis**\n{entreg}\n\n"
            f"**Critérios de Aceite**\n{crit}\n\n"
            f"**Arquivos Sugeridos**\n{arq}\n\n"
            f"**Comando de Verificação**\n`{cmd}`\n\n"
            f"**Branch Sugerida**\n`{branch_sug}`\n\n"
            f"**Título do PR**\n{pr_title}\n\n"
            f"**Revisor**\n{revisor}\n\n"
            f"**Observações**\n{obs}\n"
        )

        title = f"[Semana {semana}] {tarefa} ({idaluno} - Squad {squad} - {ia})"

        print(f"→ Criando issue: {title} | assignees={assignees} | labels={labels}")
        try:
            repo.create_issue(
                title=title,
                body=body,
                labels=labels,
                assignees=assignees
            )
        except Exception as e:
            print(f"[ERRO] Falha ao criar issue '{title}': {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
