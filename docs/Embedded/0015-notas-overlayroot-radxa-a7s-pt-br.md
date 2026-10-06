# Notas sobre configuração e operação do OverlayRoot na Radxa A7S

[English](./0015-notes-overlayroot-radxa-a7s.md)

## 1. Ordem Ideal de Configuração
Para evitar dores de cabeça, o `overlayroot` deve ser a **última** configuração aplicada ao equipamento, quando ele já estiver pronto para produção. Siga esta ordem:
1. Particionar o disco (SD Card, SSD ou HD).
2. Criar as pastas de montagem.
3. Configurar o arquivo `/etc/fstab` com regras de segurança (`noexec`).
4. Instalar e testar o seu programa (na partição do sistema).
5. Instalar e ativar o `overlayroot`.

## 2. Particionamento e Formatação (Windows 11 + WSL + GParted)
O Windows nativo não manipula partições `ext4` (padrão Linux). Usaremos o WSL para acessar o disco fisicamente e redimensioná-lo.

1. Abra o PowerShell como Administrador no Windows e instale o gerenciador de USB:
   `winget install --interactive --exact dorssel.usbipd-win`
2. Liste os dispositivos USB e anote o "BUSID" do leitor de cartão/HD:
   `usbipd list`
3. Compartilhe e anexe o dispositivo ao WSL:
   `usbipd bind --busid <BUSID>`
   `usbipd attach --wsl --busid <BUSID>`
4. Abra o terminal do seu WSL (ex: Ubuntu) e instale o GParted:
   `sudo apt update && sudo apt install gparted`
5. Inicie o GParted graficamente:
   `sudo gparted`
6. **No GParted:**
   - Selecione o disco correto no canto superior direito.
   - Clique com o botão direito na partição principal e escolha **"Redimensionar/Mover"**.
   - Diminua o espaço para liberar uma área não alocada.
   - Clique com o botão direito no espaço livre e escolha **"Nova"**.
   - Defina o sistema de arquivos como `ext4` e adicione.
   - Clique no ícone verde "Aplicar" (V) para gravar as mudanças.

## 3. Entendendo o Ponto de Montagem e o fstab
No Linux, não existem letras de unidade como `D:` ou `E:`. Você cria uma pasta comum em qualquer lugar do sistema e usa o arquivo `/etc/fstab` (File System Table) para instruir o Linux a "encaixar" uma partição física dentro daquela pasta durante o boot.

Quando você cria a pasta (ex: `mkdir /dados`), ela é criada na partição principal. Mas, quando a partição externa/nova é montada nela, a pasta passa a ser uma "janela" direta para o outro disco. Tudo que for gravado lá será fisicamente salvo na nova partição.

## 4. Configurando a Montagem Permanente e Segura (fstab)
Após colocar o disco particionado de volta no Radxa e ligá-lo:

1. Identifique o nome exato da nova partição que você criou:
   `lsblk` (Isso listará todos os discos. Ex: `/dev/mmcblk0p3`).
2. Crie a pasta onde o seu programa gravará os dados:
   `mkdir -p /home/radxa/meu_programa/dados`
3. Edite o arquivo fstab:
   `sudo nano /etc/fstab`
4. Adicione a seguinte linha no final do arquivo (aplicando a regra de segurança `noexec`):
   `/dev/mmcblk0p3  /home/radxa/meu_programa/dados  ext4  defaults,noexec  0  2`
   * **Coluna 1:** Dispositivo físico.
   * **Coluna 2:** Caminho da pasta (Ponto de montagem).
   * **Coluna 3:** Sistema de arquivos (`ext4`).
   * **Coluna 4 (Opções):** `defaults` (leitura/escrita padrão) + `noexec` (bloqueia a execução de programas a partir desta partição, melhorando a segurança).
   * **Coluna 5:** Dump (usar `0`).
   * **Coluna 6:** Ordem de checagem de erros (`2` para partições secundárias).
5. Salve (`Ctrl+O`, `Enter`) e saia (`Ctrl+X`).
6. Teste se a configuração funcionou:
   `sudo mount -a`
7. Reinicie a placa para garantir que a partição está sendo montada automaticamente.

## 5. Conceito do OverlayFS e overlayroot
O `overlayroot` empilha duas camadas:
1. **Lowerdir (Inferior):** O disco físico real (protegido como somente-leitura).
2. **Upperdir (Superior):** Uma camada virtual na RAM (`tmpfs`).

Gravações feitas fora das suas partições de dados vão para a RAM e são perdidas ao reiniciar. Como a pasta de dados está configurada no fstab, as gravações nela "furam" o overlay e vão para o disco físico.

## 6. Instalação e Ativação do overlayroot
1. `sudo apt update`
2. `sudo apt install overlayroot`
3. `sudo nano /etc/overlayroot.conf`
4. Altere `overlayroot=""` para `overlayroot="tmpfs"`
5. Reinicie o Radxa: `sudo reboot`

## 7. Boas Práticas de Arquitetura e Atualização
**Onde manter o executável?**
Para manter a máquina industrial à prova de falhas (quedas de energia e corrupção de dados), o executável do seu programa **deve ficar na partição principal** (que é congelada pelo `overlayroot`). Apenas arquivos de log, bancos de dados e relatórios devem ir para a partilha de `/dados`.

Como a partição de dados foi montada com a flag `noexec` no fstab, nenhum arquivo malicioso ou corrompido poderá ser executado de lá.

**Para atualizar o executável remotamente (WinSCP + SSH):**
1. Envie o novo arquivo executável via WinSCP para o Radxa (ele cairá na RAM).
2. Via terminal, destrave o disco físico original oculto:
   `sudo mount -o remount,rw /media/root-ro`
3. Copie o executável para dentro do sistema físico real:
   `sudo cp /home/radxa/novo_executavel /media/root-ro/home/radxa/meu_programa/executavel_principal`
4. Tranque o sistema novamente como somente-leitura:
   `sudo mount -o remount,ro /media/root-ro`
