# -*- coding: utf-8 -*-
import sqlite3
import random
from datetime import datetime, timedelta
import sys

DIVISION_NAMES = (
    'PrimaryDivision',
    'SecondaryDivision',
    'TertiaryDivision',
)
MAX_DEFECTS_PER_DIVISION = 8
EJECTOR_RATE_RANGES = (
    (1000, 50000),
    (51000, 100000),
    (101000, 150000),
    (151000, 200000),
    (201000, 250000),
    (251000, 300000),
    (301000, 350000),
    (350000, 400000),
)

def check_connection_and_table():
    conn = None
    try:
        conn = sqlite3.connect('statistics.sqlite')
        cursor = conn.cursor()

        required_tables = (
            'ejector_rate_per_defect_per_division_short',
            'throughput_per_division_short',
            'string_table',
        )
        placeholders = ', '.join('?' for _ in required_tables)
        cursor.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name IN ({})".format(placeholders),
            required_tables
        )
        existing_tables = {row[0] for row in cursor.fetchall()}
        missing_tables = set(required_tables) - existing_tables

        if not missing_tables:
            print("Connection ok. All required tables found.")
        else:
            print("Table not found: {}".format(', '.join(sorted(missing_tables))))
            return False

    except sqlite3.Error as e:
        print("Connection error: {}".format(e))
        return False
    finally:
        if conn:
            conn.close()

    return True

def load_statistics_codes():
    conn = sqlite3.connect('statistics.sqlite')
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT name, value FROM string_table ORDER BY rowid')
        rows = cursor.fetchall()
    finally:
        conn.close()

    division_codes = {}
    defect_codes = []
    blank_codes = []

    for name, value in rows:
        normalized_name = '' if name is None else name.strip()
        if normalized_name in DIVISION_NAMES:
            if normalized_name in division_codes:
                raise ValueError("Duplicate string_table entry: {}".format(normalized_name))
            division_codes[normalized_name] = value
        elif normalized_name == '':
            blank_codes.append(value)
        else:
            defect_codes.append(value)

    missing_divisions = [name for name in DIVISION_NAMES if name not in division_codes]
    if missing_divisions:
        raise ValueError(
            "Missing division codes in string_table: {}".format(', '.join(missing_divisions))
        )
    if len(defect_codes) > MAX_DEFECTS_PER_DIVISION:
        raise ValueError(
            "string_table contains {} defect codes; at most {} are supported".format(
                len(defect_codes), MAX_DEFECTS_PER_DIVISION
            )
        )
    if len(defect_codes) < MAX_DEFECTS_PER_DIVISION:
        if len(blank_codes) != 1:
            raise ValueError(
                "string_table must contain exactly one blank name when fewer than {} defects exist".format(
                    MAX_DEFECTS_PER_DIVISION
                )
            )
        defect_codes.extend(
            [blank_codes[0]] * (MAX_DEFECTS_PER_DIVISION - len(defect_codes))
        )

    ordered_division_codes = [division_codes[name] for name in DIVISION_NAMES]
    blank_code = blank_codes[0] if blank_codes else None
    return ordered_division_codes, defect_codes, blank_code

def generate_defect_values(defect_codes, blank_code):
    values = []
    for defect_code, rate_range in zip(defect_codes, EJECTOR_RATE_RANGES):
        values.append(defect_code)
        values.append(
            None if defect_code == blank_code else random.randint(rate_range[0], rate_range[1])
        )
    return values

def clear_tables(start_date, end_date):
    conn = sqlite3.connect('statistics.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM ejector_rate_per_defect_per_division_short
        WHERE timestamp BETWEEN ? AND ?''', (start_date, end_date))

    cursor.execute('''
        DELETE FROM throughput_per_division_short
        WHERE timestamp BETWEEN ? AND ?''', (start_date, end_date))

    conn.commit()
    conn.close()
    print("Tables cleared for the specified period.")

def generate_data(start_date, end_date, division_codes, defect_codes, blank_code):
    conn = sqlite3.connect('statistics.sqlite')
    cursor = conn.cursor()

    current_time = start_date
    nrRecords = 0

    while current_time <= end_date:
        timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
        record_ejectors = [timestamp]
        for division_code in division_codes:
            record_ejectors.append(division_code)
            record_ejectors.extend(generate_defect_values(defect_codes, blank_code))

        # Data for throughput_per_division_short
        record_throughput = [
            timestamp,
            division_codes[0],
            random.randint(500, 1000),  # throughput_1
            division_codes[1],
            random.randint(1100, 2000),  # throughput_2
            division_codes[2],
            random.randint(2100, 3000)  # throughput_3
        ]

        cursor.execute('''
            INSERT INTO ejector_rate_per_defect_per_division_short (
                timestamp, str_division_1, str_defect_1_1, ejector_rate_1_1,
                str_defect_1_2, ejector_rate_1_2, str_defect_1_3, ejector_rate_1_3,
                str_defect_1_4, ejector_rate_1_4, str_defect_1_5, ejector_rate_1_5,
                str_defect_1_6, ejector_rate_1_6, str_defect_1_7, ejector_rate_1_7,
                str_defect_1_8, ejector_rate_1_8, str_division_2, str_defect_2_1,
                ejector_rate_2_1, str_defect_2_2, ejector_rate_2_2, str_defect_2_3,
                ejector_rate_2_3, str_defect_2_4, ejector_rate_2_4, str_defect_2_5,
                ejector_rate_2_5, str_defect_2_6, ejector_rate_2_6, str_defect_2_7,
                ejector_rate_2_7, str_defect_2_8, ejector_rate_2_8, str_division_3,
                str_defect_3_1, ejector_rate_3_1, str_defect_3_2, ejector_rate_3_2,
                str_defect_3_3, ejector_rate_3_3, str_defect_3_4, ejector_rate_3_4,
                str_defect_3_5, ejector_rate_3_5, str_defect_3_6, ejector_rate_3_6,
                str_defect_3_7, ejector_rate_3_7, str_defect_3_8, ejector_rate_3_8
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                      ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                      ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', record_ejectors)

        cursor.execute('''
            INSERT INTO throughput_per_division_short (
                timestamp, str_division_1, throughput_1,
                str_division_2, throughput_2,
                str_division_3, throughput_3
            ) VALUES (?, ?, ?, ?, ?, ?, ?)''', record_throughput)


        current_time += timedelta(minutes=1)  # add 1 minute
        nrRecords += 1

    conn.commit()
    conn.close()
    print("Inserted {} records into the database.".format(nrRecords))

#-----------------------------------------------------------------------------
#   Main
#-----------------------------------------------------------------------------
def main():
    if len(sys.argv) != 3:
        print("Usage: python generateStats.py 'YYYY-MM-DD HH:MM' 'YYYY-MM-DD HH:MM'")
        sys.exit(1)

    start_date_str = sys.argv[1]
    end_date_str = sys.argv[2]

    # Convert strings to datetime
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d %H:%M')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d %H:%M')

    # Check connection and table existence
    if check_connection_and_table():
        try:
            division_codes, defect_codes, blank_code = load_statistics_codes()
        except (sqlite3.Error, ValueError) as error:
            print("String table error: {}".format(error))
            sys.exit(1)

        clear_tables(start_date, end_date)
        generate_data(start_date, end_date, division_codes, defect_codes, blank_code)
        print("Data generation completed.")

if __name__ == '__main__':
    main()
