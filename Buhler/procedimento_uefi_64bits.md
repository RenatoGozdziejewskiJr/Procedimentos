# Procedimento de Gravação de Imagem do Windows (Modo UEFI / GPT)

Este procedimento é adequado para imagens do Windows de **64 bits**, tirando proveito nativo da arquitetura UEFI da placa Advantech AIMB-216.

## Requisitos
- Imagem do Windows (`.win` ou `.wim`) de 64 bits.
- Host (computador onde o procedimento é executado) de 64 bits.
- SSD zerado.

## Passo 1: Particionamento do SSD (Diskpart)
No prompt de comando (cmd) como Administrador, execute o `diskpart` e insira os comandos sequencialmente.
*(Atenção: verifique se o disco alvo é realmente o disco 0 utilizando `list disk` antes de aplicar o comando `clean`)*.

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

## Passo 2: Aplicação da Imagem (DISM)
Aplique a imagem do Windows na partição principal (`W:`). Substitua o caminho `D:\sua_imagem.win` pelo local correto do seu arquivo.

```cmd
dism /Apply-Image /ImageFile:D:\sua_imagem.win /Index:1 /ApplyDir:W:```

## Passo 3: Configuração do Boot (Bcdboot)
Gere os arquivos de inicialização na partição EFI (`S:`).

```cmd
bcdboot W:\Windows /s S: /f UEFI
```

*(Dica: Se houver falha de cópia por conta de localidade, force o idioma com o parâmetro `/l pt-br` ou `/l en-us`)*.

## Passo 4: Configuração na BIOS (Placa AIMB-216)
Para inicializar de forma otimizada em modo UEFI:
1. Ligue o equipamento e pressione **<Del>** durante a inicialização (POST) para acessar o BIOS Setup.
2. Certifique-se de que a prioridade de inicialização na guia de Boot esteja configurada para a partição "Windows Boot Manager".
3. Pressione **<F10>** para salvar as alterações e sair.
