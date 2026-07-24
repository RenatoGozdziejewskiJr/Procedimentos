# Machine Configuration Tool (CA20-2541)

## Visao Geral

- Description: Machine Configuration Tool for Sortex S
- Software Part Number: CA20-2541
- Latest issue/build/date: 3 / 3.1.2 / 2-Nov-2015
- Previous issues:
    - 2 / 2.0.393 / 13-Aug-2014
    - 1 / 1.2.41 / 14-Apr-2014

---

## Software Necessario

### Ambiente original

- Qt Creator
- Qt 5.1.0
- Visual Studio 2010
- Boost 1.48

### Ambiente apos port

- Qt Creator
- Qt 5.8.0
- Visual Studio 2013
- Boost 1.61

---

## Como Gerar o Build

### Via Jenkins

- Job: CA20-2541_(Machine_Config_Tool)

### Apos port

- _Millikan/_AIMB-216-Tools/CA20-2541_Machine_Config_Tool

---

## Como Compilar no Qt Creator

Alguns arquivos e diretorios precisam ser copiados para a raiz do diretorio de build.

Arquivos necessarios (origem: CA20-1741):

- componentlife.xml
- machine.xml
- systemmodel.xml

Tambem copie os seguintes diretorios:

```text
C:\Qt\Qt5.1.0\5.1.0\msvc2010\plugins\platforms
C:\Qt\Qt5.1.0\5.1.0\msvc2010\qml
```

Para os destinos:

```text
<build root>\release
<build root>\debug
```

---

## Executando a Aplicacao

Esta aplicacao e um wrapper para um script Python. Mesmo compilando e executando, e necessario copiar arquivos adicionais para funcionamento completo.

Copie:

```text
C:\Python26\DLLs\
```

Para:

```text
<build root>\DLLs\
```
