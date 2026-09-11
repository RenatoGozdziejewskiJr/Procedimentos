# Geração de Dados de Estatísticas para Millikan e Merlin

Este procedimento descreve como usar o script `generateStats.py` para gerar dados aleatórios de estatísticas em máquinas Millikan e Merlin.

O script grava os dados no banco `statistics.sqlite`. Como o caminho do banco é relativo, o comando deve ser executado dentro do diretório `Sortex/sc_app/storage`.

## Pré-requisitos

- Python instalado na máquina.
- Arquivo `generateStats.py` disponível.
- Banco `statistics.sqlite` existente em `Sortex/sc_app/storage`.
- Tabelas abaixo existentes no banco:
  - `string_table`
  - `ejector_rate_per_defect_per_division_short`
  - `throughput_per_division_short`

## Códigos de Divisões e Defeitos

O script lê os códigos diretamente da tabela `string_table`. Os registros com os nomes abaixo são usados como divisões, nesta ordem:

1. `PrimaryDivision`
2. `SecondaryDivision`
3. `TertiaryDivision`

Os demais registros com nome preenchido são usados como defeitos, respeitando a ordem em que foram inseridos na tabela. O script aceita no máximo oito defeitos.

Quando existem menos de oito defeitos, as posições restantes recebem o código do registro cujo nome é vazio ou contém somente espaços. Nessas posições, o valor de `ejector_rate` é gravado como `NULL`.

O script valida esses códigos antes de apagar ou gerar dados. A execução é interrompida se faltar uma divisão, se houver mais de oito defeitos ou se o código do nome vazio necessário não estiver definido.

## Atenção

Antes de gerar os dados, o script apaga os registros existentes no intervalo informado nas duas tabelas. Faça uma cópia de segurança do banco antes da execução.

```bash
cd Sortex/sc_app/storage
cp statistics.sqlite statistics.sqlite.bak
```

## Preparação

Copie o script para o diretório que contém o banco:

```bash
cp /caminho/para/generateStats.py Sortex/sc_app/storage/
cd Sortex/sc_app/storage
```

Confirme que o script e o banco estão no diretório atual:

```bash
ls -l generateStats.py statistics.sqlite
```

## Execução

Execute o script informando a data e a hora inicial e final no formato `YYYY-MM-DD HH:MM`:

```bash
python generateStats.py 'YYYY-MM-DD HH:MM' 'YYYY-MM-DD HH:MM'
```

Exemplo para gerar um registro por minuto durante uma hora:

```bash
python generateStats.py '2026-09-11 10:00' '2026-09-11 11:00'
```

As datas inicial e final são inclusivas. Portanto, o exemplo acima gera 61 registros em cada tabela.

Se o comando `python` não estiver disponível e a máquina usar Python 3, execute:

```bash
python3 generateStats.py '2026-09-11 10:00' '2026-09-11 11:00'
```

## Resultado Esperado

Quando a conexão e as tabelas forem encontradas, a saída será semelhante a:

```text
Connection ok. All required tables found.
Tables cleared for the specified period.
Inserted 61 records into the database.
Data generation completed.
```

O script gera dados para três divisões e grava um registro por minuto nas tabelas de taxa de ejetores e throughput.

## Solução de Problemas

### Mensagem `Table not found.`

Confirme se o comando está sendo executado dentro de `Sortex/sc_app/storage`, se o arquivo `statistics.sqlite` correto está nesse diretório e se as três tabelas necessárias existem.

### Mensagem `String table error`

Verifique se `string_table` contém os códigos das três divisões, no máximo oito defeitos e um registro com nome vazio quando houver menos de oito defeitos.

### Mensagem `Connection error`

Verifique as permissões de leitura e escrita do arquivo `statistics.sqlite` e do diretório `Sortex/sc_app/storage`.

### Formato de data inválido

Use exatamente o formato `YYYY-MM-DD HH:MM`, mantendo cada data e hora entre aspas.

### Restaurar o banco

Para descartar os dados gerados e restaurar a cópia de segurança:

```bash
cd Sortex/sc_app/storage
cp statistics.sqlite.bak statistics.sqlite
```
