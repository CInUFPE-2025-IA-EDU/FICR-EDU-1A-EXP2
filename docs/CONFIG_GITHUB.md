# Configurações no GitHub
1) Branch protection em `main`:
- Require a pull request before merging
- Require approvals = 1
- Require review from Code Owners
- (opcional) Require approval of the most recent reviewable push
- Não marque "Require status checks" até o CI rodar ao menos 1x

2) Actions: Settings → Actions → General
- Allow all actions and reusable workflows
- Workflow permissions: Read and write

3) Seed Issues:
- Actions → Seed Issues from Excel → Run workflow
- `excel_path`: `tasks/planejamento.xlsx`
- `ia_default`: `COMIA` ou `SEMIA`

4) Branch dos alunos:
- `feat/aluno-<IdAluno>-<slug>-COMIA` ou `-SEMIA` (o workflow rotula o PR automaticamente)
