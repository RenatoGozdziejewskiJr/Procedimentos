# -*- coding: utf-8 -*-
import sqlite3
import random
from datetime import datetime, timedelta, timezone
import sys

import splintco_python

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

def local_time_to_utc(date_time):
    return date_time.astimezone(timezone.utc).replace(tzinfo=None)

def check_connection_and_table():
    conn = None
    try:
        conn = sqlite3.connect('.\statistics.sqlite')
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

def load_statistics_codes_and_defects(response):
    conn = sqlite3.connect('statistics.sqlite')
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT name, value FROM string_table ORDER BY rowid')
        rows = cursor.fetchall()
    finally:
        conn.close()

    string_map = {}
    blank_code = None

    for name, value in rows:
        normalized_name = '' if name is None else name.strip()
        if normalized_name == '':
            if blank_code is None:
                blank_code = value
        else:
            string_map[normalized_name] = value

    ordered_division_codes = []
    for div_name in DIVISION_NAMES:
        if div_name not in string_map:
            raise ValueError("Missing division codes in string_table: {}".format(div_name))
        ordered_division_codes.append(string_map[div_name])

    defects_by_division = {div_name: [] for div_name in DIVISION_NAMES}

    for defect in getattr(response, "list_of_defects", []):
        d_name = getattr(defect, 'defect')
        div_name = getattr(defect, 'division')
        if d_name and div_name:
            if div_name in defects_by_division:
                if d_name in string_map:
                    defects_by_division[div_name].append(string_map[d_name])
                else:
                    print("Warning: Defect {} not found in string_table.".format(d_name))

    defects_per_division_codes = []
    for div_name in DIVISION_NAMES:
        codes = defects_by_division[div_name]
        if len(codes) > MAX_DEFECTS_PER_DIVISION:
            raise ValueError(
                "Division {} has {} defect codes; at most {} are supported".format(
                    div_name, len(codes), MAX_DEFECTS_PER_DIVISION
                )
            )
        if len(codes) < MAX_DEFECTS_PER_DIVISION:
            if blank_code is None:
                raise ValueError(
                    "string_table must contain exactly one blank name when fewer than {} defects exist".format(
                        MAX_DEFECTS_PER_DIVISION
                    )
                )
            codes.extend([blank_code] * (MAX_DEFECTS_PER_DIVISION - len(codes)))
        defects_per_division_codes.append(codes)

    return ordered_division_codes, defects_per_division_codes, blank_code

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

def generate_data(start_date, end_date, division_codes, defects_per_division_codes, blank_code):
    conn = sqlite3.connect('statistics.sqlite')
    cursor = conn.cursor()

    current_time = start_date
    nrRecords = 0

    while current_time <= end_date:
        timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
        record_ejectors = [timestamp]
        for i, division_code in enumerate(division_codes):
            record_ejectors.append(division_code)
            record_ejectors.extend(generate_defect_values(defects_per_division_codes[i], blank_code))

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

    # Interpret the informed period using the computer's local timezone and store it as UTC.
    start_date = local_time_to_utc(datetime.strptime(start_date_str, '%Y-%m-%d %H:%M'))
    end_date = local_time_to_utc(datetime.strptime(end_date_str, '%Y-%m-%d %H:%M'))
    print(
        "UTC period: {} to {}".format(
            start_date.strftime('%Y-%m-%d %H:%M'),
            end_date.strftime('%Y-%m-%d %H:%M')
        )
    )

    # Check connection and defect list
    config = splintco_python.SessionConfig()
    config.host = "127.0.0.1"
    config.port = 50713
    config.connection_timeout = 3000
    config.auto_reconnect = True
    config.request_attempts = 3

    session = splintco_python.SplintSession(config)

    success, err = session.connect()
    if not success:
        print(f"Failed to connect: {err}")
        return
    
    print("Connected successfully.")

    # Get defect list
    request = splintco_python.GetDefectListRequest()
    request.notification_level = 0
    encoded_request = splintco_python.encode_get_defect_list_request(request)

    response = None
    # Send request and await bytes response
    response_bytes, err = session.send(splintco_python.GET_DEFECT_LIST_COMMAND_ID, encoded_request)
    if response_bytes is None:
        print(f"Protocol or Connection Error: {err}")
    else:
        # Decode the response
        response = splintco_python.decode_get_defect_list_response(response_bytes)

    if response is not None:
        # Handle Command Error
        if getattr(response, "command_error", 0) != 0:
            error_msg = splintco_python.get_get_defect_list_command_error_string(response.command_error)
            print(f"Command Error: {error_msg}")
        else:
            # Success! Print JSON representation
            print("JSON:", splintco_python.get_defect_list_response_to_json(response))

        for defect in getattr(response, "list_of_defects", []):
            if getattr(defect, 'defect') and getattr(defect, 'division'):
                print("Defect: {} Division: {}".format(defect.defect, defect.division))

    # Disconnect from the session after checking the connection and defect list
    session.disconnect()

    if response is None or getattr(response, "command_error", 0) != 0:
        print("Could not retrieve valid defect list. Exiting.")
        sys.exit(1)

    # Check connection and table existence
    if check_connection_and_table():
        try:
            division_codes, defects_per_division_codes, blank_code = load_statistics_codes_and_defects(response)
        except (sqlite3.Error, ValueError) as error:
            print("String table error: {}".format(error))
            sys.exit(1)

        clear_tables(start_date, end_date)
        generate_data(start_date, end_date, division_codes, defects_per_division_codes, blank_code)
        print("Data generation completed.")

if __name__ == '__main__':
    main()
