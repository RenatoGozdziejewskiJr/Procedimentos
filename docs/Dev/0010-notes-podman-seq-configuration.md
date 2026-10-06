# Notes about Configuring Seq with Podman

[Português (Brasil)](0010-notas-configuracao-seq-com-podman-pt-br.md)

This procedure starts Seq locally with Podman Compose, sets the initial administrator credentials and creates an API key for log ingestion.

## 1. Docker Compose

In `docker-compose.yml`, configure the Seq service as follows:

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

Port `80` is internal to the container. With the mapping above, Seq is available on the host at `http://localhost:5341`.

In the list syntax used for `environment`, do not add quotation marks after the equals sign. For example, use `- SEQ_FIRSTRUN_ADMINPASSWORDHASH=hash`, not `- SEQ_FIRSTRUN_ADMINPASSWORDHASH="hash"`, because the quotation marks would be sent as part of the value and invalidate the Base64 hash.

## 2. Generating the Administrator Password Hash

The `config hash` command reads the password from standard input. In PowerShell, run:

```powershell
"UmaSenhaForte" | podman run -i --rm datalust/seq:2025.2 config hash
```

Copy the output to `SEQ_FIRSTRUN_ADMINPASSWORDHASH`. The `SEQ_FIRSTRUN_ADMINUSERNAME` and `SEQ_FIRSTRUN_ADMINPASSWORDHASH` settings are applied only when the data volume is created for the first time.

To delete the local data and repeat initialisation:

```powershell
podman compose down -v
podman compose up -d
```

To start or stop the service without deleting data:

```powershell
podman compose up -d
podman compose down
```

## 3. Creating an API Key Without a CLI

For local development, the most practical way to create an API key is through the Seq interface itself, without installing an additional CLI:

1. Go to `http://localhost:5341` and authenticate as the administrator.
2. Open **Data > Ingestion**.
3. Select **Add API key**.
4. Set an application name, for example `joint-forces-local`.
5. Grant the **Ingest** permission.
6. Save and copy the displayed token. It is shown only once.

Each application or environment should have its own API key. Store the token in local configuration or a secret manager, never in version-controlled files.

> The `seq` executable inside the container is the GNU/Linux command for generating numeric sequences. It is not the Datalust administrative client and cannot create API keys.
