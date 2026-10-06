# Notes about essential Git commands

[Português (Brasil)](./0016-notas-comandos-essenciais-git-pt-br.md)

## 1. Basic workflow and branches

- **Create and switch to a new branch:**
  ```bash
  git checkout -b <nome-da-nova-branch>
  ```
- **Stage changes:**
  ```bash
  git add <arquivos> # ou git add .
  ```
- **Commit changes:** (Use the Conventional Commits types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.)
  ```bash
  git commit -m "feat: add hat wobble #12345"
  ```
- **Push the new branch to the remote repository:**
  ```bash
  git push origin <nome-da-nova-branch>
  # Usar -f apenas se precisar sobrescrever o histórico após um rebase
  ```

## 2. Updating and rebasing
- **Update the local development branch:**
  ```bash
  git fetch origin develop:develop
  ```
- **Run an interactive rebase (for example, to squash commits):**
  ```bash
  git rebase -i develop
  ```

## 3. Branch management

- **Rename a branch:**
  ```bash
  git checkout <branch-antiga>
  git branch -m "novo-nome"
  ```
- **Delete a local branch:**
  ```bash
  git branch -d nome-da-branch
  ```
- **List branches already merged into master:**
  *(Useful for housekeeping.)*
  ```bash
  git branch --merged | grep -v "\*"
  ```

## 4. Reset a local branch
To discard all local changes and make your branch exactly match the remote version:
```bash
# 1. Atualiza as informações do repositório remoto
git fetch origin

# 2. Força a sua branch local a ficar idêntica à remota
git reset --hard origin/nome-da-sua-branch
```

## 5. Other useful commands
- **Show only the names of changed files (without the diff):**
  ```bash
  git diff --name-only
  ```
- **Configure credentials locally (for the current repository only):**
  ```bash
  git config --local credential.useHttpPath true
  git config --local credential.username SeuNomeDeUsuario
  ```

---

## 6. Branch naming conventions

- Use hyphens (`-`) to separate words.
- Do **not** use camelCase.
- Use slashes (`/`) to group branches into logical folders.
- Recommended prefixes:
- `feature/` (new features)
- `refactor/` (code refactoring)
- `chore/` (maintenance tasks, dependencies)
- `hotfix/` or `fix/` (bug fixes)
