# Configuracao local do Seq com Podman

Este procedimento inicia o Seq localmente com Podman Compose, define o usuario administrador inicial e cria uma API key para ingestao de logs.

## Docker Compose

No `docker-compose.yml`, configure o servico Seq desta forma:

```yaml
services:
  seq:
    image: datalust/seq:2025.2
    environment:
      - ACCEPT_EULA=Y
      - SEQ_FIRSTRUN_ADMINUSERNAME=admin
      - SEQ_FIRSTRUN_ADMINPASSWORDHASH=COLE_O_HASH_AQUI
    ports:
      - '5341:80'
    volumes:
      - seqvol:/data

volumes:
  seqvol:
```

A porta `80` e interna ao container. Com o mapeamento acima, o Seq fica disponivel no host em `http://localhost:5341`.

Na sintaxe de lista usada em `environment`, nao inclua aspas apos o sinal `=`. Por exemplo, use `- SEQ_FIRSTRUN_ADMINPASSWORDHASH=hash` e nao `- SEQ_FIRSTRUN_ADMINPASSWORDHASH="hash"`, pois as aspas seriam enviadas como parte do valor e invalidariam o hash Base64.

## Gerar o hash da senha do administrador

O comando `config hash` le a senha pela entrada padrao. No PowerShell, execute:

```powershell
"UmaSenhaForte" | podman run -i --rm datalust/seq:2025.2 config hash
```

Copie a saida para `SEQ_FIRSTRUN_ADMINPASSWORDHASH`. A configuracao `SEQ_FIRSTRUN_ADMINUSERNAME` e `SEQ_FIRSTRUN_ADMINPASSWORDHASH` so e aplicada quando o volume de dados e criado pela primeira vez.

Para apagar os dados locais e repetir a inicializacao:

```powershell
podman compose down -v
podman compose up -d
```

Para apenas iniciar ou parar o servico sem apagar dados:

```powershell
podman compose up -d
podman compose down
```

## Criar uma API key sem CLI

Para desenvolvimento local, a forma mais pratica de criar uma API key e pela propria interface do Seq, sem instalar um CLI adicional:

1. Acesse `http://localhost:5341` e autentique-se com o usuario administrador.
2. Abra **Data > Ingestion**.
3. Selecione **Add API key**.
4. Defina um nome para a aplicacao, por exemplo `joint-forces-local`.
5. Conceda a permissao **Ingest**.
6. Salve e copie o token exibido. Ele e mostrado uma unica vez.

Cada aplicacao ou ambiente deve ter sua propria API key. Armazene o token em uma configuracao local ou gerenciador de segredos, nunca em arquivos versionados.

> O executavel `seq` dentro do container e o comando GNU/Linux para gerar sequencias numericas. Ele nao e o cliente administrativo do Datalust e nao cria API keys.