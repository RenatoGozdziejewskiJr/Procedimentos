# Notas sobre Conventional Comments

[English (UK)](0007-notes-conventional-comments.md)

Resumo baseado em https://conventionalcomments.org/ para padronizar feedback em revisões.

## 1. Objetivo

- Deixar comentários de review mais claros, acionáveis e fáceis de interpretar.
- Reduzir ruído e ambiguidade em PRs.
- Permitir leitura humana e também parsing por ferramentas.

## 2. Formato padrão

Use este formato:

```text
<label> [decorations]: <subject>

[discussion]
```

- label: tipo do comentário.
- decorations (opcional): contexto adicional entre parênteses, separado por vírgulas.
- subject: mensagem principal.
- discussion (opcional): contexto, motivação e próximos passos.

## 3. Labels recomendadas

- praise: reconhecimento positivo sincero.
- nitpick: ajuste de preferência trivial e naturalmente não bloqueante.
- suggestion: proposta para melhorar a implementação atual.
- issue: problema identificado (funcional, técnico, UX etc.).
- todo: ajuste pequeno e necessário.
- question: dúvida ou pedido de esclarecimento.
- thought: ideia não bloqueante para o futuro.
- chore: tarefa de processo necessária antes da aceitação formal.
- note: observação informativa e não bloqueante.

### 3.1 Labels adicionais comuns

- typo: erro de ortografia.
- polish: melhoria de qualidade ou acabamento.
- quibble: alternativa mais leve a nitpick.

## 4. Decorations comuns

- (non-blocking): não deve bloquear a aprovação.
- (blocking): deve bloquear a aprovação até ser resolvida.
- (if-minor): resolver apenas se a alteração for pequena ou trivial.

Outras decorations podem ser usadas conforme o contexto técnico, por exemplo:

- (security), (performance), (test), (ux), (docs).

## 5. Boas práticas

- Prefira comentários específicos, com uma ação clara.
- Em comentários issue, inclua uma suggestion associada quando possível.
- Evite usar muitas decorations em um único comentário.
- Inclua pelo menos um elogio sincero por review quando fizer sentido.

## 6. Referência rápida para comentários de PR no Azure

Use diretamente nos comentários da PR:

```text
suggestion: Podemos extrair este bloco para reduzir duplicação?
```

```text
issue (blocking): Este fluxo quebra quando o token expira.
```

```text
nitpick (non-blocking): Renomear esta variável para refletir melhor o payload.
```

```text
question: Esse endpoint sempre deve retornar dados ordenados por data?
```

```text
praise: Ótima cobertura de testes para este cenário crítico.
```

## 7. Referência rápida para commits Git

Conventional Comments é para comentários de review. Para mensagens de commit, o padrão relacionado é Conventional Commits.

Formato:

```text
<type>(<scope opcional>): <descrição curta>
```

Tipos mais comuns:

- feat: nova funcionalidade.
- fix: correção de bug.
- docs: documentação.
- refactor: reorganização do código sem mudança funcional.
- test: testes.
- chore: manutenção ou infraestrutura.
- perf: melhoria de desempenho.
- ci: pipeline ou automação.

Exemplos:

```text
feat(auth): adiciona renovação automática de token
fix(api): corrige tratamento de timeout no retry
docs(dev): adiciona guia de build do devcontainer
chore(ci): atualiza versão do agente no pipeline
```

## 8. Copiar e colar: 10 mensagens prontas para PR (Azure)

```text
1) issue (blocking): Existe risco de NullReference quando a resposta da API vem vazia.

2) suggestion: Podemos extrair esta validação para um helper e reduzir duplicação entre os métodos.

3) question: Esse comportamento foi definido por regras de negócio ou é efeito colateral da implementação atual?

4) nitpick (non-blocking): Renomear esta variável para refletir melhor o conteúdo do payload.

5) todo: Incluir testes para o cenário de erro 401 e evitar regressões.

6) chore: Ajustar o pipeline para que este job também execute em branches de release.

7) note (non-blocking): Esta alteração afeta o contrato do endpoint e pode impactar consumidores legados.

8) thought (non-blocking): Em uma próxima iteração, considere cache local para reduzir chamadas sequenciais.

9) suggestion (if-minor): Se for uma alteração pequena, padronizar as mensagens de log conforme os outros módulos.

10) praise: Boa separação de responsabilidades; ficou muito mais fácil testar e manter.
```
