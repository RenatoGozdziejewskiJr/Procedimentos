# Notes about Generating Statistics Data for Millikan and Merlin

[Português (Brasil)](0003-notas-geracao-dados-estatisticos-millikan-merlin-pt-br.md)

## 1. Overview

This procedure describes how to use the `generateStats.py` script to generate random statistics data for Millikan and Merlin machines.

The script writes data to the `statistics.sqlite` database. Because the database path is relative, run the command from the `Sortex/sc_app/storage` directory.

## 2. Prerequisites

- Python installed on the machine.
- The `generateStats.py` file available.
- The `splintco_python` module available for communication with the machine software.
- The machine software running and accessible locally on port 50713.
- The `statistics.sqlite` database present in `Sortex/sc_app/storage`.
- The following tables present in the database:
  - `string_table`
  - `ejector_rate_per_defect_per_division_short`
  - `throughput_per_division_short`

## 3. Division and Defect Codes

The script connects to the machine software and requests the list of defects currently active for each division.

The `string_table` is used only to look up the numeric ID corresponding to each division or defect name. The following division names are expected:

1. `PrimaryDivision`
2. `SecondaryDivision`
3. `TertiaryDivision`

The IDs of the defects returned by the machine for each division are looked up in `string_table`. The script accepts a maximum of eight defects per division.

When a division has fewer than eight configured defects, the remaining positions use the numeric code for the record in `string_table` whose name is empty or contains only spaces. For those positions, `ejector_rate` is written as `NULL`.

The script validates this data before deleting or generating information. Execution stops if communication with the machine fails, a division is missing from the string table, a division has more than eight defects, or the code for the empty name is not defined.

## 4. Important Warning

Before generating data, the script deletes existing records within the specified interval from both tables. Back up the database before running it.

```bash
cd Sortex/sc_app/storage
cp statistics.sqlite statistics.sqlite.bak
```

## 5. Preparation

Copy the script to the directory containing the database:

```bash
cp /caminho/para/generateStats.py Sortex/sc_app/storage/
cd Sortex/sc_app/storage
```

Confirm that the script and database are in the current directory:

```bash
ls -l generateStats.py statistics.sqlite
```

## 6. Running the Script

Run the script with the local start and end date and time in `YYYY-MM-DD HH:MM` format. The script detects the time zone configured in the operating system and converts the values to UTC before querying or writing to the database:

```bash
python generateStats.py 'YYYY-MM-DD HH:MM' 'YYYY-MM-DD HH:MM'
```

Example: generate one record per minute for one hour:

```bash
python generateStats.py '2026-09-11 10:00' '2026-09-11 11:00'
```

On a computer configured for UTC−3, the example interval is written to the database from `2026-09-11 13:00:00` to `2026-09-11 14:00:00` UTC. In another country, the result is adjusted according to the configured local time zone. The start and end dates are inclusive; therefore, 61 records are generated in each table.

Before running the script, confirm that the operating system's date, time, and time zone are correct.

If the `python` command is unavailable and the machine uses Python 3, run:

```bash
python3 generateStats.py '2026-09-11 10:00' '2026-09-11 11:00'
```

## 7. Expected Result

When the connection and tables are found, the output will resemble:

```text
UTC period: 2026-09-11 13:00 to 2026-09-11 14:00
Connected successfully.
JSON: {...}
Defect: Chalky Division: PrimaryDivision
Defect: Yellow Division: SecondaryDivision
...
Connection ok. All required tables found.
Tables cleared for the specified period.
Inserted 61 records into the database.
Data generation completed.
```

The script generates data for three divisions and writes one record per minute to the ejector-rate and throughput tables.

## 8. Building the Executable (.exe)

To run the script in environments where its dependencies do not need to be installed, it can be packaged as an executable.

### 8.1 Installing PyInstaller

First, install `pyinstaller`:

```bash
pip install pyinstaller
```

### 8.2 Creating the Executable

To create a single-file executable that includes the required `.pyd` library, run this command from the same directory as the script:

```bash
pyinstaller --onefile --add-binary "splintco_python.cp311-win_amd64.pyd;." generateStats.py
```

The generated executable (`generateStats.exe`) is saved in the `dist/` subdirectory.

## 9. Troubleshooting

### 9.1 `Table not found.` Message

Confirm that the command is being run from `Sortex/sc_app/storage`, that the correct `statistics.sqlite` file is in that directory, and that all three required tables exist.

### 9.2 `String table error` Message

Check that `string_table` contains the codes for the three divisions, the IDs for all defects currently reported by the machine, and a record with an empty name when any division has fewer than eight defects.

### 9.3 Equipment Connection Errors (`Failed to connect` / `Protocol or Connection Error`)

The script must obtain the defect list by communicating with the machine on port 50713. Check that the equipment's main service is running and responding to requests.

### 9.4 `Connection error` Message

Check the read and write permissions for `statistics.sqlite` and the `Sortex/sc_app/storage` directory.

### 9.5 Invalid Date Format

Use exactly the `YYYY-MM-DD HH:MM` format, keeping each date and time in quotation marks.

### 9.6 Restoring the Database

To discard the generated data and restore the backup:

```bash
cd Sortex/sc_app/storage
cp statistics.sqlite.bak statistics.sqlite
```
