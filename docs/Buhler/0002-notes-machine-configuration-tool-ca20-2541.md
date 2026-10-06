# Notes about the Machine Configuration Tool (CA20-2541)

## 1. Overview

- Description: Machine Configuration Tool for Sortex S
- Software Part Number: CA20-2541
- Latest issue/build/date: 3 / 3.1.2 / 2-Nov-2015
- Previous issues:
  - 2 / 2.0.393 / 13-Aug-2014
  - 1 / 1.2.41 / 14-Apr-2014

## 2. Required Software

### 2.1 Original Environment

- Qt Creator
- Qt 5.1.0
- Visual Studio 2010
- Boost 1.48

### 2.2 Environment After Porting

- Qt Creator
- Qt 5.8.0
- Visual Studio 2013
- Boost 1.61

## 3. Generating the Build

### 3.1 Via Jenkins

- Job: CA20-2541_(Machine_Config_Tool)

### 3.2 After Porting

- `_Millikan/_AIMB-216-Tools/CA20-2541_Machine_Config_Tool`

## 4. Building in Qt Creator

Some files and directories must be copied to the root of the build directory.

Required files (source: CA20-1741):

- componentlife.xml
- machine.xml
- systemmodel.xml

Also copy the following directories:

```text
C:\Qt\Qt5.1.0\5.1.0\msvc2010\plugins\platforms
C:\Qt\Qt5.1.0\5.1.0\msvc2010\qml
```

To these destinations:

```text
<build root>\release
<build root>\debug
```

## 5. Running the Application

This application is a wrapper for a Python script. Even after compiling and running it, additional files must be copied for full operation.

Copy:

```text
C:\Python26\DLLs\
```

To:

```text
<build root>\DLLs\
```
