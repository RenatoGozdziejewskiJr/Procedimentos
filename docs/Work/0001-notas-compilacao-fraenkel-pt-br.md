# Notas sobre a compilação do Fraenkel

[English (UK)](0001-notes-fraenkel-build.md)

## 1. Compilação do Core

Execute `update-core-interfaces.py` em `Build Tools\Releases\Windows XP, win32 (1)`, usando o Prompt de Comando com privilégios de Administrador:

```cmd
py -2.7 update-core-interfaces.py
```

Em seguida, execute `update-component-interfaces.py millikan-components.txt` no mesmo diretório e Prompt de Comando:

```cmd
py -2.7 update-component-interfaces.py millikan-components.txt
```

Compile a solução Core no Visual Studio 2013, primeiro em Release e depois em Debug.

## 2. Compilação dos Components

Execute `local-core-release.py` em `Build Tools\Releases\Windows XP, win32 (1)`, usando o Prompt de Comando com privilégios de Administrador:

```cmd
py -2.7 local-core-release.py
```

Compile a solução Components no Visual Studio 2013, primeiro em Release e depois em Debug.

## 3. Agrupamento das DLLs

Exclua o diretório `Sortex` na raiz do repositório, caso exista.

Usando Bash:

```bash
alias python='winpty python.exe'
touch .bashrc
cd Build\ Tools/Releases/Windows\ XP,\ win32\ (1)
  python collect-application.py millikan-components.txt ../../../
```

Como alternativa, use o Prompt de Comando:

```cmd
py -2.7 collect-application.py millikan-components.txt ../../../
```

### 3.1 Cópia das DLLs do Boost

//release

```bash
cp /c/boost/boost_1_61_0/stage/lib/boost_chrono-vc120-mt-1_61.dll ../../../Sortex/sc_app
cp /c/boost/boost_1_61_0/stage/lib/boost_system-vc120-mt-1_61.dll ../../../Sortex/sc_app
cp /c/boost/boost_1_61_0/stage/lib/boost_thread-vc120-mt-1_61.dll ../../../Sortex/sc_app
```

Como alternativa:

```cmd
copy c:\boost\boost_1_61_0\stage\lib\boost_chrono-vc120-mt-1_61.dll ..\..\..\Sortex\sc_app
copy c:\boost\boost_1_61_0\stage\lib\boost_system-vc120-mt-1_61.dll ..\..\..\Sortex\sc_app
copy c:\boost\boost_1_61_0\stage\lib\boost_thread-vc120-mt-1_61.dll ..\..\..\Sortex\sc_app
```

//debug

```bash
cp /c/boost/boost_1_61_0/stage/lib/boost_chrono-vc120-mt-gd-1_61.dll ../../../Sortex/sc_app_d
cp /c/boost/boost_1_61_0/stage/lib/boost_system-vc120-mt-gd-1_61.dll ../../../Sortex/sc_app_d
cp /c/boost/boost_1_61_0/stage/lib/boost_thread-vc120-mt-gd-1_61.dll ../../../Sortex/sc_app_d
```

Como alternativa:

```cmd
copy c:\boost\boost_1_61_0\stage\lib\boost_chrono-vc120-mt-gd-1_61.dll ..\..\..\Sortex\sc_app_d
copy c:\boost\boost_1_61_0\stage\lib\boost_system-vc120-mt-gd-1_61.dll ..\..\..\Sortex\sc_app_d
copy c:\boost\boost_1_61_0\stage\lib\boost_thread-vc120-mt-gd-1_61.dll ..\..\..\Sortex\sc_app_d
```

### 3.2 Criação e cópia dos arquivos INI

Crie os arquivos `.ini`:

```bash
python create-components-ini.py millikan-components.txt
```

Como alternativa:

```cmd
py -2.7 create-components-ini.py millikan-components.txt
```

Copie os arquivos `components.ini` dos diretórios Debug e Release para os respectivos diretórios em `Sortex\` (localize os arquivos `components.ini` nos diretórios Debug e Release):

```bash
cp Release/components.ini ../../../Sortex/sc_app
cp Debug/components.ini ../../../Sortex/sc_app_d
```

Como alternativa:

```cmd
copy Release\components.ini ..\..\..\Sortex\sc_app
copy Debug\components.ini ..\..\..\Sortex\sc_app_d
```

## 4. Cópia de arquivos após a compilação

Para facilitar a atualização após compilar um projeto específico, adicione comandos como os seguintes aos eventos de post-build:

```cmd
cd $(OutputPath)
copy *.pdb "$(SolutionDir)..\Sortex\sc_app_d" /Y
copy *.dll "$(SolutionDir)..\Sortex\sc_app_d" /Y
```

Como alternativa:

```cmd
for %%e in (pdb dll) do copy *.%%e "$(SolutionDir)..\Sortex\sc_app_d" /Y
```

Isso copia os arquivos para o diretório `Sortex` especificado:

```cmd
@echo off
echo "----------------------- copying *.pdb / *.dll files"
cd $(OutputPath)
copy *.pdb "$(SolutionDir)..\Sortex\sc_app_d" /Y
copy *.dll "$(SolutionDir)..\Sortex\sc_app_d" /Y
echo "-----------------------"
@echo on
cd $(HerbertDir)
copy "$(HerbertDir)code\version.h" "$(TargetDir)"
"$(BuildToolsDir)Releases/$(FraenkelPlatformName)/update-releases.py" -b "$(TargetFileName)" -t "Debug"
```
