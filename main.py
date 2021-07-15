import time
import psycopg2
import sys
import numpy as np
import math
import threading

# 임시 데이터 불러오기(next_location & next_zone_no)


def get_temp_Enc_Data(cursor):
    cursor.execute(
        F'Select * from "ENCData" where "Location Lat" is not null limit 10')
    next_rows = cursor.fetchall()
    return next_rows


dlatitude = [0, 1, 1, 1, 0, -1, -1, -1, 0]
dlongitude = [0, -1, 0, 1, 1, 1, 0, -1, -1]


def calculate_Zone_No(latitude, longitude):
    latitude = latitude + 90
    longitude = longitude + 180

    return math.trunc(longitude) + math.trunc(latitude) * 360


def get_Zone_Enc_Data(cursor, zone_no):
    cursor.execute(F'Select * from "ENCData" where "Zone_No" = {zone_no}')
    rows = cursor.fetchall()
    # print(zone_no, len(rows))


def main():
    try:
        start_time = time.time()
        connect = psycopg2.connect(
            host='localhost', dbname='new_enc', user='postgres')
        cursor = connect.cursor()
        print(F'taken time:{time.time()-start_time}s')

        # 임시 구현.
        temp_next_enc_data = get_temp_Enc_Data(cursor)
        ##

        cur_Latitude = 32
        cur_Longitude = 127
        cur_Zone_No = 150

        for temp in temp_next_enc_data:  # while문으로 대체 예정
            next_latitude = temp[6]
            next_longitude = temp[7]
            next_Zone_No = calulate_Zone_No(next_latitude, next_longitude)

            if cur_Zone_No == next_Zone_No:
                next_Zone_No = cur_Zone_No
                next_latitude = cur_Latitude
                next_longitude = cur_Longitude
            # TODO: 9 hot zone, 7 broad zone. Total: 16 zone to redis
            else:
                temp_l = []
                for i in range(0, 9):
                    hot_zone_no = next_Zone_No + 360 * \
                        dlatitude[i] + dlongitude[i]
                    temp_l.append(hot_zone_no)
                print(temp_l)

    except Exception as e:
        print("Error", e)
    else:
        # print(len(Hot_Zone_Enc_Data))
        pass
    finally:
        if connect:
            connect.close()


if __name__ == '__main__':
    main()
