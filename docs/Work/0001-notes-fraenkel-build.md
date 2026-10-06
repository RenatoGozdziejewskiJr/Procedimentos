# Notes about the Fraenkel Build

[Português (Brasil)](0001-notas-compilacao-fraenkel-pt-br.md)

## 1. Building the Core

Run `update-core-interfaces.py` from `Build Tools\Releases\Windows XP, win32 (1)` in a Command Prompt with Administrator privileges:

```cmd
py -2.7 update-core-interfaces.py
```

Then run `update-component-interfaces.py millikan-components.txt` from the same directory and Command Prompt:

```cmd
py -2.7 update-component-interfaces.py millikan-components.txt
```

Build the Core solution in Visual Studio 2013, building Release first and then Debug.

## 2. Building Components

Run `local-core-release.py` from `Build Tools\Releases\Windows XP, win32 (1)` in a Command Prompt with Administrator privileges:

```cmd
py -2.7 local-core-release.py
```

Build the Components solution in Visual Studio 2013, building Release first and then Debug.

## 3. Grouping the DLLs

Delete the `Sortex` directory at the repository root if it exists.

Using Bash:

```bash
alias python='winpty python.exe'
touch .bashrc
cd Build\ Tools/Releases/Windows\ XP,\ win32\ (1)
  python collect-application.py millikan-components.txt ../../../
```

Alternatively, use Command Prompt:

```cmd
py -2.7 collect-application.py millikan-components.txt ../../../
```

### 3.1 Copying the Boost DLLs

//release

```bash
cp /c/boost/boost_1_61_0/stage/lib/boost_chrono-vc120-mt-1_61.dll ../../../Sortex/sc_app
cp /c/boost/boost_1_61_0/stage/lib/boost_system-vc120-mt-1_61.dll ../../../Sortex/sc_app
cp /c/boost/boost_1_61_0/stage/lib/boost_thread-vc120-mt-1_61.dll ../../../Sortex/sc_app
```

Alternatively:

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

Alternatively:

```cmd
copy c:\boost\boost_1_61_0\stage\lib\boost_chrono-vc120-mt-gd-1_61.dll ..\..\..\Sortex\sc_app_d
copy c:\boost\boost_1_61_0\stage\lib\boost_system-vc120-mt-gd-1_61.dll ..\..\..\Sortex\sc_app_d
copy c:\boost\boost_1_61_0\stage\lib\boost_thread-vc120-mt-gd-1_61.dll ..\..\..\Sortex\sc_app_d
```

### 3.2 Creating and Copying the INI Files

Create the `.ini` files:

```bash
python create-components-ini.py millikan-components.txt
```

Alternatively:

```cmd
py -2.7 create-components-ini.py millikan-components.txt
```

Copy the `components.ini` files from the Debug and Release directories to their corresponding directories under `Sortex\` (locate the `components.ini` files in the Debug and Release directories):

```bash
cp Release/components.ini ../../../Sortex/sc_app
cp Debug/components.ini ../../../Sortex/sc_app_d
```

Alternatively:

```cmd
copy Release\components.ini ..\..\..\Sortex\sc_app
copy Debug\components.ini ..\..\..\Sortex\sc_app_d
```

## 4. Copying Files After a Build

To simplify updating after building a specific project, add commands such as the following to the post-build events:

```cmd
cd $(OutputPath)
copy *.pdb "$(SolutionDir)..\Sortex\sc_app_d" /Y
copy *.dll "$(SolutionDir)..\Sortex\sc_app_d" /Y
```

Alternatively:

```cmd
for %%e in (pdb dll) do copy *.%%e "$(SolutionDir)..\Sortex\sc_app_d" /Y
```

This copies the files to the specified `Sortex` directory:

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
