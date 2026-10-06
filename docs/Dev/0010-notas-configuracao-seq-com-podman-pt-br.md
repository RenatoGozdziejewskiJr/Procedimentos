# Notas sobre a configuração local do Seq com Podman

[English (UK)](0010-notes-podman-seq-configuration.md)

Este procedimento inicia o Seq localmente com Podman Compose, define o usuário administrador inicial e cria uma API key para ingestão de logs.

## 1. Docker Compose

No `docker-compose.yml`, configure o serviço Seq desta forma:

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

A porta `80` é interna ao contêiner. Com o mapeamento acima, o Seq fica disponível no host em `http://localhost:5341`.

Na sintaxe de lista usada em `environment`, não inclua aspas após o sinal `=`. Por exemplo, use `- SEQ_FIRSTRUN_ADMINPASSWORDHASH=hash` e não `- SEQ_FIRSTRUN_ADMINPASSWORDHASH="hash"`, pois as aspas seriam enviadas como parte do valor e invalidariam o hash Base64.

## 2. Gerar o hash da senha do administrador

O comando `config hash` lê a senha pela entrada padrão. No PowerShell, execute:

```powershell
"UmaSenhaForte" | podman run -i --rm datalust/seq:2025.2 config hash
```

Copie a saída para `SEQ_FIRSTRUN_ADMINPASSWORDHASH`. As configurações `SEQ_FIRSTRUN_ADMINUSERNAME` e `SEQ_FIRSTRUN_ADMINPASSWORDHASH` só são aplicadas quando o volume de dados é criado pela primeira vez.

Para apagar os dados locais e repetir a inicialização:

```powershell
podman compose down -v
podman compose up -d
```

Para apenas iniciar ou parar o serviço sem apagar dados:

```powershell
podman compose up -d
podman compose down
```

## 3. Criar uma API key sem CLI

Para desenvolvimento local, a forma mais prática de criar uma API key é pela própria interface do Seq, sem instalar um CLI adicional:

1. Acesse `http://localhost:5341` e autentique-se com o usuário administrador.
2. Abra **Data > Ingestion**.
3. Selecione **Add API key**.
4. Defina um nome para a aplicação, por exemplo `joint-forces-local`.
5. Conceda a permissão **Ingest**.
6. Salve e copie o token exibido. Ele é mostrado uma única vez.

Cada aplicação ou ambiente deve ter sua própria API key. Armazene o token em uma configuração local ou em um gerenciador de segredos, nunca em arquivos versionados.

> O executável `seq` dentro do contêiner é o comando GNU/Linux para gerar sequências numéricas. Ele não é o cliente administrativo do Datalust e não cria API keys.
