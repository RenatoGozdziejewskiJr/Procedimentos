# -*- coding: utf-8 -*-
import sqlite3
import random
from datetime import datetime, timedelta
import sys
import math

def check_connection_and_table():
    conn = None
    try:
        conn = sqlite3.connect('statistics.sqlite') 
        cursor = conn.cursor()
        
        # Check if the table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ejector_rate_per_defect_per_division_short';")
        table_exists_1 = cursor.fetchone()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='throughput_per_division_short';")
        table_exists_2 = cursor.fetchone()
        
        if table_exists_1 and table_exists_2:
            print("Connection ok. Both tables found.")
        else:
            print("Table not found.")
            return False
        
    except sqlite3.Error as e:
        print("Connection error: {}".format(e))
        return False
    finally:
        if conn:
            conn.close()
    
    return True

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

def generate_sine_value(base, amplitude, time_index, frequency, phase):
    return int(base + amplitude * math.sin(frequency * time_index + phase))

def generate_data(start_date, end_date):
    conn = sqlite3.connect('statistics.sqlite')
    cursor = conn.cursor()

    current_time = start_date

    # Define code for defects and divisions - These codes can be found in the string_table table
    str_division_1 = 1  # Primary Division
    str_defects_1 = [11, 7, 3, 5, 12, 6, 2, 2]  # defect codes for division 1

    str_division_2 = 15  # Secondary Division    
    str_defects_2 = [11, 7, 3, 5, 12, 6, 2, 2]  # defect codes for division 2

    str_division_3 = 16  # Tertiary Division    
    str_defects_3 = [11, 7, 3, 5, 12, 6, 2, 2]  # defect codes for division 3

    nrRecords = 0

    frequency = 2 * math.pi / 60 # Frequency for sine wave generation (1 cycle per minute)
    phase1 = 0            
    phase2 = math.pi / 4  
    phase3 = math.pi / 2  

    while current_time <= end_date:
        time_index = (current_time - start_date).seconds // 60 # Calculate the time index in minutes from start_date

        # create a record for each minute
        record_ejectors = [
            current_time.strftime('%Y-%m-%d %H:%M:%S'),
            str_division_1,
            str_defects_1[0],  # str_defect_1_1
            random.randint(  1000, 50000) if str_defects_1[0] != 2 else None,  # ejector_rate_1_1
            str_defects_1[1],  # str_defect_1_2
            random.randint( 51000, 100000) if str_defects_1[1] != 2 else None,  # ejector_rate_1_2
            str_defects_1[2],  # str_defect_1_3
            random.randint(101000, 150000) if str_defects_1[2] != 2 else None,  # ejector_rate_1_3
            str_defects_1[3],  # str_defect_1_4
            random.randint(151000, 200000) if str_defects_1[3] != 2 else None,  # ejector_rate_1_4
            str_defects_1[4],  # str_defect_1_5
            random.randint(201000, 250000) if str_defects_1[4] != 2 else None,  # ejector_rate_1_5
            str_defects_1[5],  # str_defect_1_6
            random.randint(251000, 300000) if str_defects_1[5] != 2 else None,  # ejector_rate_1_6
            str_defects_1[6],  # str_defect_1_7
            random.randint(301000, 350000) if str_defects_1[6] != 2 else None,  # ejector_rate_1_7
            str_defects_1[7],  # str_defect_1_8
            random.randint(350000, 400000) if str_defects_1[7] != 2 else None,  # ejector_rate_1_8
            str_division_2,
            str_defects_2[0],  # str_defect_2_1
            random.randint(  1000, 50000) if str_defects_2[0] != 2 else None,  # ejector_rate_2_1
            str_defects_2[1],  # str_defect_2_2
            random.randint( 51000, 100000) if str_defects_2[1] != 2 else None,  # ejector_rate_2_2
            str_defects_2[2],  # str_defect_2_3
            random.randint(101000, 150000) if str_defects_2[2] != 2 else None,  # ejector_rate_2_3
            str_defects_2[3],  # str_defect_2_4
            random.randint(151000, 200000) if str_defects_2[3] != 2 else None,  # ejector_rate_2_4
            str_defects_2[4],  # str_defect_2_5
            random.randint(201000, 250000) if str_defects_2[4] != 2 else None,  # ejector_rate_2_5
            str_defects_2[5],  # str_defect_2_6
            random.randint(251000, 300000) if str_defects_2[5] != 2 else None,  # ejector_rate_2_6
            str_defects_2[6],  # str_defect_2_7
            random.randint(301000, 350000) if str_defects_2[6] != 2 else None,  # ejector_rate_2_7
            str_defects_2[7],  # str_defect_2_8
            random.randint(350000, 400000) if str_defects_2[7] != 2 else None,  # ejector_rate_2_8
            str_division_3,
            str_defects_3[0],  # str_defect_3_1
            random.randint(  1000, 50000) if str_defects_3[0] != 2 else None,  # ejector_rate_3_1
            str_defects_3[1],  # str_defect_3_2
            random.randint( 51000, 100000) if str_defects_3[1] != 2 else None,  # ejector_rate_3_2
            str_defects_3[2],  # str_defect_3_3
            random.randint(101000, 150000) if str_defects_3[2] != 2 else None,  # ejector_rate_3_3
            str_defects_3[3],  # str_defect_3_4
            random.randint(151000, 200000) if str_defects_3[3] != 2 else None,  # ejector_rate_3_4
            str_defects_3[4],  # str_defect_3_5
            random.randint(201000, 250000) if str_defects_3[4] != 2 else None,  # ejector_rate_3_5
            str_defects_3[5],  # str_defect_3_6
            random.randint(251000, 300000) if str_defects_3[5] != 2 else None,  # ejector_rate_3_6
            str_defects_3[6],  # str_defect_3_7
            random.randint(301000, 350000) if str_defects_3[6] != 2 else None,  # ejector_rate_3_7
            str_defects_3[7],  # str_defect_3_8
            random.randint(350000, 400000) if str_defects_3[7] != 2 else None,  # ejector_rate_3_8
        ]

        # Data for throughput_per_division_short
        record_throughput = [
            current_time.strftime('%Y-%m-%d %H:%M:%S'),
            str_division_1, 
            random.randint(500, 1000),  # throughput_1
            #generate_sine_value(2000, 1500, time_index, frequency, phase1), # throughput_1
            str_division_2,
            random.randint(1100, 2000),  # throughput_2
            #generate_sine_value(2000, 1500, time_index, frequency/2, phase2),  # throughput_2
            str_division_3,
            random.randint(2100, 3000)  # throughput_3
            #generate_sine_value(2000, 1500, time_index, frequency/4, phase3)   # throughput_3
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
        clear_tables(start_date, end_date)  
        generate_data(start_date, end_date)
        print("Data generation completed.")

if __name__ == '__main__':
    main()