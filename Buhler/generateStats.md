# Geração de Dados de Estatísticas para Millikan e Merlin

Este procedimento descreve como usar o script `generateStats.py` para gerar dados aleatórios de estatísticas em máquinas Millikan e Merlin.

O script grava os dados no banco `statistics.sqlite`. Como o caminho do banco é relativo, o comando deve ser executado dentro do diretório `Sortex/sc_app/storage`.

## Pré-requisitos

- Python instalado na máquina.
- Arquivo `generateStats.py` disponível.
- Banco `statistics.sqlite` existente em `Sortex/sc_app/storage`.
- Tabelas abaixo existentes no banco:
  - `ejector_rate_per_defect_per_division_short`
  - `throughput_per_division_short`

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
Connection ok. Both tables found.
Tables cleared for the specified period.
Inserted 61 records into the database.
Data generation completed.
```

O script gera dados para três divisões e grava um registro por minuto nas tabelas de taxa de ejetores e throughput.

## Solução de Problemas

### Mensagem `Table not found.`

Confirme se o comando está sendo executado dentro de `Sortex/sc_app/storage` e se o arquivo `statistics.sqlite` correto está nesse diretório.

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
