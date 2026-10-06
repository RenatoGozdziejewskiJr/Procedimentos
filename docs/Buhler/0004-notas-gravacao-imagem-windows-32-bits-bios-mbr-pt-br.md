# Notas sobre a gravação de imagem do Windows 32 bits (modo BIOS / MBR)

[English (UK)](0004-notes-windows-32-bit-image-deployment-bios-mbr.md)

Este procedimento é **obrigatório** quando o host que executa o processo é de 64 bits e a imagem a ser gravada é de **32 bits**. Ele também contorna a limitação técnica de que firmwares UEFI de 64 bits não conseguem inicializar sistemas operacionais de 32 bits.

## 1. Requisitos

- Imagem do Windows (`.win` ou `.wim`) de 32 bits.
- SSD zerado.
- Placa-mãe com suporte a CSM (Compatibility Support Module) ativado, como a Advantech AIMB-216.

## 2. Particionamento do SSD (Diskpart)

No Prompt de Comando (cmd) como Administrador, execute o `diskpart` e insira os comandos sequencialmente para criar uma tabela de partição MBR clássica.

**Atenção:** antes de executar `clean`, use `list disk` para confirmar que o disco de destino é o disco 0.

```cmd
diskpart
select disk 0
clean
convert mbr
create partition primary size=100
format quick fs=ntfs label="System"
assign letter="S"
active
create partition primary
format quick fs=ntfs label="Windows"
assign letter="W"
exit
```

**Nota crítica:** o comando `active` é fundamental no particionamento MBR, pois indica à BIOS qual partição contém o carregador de inicialização.

## 3. Aplicação da imagem (DISM)

Aplique a imagem do Windows na partição principal (`W:`). Substitua `D:\sua_imagem.win` pelo caminho correto do arquivo de imagem.

```cmd
dism /Apply-Image /ImageFile:D:\sua_imagem.win /Index:1 /ApplyDir:W:
```

## 4. Configuração do boot (Bcdboot)

Como a imagem é de 32 bits e o host atual é de 64 bits, force a geração dos arquivos de boot clássicos (Legacy/BIOS) usando o parâmetro apropriado:

```cmd
bcdboot W:\Windows /s S: /f BIOS
```

## 5. Configuração obrigatória na BIOS (placa AIMB-216)

O sistema da Advantech não inicializará o disco MBR recém-criado sem ativar o suporte a sistemas legados.

1. Ligue o equipamento e pressione **<Del>** durante o POST para acessar o BIOS Setup.
2. Navegue com as setas até a aba **Advanced** e selecione **Compatibility Support Module Configuration**.
3. Pressione Enter em **CSM Support** e altere o valor para **Enabled**.
4. Localize **Boot Options Filter** e ajuste para priorizar **Legacy ROM**.
5. Pressione **<F10>** para salvar as alterações e reiniciar o equipamento.
