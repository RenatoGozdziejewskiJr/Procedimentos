# Notas sobre comandos essenciais do Git

[English](./0016-notes-essential-git-commands.md)

## 1. Fluxo Básico e Branches

- **Criar uma nova branch e mudar para ela:** 
  ```bash
  git checkout -b <nome-da-nova-branch>
  ```
- **Adicionar mudanças:** 
  ```bash
  git add <arquivos> # ou git add .
  ```
- **Fazer o commit:** (Utilize as convenções de conventional commits: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`)
  ```bash
  git commit -m "feat: add hat wobble #12345"
  ```
- **Enviar a branch nova para o repositório remoto:** 
  ```bash
  git push origin <nome-da-nova-branch>
  # Usar -f apenas se precisar sobrescrever o histórico após um rebase
  ```

## 2. Atualização e Rebase
- **Atualizar a branch de desenvolvimento local:** 
  ```bash
  git fetch origin develop:develop
  ```
- **Fazer rebase interativo (ex: para fazer squash de commits):** 
  ```bash
  git rebase -i develop
  ```

## 3. Gerenciamento de Branches

- **Renomear branch:**
  ```bash
  git checkout <branch-antiga>
  git branch -m "novo-nome"
  ```
- **Remover branch local:**
  ```bash
  git branch -d nome-da-branch
  ```
- **Listar branches já mergeadas na master:**
  *(Útil para limpeza)*
  ```bash
  git branch --merged | grep -v "\*"
  ```

## 4. Resetar Branch Local
Para descartar todas as alterações locais e deixar sua branch exatamente igual à versão remota:
```bash
# 1. Atualiza as informações do repositório remoto
git fetch origin

# 2. Força a sua branch local a ficar idêntica à remota
git reset --hard origin/nome-da-sua-branch
```

## 5. Outros Úteis
- **Ver apenas os nomes dos arquivos modificados (sem o conteúdo diff):**
  ```bash
  git diff --name-only
  ```
- **Configurar credenciais localmente (apenas para o repositório atual):**
  ```bash
  git config --local credential.useHttpPath true
  git config --local credential.username SeuNomeDeUsuario
  ```

---

## 6. Convenção de Nomenclatura para Branches

- Use hifens (`-`) para separar palavras.
- **Não** use camelCase.
- Use barras (`/`) para agrupar as branches em pastas lógicas.
- Prefixos de pastas recomendados:
  - `feature/` (Novas funcionalidades)
  - `refactor/` (Refatorações de código)
  - `chore/` (Tarefas de manutenção, dependências)
  - `hotfix/` ou `fix/` (Correção de bugs)
