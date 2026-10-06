# Notas sobre a gravação de imagem do Windows 64 bits (modo UEFI / GPT)

[English (UK)](0005-notes-windows-64-bit-image-deployment-uefi-gpt.md)

Este procedimento é adequado para imagens do Windows de **64 bits** e aproveita a arquitetura UEFI nativa da placa Advantech AIMB-216.

## 1. Requisitos

- Imagem do Windows (`.win` ou `.wim`) de 64 bits.
- Host de 64 bits (computador no qual o procedimento é executado).
- SSD zerado.

## 2. Particionamento do SSD (Diskpart)

No Prompt de Comando (cmd) como Administrador, execute o `diskpart` e insira os comandos sequencialmente.

**Atenção:** antes de executar `clean`, use `list disk` para confirmar que o disco de destino é o disco 0.

```cmd
diskpart
select disk 0
clean
convert gpt
create partition efi size=100
format quick fs=fat32 label="System"
assign letter="S"
create partition msr size=16
create partition primary
format quick fs=ntfs label="Windows"
assign letter="W"
exit
```

## 3. Aplicação da imagem (DISM)

Aplique a imagem do Windows na partição principal (`W:`). Substitua `D:\sua_imagem.win` pelo caminho correto do arquivo de imagem.

```cmd
dism /Apply-Image /ImageFile:D:\sua_imagem.win /Index:1 /ApplyDir:W:
```

## 4. Configuração do boot (Bcdboot)

Gere os arquivos de inicialização na partição EFI (`S:`):

```cmd
bcdboot W:\Windows /s S: /f UEFI
```

**Dica:** se houver falha de cópia por conta da localidade, force o idioma com o parâmetro `/l pt-br` ou `/l en-us`.

## 5. Configuração na BIOS (placa AIMB-216)

Para inicializar de forma otimizada em modo UEFI:

1. Ligue o equipamento e pressione **<Del>** durante a inicialização (POST) para acessar o BIOS Setup.
2. Certifique-se de que a prioridade de inicialização na aba Boot esteja configurada para a partição **Windows Boot Manager**.
3. Pressione **<F10>** para salvar as alterações e sair.
