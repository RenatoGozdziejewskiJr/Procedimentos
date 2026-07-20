GIT:
create the branch: git checkout -b <newBranch>  
add the change: git add <files>
commit the change: git commit -m "feat: add hat wobble #12345"
label: feat, fix, docs, style, refactor, test chore
update the development branch: git fetch origin develop:develop 
rebase: git rebase -i develop
squash the commits
push the new branch remotely: git push origin  <newBranch> -f

Tip: Use the following command while being on "master", to list merged branches:
$ git branch --merged | grep -v "\*"

Rename branch: 
checkout no branch que será renomeado: git checkout <branch>
novo nome: git branch -m "novo-nome"

Remove branch:
git branch -d nome-do-branch

Diff only file names:
 git diff --name-only

Branch names: 
usar hyphens '-' 
não usar camel case
usar '/' para agrupar em folders. 
nomes dos folders: feature/ refactor/, chore/, hotfix/, fix/

Reseta branch local:

# 1. Atualiza as informações do repositório remoto sem alterar seus arquivos
git fetch origin

# 2. Força a sua branch local a ficar idêntica à branch remota
git reset --hard origin/nome-da-sua-branch

---
configura credencial Local:

git config --local credential.useHttpPath true
git config --local credential.username RenatoGozdziejewskiJr
git push