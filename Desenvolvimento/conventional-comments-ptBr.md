# Conventional Comments

Resumo rápido baseado em https://conventionalcomments.org/ para padronizar feedback em revisões.

## Objetivo

- Deixar comentários de review mais claros, acionáveis e fáceis de interpretar.
- Reduzir ruído e ambiguidade em PRs.
- Permitir leitura humana e também parsing por ferramentas.

## Formato padrão

Use este formato:

```text
<label> [decorations]: <subject>

[discussion]
```

- label: tipo do comentário.
- decorations (opcional): contexto extra entre parênteses, separado por vírgula.
- subject: mensagem principal.
- discussion (opcional): contexto, motivação e próximos passos.

## Labels recomendadas

- praise: reconhecimento positivo real.
- nitpick: ajuste de preferência, trivial e não bloqueante por natureza.
- suggestion: proposta de melhoria com direção clara.
- issue: problema identificado (funcional, técnico, UX, etc.).
- todo: ajuste pequeno e necessário.
- question: dúvida para validar entendimento/risco.
- thought: ideia de melhoria futura, sem bloqueio.
- chore: tarefa de processo para concluir aceitação.
- note: observação informativa, não bloqueante.

Labels adicionais comuns:

- typo: erro de digitação.
- polish: melhoria de acabamento/qualidade.
- quibble: equivalente leve a nitpick.

## Decorations comuns

- (non-blocking): não deve bloquear aprovação.
- (blocking): deve bloquear aprovação até resolver.
- (if-minor): resolver apenas se a mudança for pequena.

Outras decorations podem ser usadas por contexto técnico, por exemplo:

- (security), (performance), (test), (ux), (docs).

## Boas práticas

- Prefira comentários específicos, com ação clara.
- Em issue, tente incluir uma suggestion quando possível.
- Evite excesso de decorations no mesmo comentário.
- Inclua pelo menos um praise sincero por review quando fizer sentido.

## Referência rápida para mensagens de PR no Azure

Use diretamente no comentário da PR:

```text
suggestion: Podemos extrair este bloco para reduzir duplicação?
```

```text
issue (blocking): Este fluxo quebra quando o token expira.
```

```text
nitpick (non-blocking): Ajustar nome da variável para manter o padrão do módulo.
```

```text
question: Esse endpoint sempre retorna ordenado por data?
```

```text
praise: Ótima cobertura de testes nesse cenário crítico.
```

## Referência rápida para commits Git

Conventional Comments é para comentários de review.
Para commits, o padrão relacionado é Conventional Commits.

Formato:

```text
<type>(<scope opcional>): <descrição curta>
```

Tipos mais usados:

- feat: nova funcionalidade.
- fix: correção de bug.
- docs: documentação.
- refactor: refatoração sem mudança funcional.
- test: testes.
- chore: manutenção/infra.
- perf: melhoria de performance.
- ci: pipeline/automação.

Exemplos:

```text
feat(auth): adiciona renovação automática de token
fix(api): corrige tratamento de timeout no retry
docs(dev): adiciona guia de build do devcontainer
chore(ci): atualiza versão do agente no pipeline
```

## Copiar e colar: 10 mensagens prontas para PR (Azure)

```text
1) issue (blocking): Existe risco de NullReference quando o retorno da API vem vazio.

2) suggestion: Podemos extrair esta validação para um helper e reduzir repetição entre os métodos.

3) question: Esse comportamento foi definido em regra de negócio ou é efeito colateral da implementação atual?

4) nitpick (non-blocking): Renomear esta variável para refletir melhor o conteúdo retornado.

5) todo: Incluir teste cobrindo o cenário de erro 401 para evitar regressão.

6) chore: Ajustar o pipeline para rodar este job também em branches de release.

7) note (non-blocking): Esta mudança impacta o contrato do endpoint e pode afetar consumidores legados.

8) thought (non-blocking): Em uma próxima iteração, vale considerar cache local para reduzir chamadas sequenciais.

9) suggestion (if-minor): Se a alteração for pequena, padronizar mensagens de log conforme os outros módulos.

10) praise: Boa separação de responsabilidades, ficou mais fácil de testar e manter.
```
