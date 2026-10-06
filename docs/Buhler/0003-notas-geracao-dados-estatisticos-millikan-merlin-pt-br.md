# Notas sobre a geração de dados de estatísticas para Millikan e Merlin

[English (UK)](0003-notes-millikan-merlin-statistics-data-generation.md)

## 1. Visão geral

Este procedimento descreve como usar o script `generateStats.py` para gerar dados aleatórios de estatísticas em máquinas Millikan e Merlin.

O script grava os dados no banco `statistics.sqlite`. Como o caminho do banco é relativo, execute o comando dentro do diretório `Sortex/sc_app/storage`.

## 2. Pré-requisitos

- Python instalado na máquina.
- Arquivo `generateStats.py` disponível.
- Módulo `splintco_python` disponível para comunicação com o software da máquina.
- Software do equipamento em execução e acessível localmente pela porta 50713.
- Banco `statistics.sqlite` existente em `Sortex/sc_app/storage`.
- As tabelas abaixo existentes no banco:
  - `string_table`
  - `ejector_rate_per_defect_per_division_short`
  - `throughput_per_division_short`

## 3. Códigos de divisões e defeitos

O script se conecta ao software da máquina e solicita a lista de defeitos ativa no momento para cada divisão.

A tabela `string_table` é utilizada apenas para pesquisar o ID numérico correspondente a cada nome de divisão ou defeito. Os seguintes nomes são esperados para as divisões:

1. `PrimaryDivision`
2. `SecondaryDivision`
3. `TertiaryDivision`

Os IDs dos defeitos retornados pela máquina para cada divisão são pesquisados na `string_table`. O script aceita no máximo oito defeitos por divisão.

Quando uma divisão possui menos de oito defeitos configurados, as posições restantes recebem o código numérico do registro cujo nome é vazio ou contém somente espaços na `string_table`. Nessas posições, o valor de `ejector_rate` é gravado como `NULL`.

O script valida esses dados antes de apagar ou gerar informações. A execução é interrompida se a comunicação com a máquina falhar, se faltar uma divisão na tabela de strings, se houver mais de oito defeitos em uma mesma divisão ou se o código para o nome vazio não estiver definido.

## 4. Atenção

Antes de gerar os dados, o script apaga os registros existentes no intervalo informado nas duas tabelas. Faça uma cópia de segurança do banco antes da execução.

```bash
cd Sortex/sc_app/storage
cp statistics.sqlite statistics.sqlite.bak
```

## 5. Preparação

Copie o script para o diretório que contém o banco:

```bash
cp /caminho/para/generateStats.py Sortex/sc_app/storage/
cd Sortex/sc_app/storage
```

Confirme se o script e o banco estão no diretório atual:

```bash
ls -l generateStats.py statistics.sqlite
```

## 6. Execução

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

## 7. Resultado esperado

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

## 8. Geração do executável (.exe)

Para facilitar a execução do script em ambientes sem a necessidade de instalar as dependências, é possível compilá-lo para um arquivo executável.

### 8.1 Instalação do PyInstaller

Primeiro, instale a ferramenta `pyinstaller`:

```bash
pip install pyinstaller
```

### 8.2 Criação do executável

Para gerar o executável em um único arquivo, incluindo a biblioteca `.pyd` necessária, execute o seguinte comando no mesmo diretório do script:

```bash
pyinstaller --onefile --add-binary "splintco_python.cp311-win_amd64.pyd;." generateStats.py
```

O executável gerado (`generateStats.exe`) será salvo na subpasta `dist/`.

## 9. Solução de problemas

### 9.1 Mensagem `Table not found.`

Confirme se o comando está sendo executado dentro de `Sortex/sc_app/storage`, se o arquivo `statistics.sqlite` correto está nesse diretório e se as três tabelas necessárias existem.

### 9.2 Mensagem `String table error`

Verifique se `string_table` contém os códigos das três divisões, os IDs de todos os defeitos que estão sendo reportados pela máquina em tempo real e um registro com nome vazio quando houver menos de oito defeitos em qualquer uma das divisões.

### 9.3 Erros de conexão com o equipamento (`Failed to connect` / `Protocol or Connection Error`)

O script precisa obter a lista de defeitos comunicando-se com a máquina na porta 50713. Verifique se o serviço principal do equipamento está em execução e respondendo às requisições.

### 9.4 Mensagem `Connection error`

Verifique as permissões de leitura e escrita do arquivo `statistics.sqlite` e do diretório `Sortex/sc_app/storage`.

### 9.5 Formato de data inválido

Use exatamente o formato `YYYY-MM-DD HH:MM`, mantendo cada data e hora entre aspas.

### 9.6 Restaurar o banco

Para descartar os dados gerados e restaurar a cópia de segurança:

```bash
cd Sortex/sc_app/storage
cp statistics.sqlite.bak statistics.sqlite
```
