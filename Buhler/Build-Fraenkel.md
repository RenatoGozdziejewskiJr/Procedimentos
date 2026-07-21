# Build Fraenkel
## Build Core

- Run python update-core-interfaces.py in Build Tools\Releases\Windows XP, win32 (1) (in a cmd window with Administrator privileges):

```cmd
py -2.7 update-core-interfaces.py

```

- Then run python update-component-interfaces.py millikan-components.txt in Build Tools\Releases\Windows XP, win32 (1) (in a cmd window with Administrator privileges):

```cmd
py -2.7 update-component-interfaces.py millikan-components.txt

```

- Build Core solution in the visual studio 2013 for both Release first and then Debug

## Build Components

- Run python local-core-release.py in Build Tools\Releases\Windows XP, win32 (1)(in a cmd window with Administrator privileges)

```cmd
py -2.7 local-core-release.py

```

- Build Components solution in the visual studio 2013 for both Release first and then Debug

---

## Agrupando as dlls
- Excluir o diretorio "Sortex" na raiz do repo se existir.
- usando o bash:

```bash
alias python='winpty python.exe'
touch .bashrc
cd Build\ Tools/Releases/Windows\ XP,\ win32\ (1)
  python collect-application.py millikan-components.txt ../../../

```
ou

```cmd
py -2.7 collect-application.py millikan-components.txt ../../../

```

- copiar as dlls do boost:
//release

```bash
cp /c/boost/boost_1_61_0/stage/lib/boost_chrono-vc120-mt-1_61.dll ../../../Sortex/sc_app
cp /c/boost/boost_1_61_0/stage/lib/boost_system-vc120-mt-1_61.dll ../../../Sortex/sc_app
cp /c/boost/boost_1_61_0/stage/lib/boost_thread-vc120-mt-1_61.dll ../../../Sortex/sc_app

```
ou

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
ou

```cmd
copy c:\boost\boost_1_61_0\stage\lib\boost_chrono-vc120-mt-gd-1_61.dll ..\..\..\Sortex\sc_app_d
copy c:\boost\boost_1_61_0\stage\lib\boost_system-vc120-mt-gd-1_61.dll ..\..\..\Sortex\sc_app_d
copy c:\boost\boost_1_61_0\stage\lib\boost_thread-vc120-mt-gd-1_61.dll ..\..\..\Sortex\sc_app_d

```

- cria os arquivos .ini

```bash
python create-components-ini.py millikan-components.txt

```
ou

```cmd
py -2.7 create-components-ini.py millikan-components.txt

```

- copiar os arquivos components.ini das pastas debug e release para as respectivas pastas em Sortex\
(procurar pelos arquivos components.ini nas pastas debug e relase

```bash
cp Release/components.ini ../../../Sortex/sc_app
cp Debug/components.ini ../../../Sortex/sc_app_d

```
ou

```cmd
copy Release\components.ini ..\..\..\Sortex\sc_app
copy Debug\components.ini ..\..\..\Sortex\sc_app_d

```

---
Para facilitar a atualizacao apos a compilacao de um projeto especifico, pode-se adicionar nos eventos de post-build, algo como:

```cmd
cd $(OutputPath)
copy *.pdb "$(SolutionDir)..\Sortex\sc_app_d" /Y

```
ou

```cmd
for %%e in (pdb dll) do copy *.%%e "$(SolutionDir)..\Sortex\sc_app_d" /Y

```
isso vai copiar os arquivos para o diretorio especifico Sortex.

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