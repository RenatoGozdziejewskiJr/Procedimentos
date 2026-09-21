# Geração de Dados de Estatísticas para Millikan e Merlin

Este procedimento descreve como usar o script `generateStats.py` para gerar dados aleatórios de estatísticas em máquinas Millikan e Merlin.

O script grava os dados no banco `statistics.sqlite`. Como o caminho do banco é relativo, o comando deve ser executado dentro do diretório `Sortex/sc_app/storage`.

## Pré-requisitos

- Python instalado na máquina.
- Arquivo `generateStats.py` disponível.
- Módulo `splintco_python` disponível para comunicação com o software da máquina.
- O software do equipamento deve estar em execução (acessível via porta 50713 local).
- Banco `statistics.sqlite` existente em `Sortex/sc_app/storage`.
- Tabelas abaixo existentes no banco:
  - `string_table`
  - `ejector_rate_per_defect_per_division_short`
  - `throughput_per_division_short`

## Códigos de Divisões e Defeitos

O script se conecta ao software da máquina e solicita a lista de defeitos ativa no momento para cada divisão. 

A tabela `string_table` é utilizada apenas para pesquisar o ID numérico correspondente a cada nome de divisão ou defeito. Os seguintes nomes são esperados para as divisões:

1. `PrimaryDivision`
2. `SecondaryDivision`
3. `TertiaryDivision`

Os defeitos retornados pela máquina para cada divisão terão seus IDs pesquisados na `string_table`. O script aceita no máximo oito defeitos por divisão.

Quando uma divisão possui menos de oito defeitos configurados, as posições restantes recebem o código numérico do registro cujo nome é vazio ou contém somente espaços na `string_table`. Nessas posições, o valor de `ejector_rate` é gravado como `NULL`.

O script valida esses dados antes de apagar ou gerar informações. A execução é interrompida se a comunicação com a máquina falhar, se faltar uma divisão na tabela de strings, se houver mais de oito defeitos em uma mesma divisão, ou se o código para o nome vazio não estiver definido.

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

Execute o script informando a data e a hora local inicial e final no formato `YYYY-MM-DD HH:MM`. O script detecta o fuso horário configurado no sistema operacional e converte os valores para UTC antes de consultar ou gravar o banco:

```bash
python generateStats.py 'YYYY-MM-DD HH:MM' 'YYYY-MM-DD HH:MM'
```

Exemplo para gerar um registro por minuto durante uma hora:

```bash
python generateStats.py '2026-09-11 10:00' '2026-09-11 11:00'
```

Em um computador configurado como UTC−3, o intervalo do exemplo será gravado no banco de `2026-09-11 13:00:00` até `2026-09-11 14:00:00` UTC. Em outro país, o resultado será ajustado conforme o fuso local configurado. As datas inicial e final são inclusivas; portanto, serão gerados 61 registros em cada tabela.

Antes de executar, confirme se a data, a hora e o fuso horário do sistema operacional estão corretos.

Se o comando `python` não estiver disponível e a máquina usar Python 3, execute:

```bash
python3 generateStats.py '2026-09-11 10:00' '2026-09-11 11:00'
```

## Resultado Esperado

Quando a conexão e as tabelas forem encontradas, a saída será semelhante a:

```text
UTC period: 2026-09-11 13:00 to 2026-09-11 14:00
Connected successfully.
JSON: {...}
Defect: Chalky Division: PrimaryDivision
Defect: Yellow Division: SecondaryDivision
...
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

Verifique se `string_table` contém os códigos das três divisões, os IDs de todos os defeitos que estão sendo reportados pela máquina em tempo real, e um registro com nome vazio quando houver menos de oito defeitos em qualquer uma das divisões.

### Erros de Conexão com o Equipamento (`Failed to connect` / `Protocol or Connection Error`)

O script precisa obter a lista de defeitos comunicando-se com a máquina na porta 50713. Verifique se o serviço principal do equipamento está sendo executado e respondendo às requisições.

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
