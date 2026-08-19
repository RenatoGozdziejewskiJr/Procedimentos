# Procedimento de Gravação de Imagem do Windows 32 bits (Modo BIOS / MBR)

Este procedimento é **obrigatório** quando o Host executando o processo é de 64 bits e a imagem a ser gravada é de **32 bits**, bem como para contornar a limitação técnica de que firmwares UEFI de 64 bits não conseguem inicializar sistemas de 32 bits.

## Requisitos
- Imagem do Windows (`.win` ou `.wim`) de 32 bits.
- SSD zerado.
- Placa-mãe com suporte a módulo CSM (Compatibility Support Module) ativado, como a Advantech AIMB-216.

## Passo 1: Particionamento do SSD (Diskpart)
No prompt de comando (cmd) como Administrador, execute o `diskpart` e insira os comandos sequencialmente para criar uma tabela de partição MBR clássica.
*(Atenção: verifique se o disco alvo é realmente o disco 0 utilizando `list disk` antes de aplicar o comando `clean`)*.

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
*(Nota Crítica: O comando `active` é fundamental no particionamento MBR para indicar fisicamente à BIOS qual é a partição contendo o carregador de inicialização).*

## Passo 2: Aplicação da Imagem (DISM)
Aplique a imagem do Windows na partição principal (`W:`). Substitua o caminho `D:\sua_imagem.win` pelo local correto do seu arquivo.

```cmd
dism /Apply-Image /ImageFile:D:\sua_imagem.win /Index:1 /ApplyDir:W:```

## Passo 3: Configuração do Boot (Bcdboot)
Como a imagem é de 32 bits e o host atual é de 64 bits, é necessário forçar a geração dos arquivos de boot clássicos (Legacy/BIOS) utilizando o parâmetro respectivo.

```cmd
bcdboot W:\Windows /s S: /f BIOS
```

## Passo 4: Configuração Obrigatória na BIOS (Placa AIMB-216)
O sistema da Advantech não inicializará o disco MBR recém-criado sem ativar o suporte a sistemas legados.

1. Ligue o equipamento e pressione **<Del>** durante o POST para acessar o BIOS Setup.
2. Navegue utilizando as setas direcionais até a aba **Advanced** e selecione a opção **Compatibility Support Module Configuration**.
3. Pressione Enter em **CSM Support** e altere o valor para **Enabled**.
4. Em seguida, localize o item **Boot Options Filter** e ajuste para priorizar **Legacy ROM**.
5. Pressione **<F10>** para salvar as alterações e reiniciar o equipamento.
