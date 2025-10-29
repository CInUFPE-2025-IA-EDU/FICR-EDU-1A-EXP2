# FICR-EDU-1A-EXP2
Ambiente de experimento 2 com indicadores por **Id Aluno**, **SQUAD**, **Semana** e **IA (COMIA/SEMIA)**.

## Fluxo
1. Suba o repositório.
2. Ajuste `config/students.yaml`.
3. Coloque o Excel em `tasks/planejamento.xlsx` (ou informe outro caminho no workflow).
4. Actions → **Seed Issues from Excel** → Run workflow.
5. Alunos criam branch: `feat/aluno-<IdAluno>-<slug>-COMIA|SEMIA`.
6. PR dispara CI (ESLint, Prettier, html-validate).

## Indicadores
- PRs/semana
- % falhas CI (entre PRs com checks)
- Tempo até primeira aprovação
- Taxa de retrabalho (Request changes + commits após review)
