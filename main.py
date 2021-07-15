import time
import psycopg2
import sys
import numpy as np
import math
import threading

# 임시 데이터 불러오기(next_location & next_zone_no)


def get_temp_Enc_Data(cursor):
    cursor.execute(F'Select * from "ENCData" limit 10')
    next_rows = cursor.fetchall()
    return next_rows


dlatitude = [0, -1, 0, 1, 1, 1, 0, -1, -1]
dlongitude = [0, 1, 1, 1, 0, -1, -1, -1, 0]


def calulate_Zone_No(latitude, longitude, factor: 5):
    latitude = latitude + 90
    longitude = longitude + 180

    column = math.trunc(latitude)
    row = math.trunc(longitude)

    return column + row * 360


def get_Zone_Enc_Data(cursor, zone_no):
    cursor.execute(F'Select * from "ENCData" where "Zone_No" = {zone_no}')
    rows = cursor.fetchall()
    # print(zone_no, len(rows))


def main():
    try:
        connect = psycopg2.connect(
            host='localhost', dbname='enc', user='postgres')
        cursor = connect.cursor()

        # 임시 구현.
        temp_next_enc_data = get_temp_Enc_Data(cursor)
        index = 0
        ##

        cur_Latitude = 32
        cur_Longitude = 127
        cur_Zone_No = 150

        for temp_next_data in temp_next_enc_data:  # while문으로 대체 예정
            next_latitude = temp_next_data["Location_Lat"]
            next_longitude = temp_next_data["Location_Lon"]
            print(next_latitude, next_longitude)

            next_Zone_No = calulate_Zone_No(next_latitude, next_longitude)
            print(next_latitude, next_longitude, next_Zone_No)

            if cur_Zone_No == next_Zone_No:
                next_Zone_No = cur_Zone_No
                next_latitude = cur_Latitude
                next_longitude = cur_Longitude

            # TODO: 9 hot zone, 7 broad zone. Total: 16 zone to redis
            # else:
            #     for i in range(0, 9):
            #         hot_zone_no = (math.floor(next_latitude) + dlatitude.index(i)) * ((math.floor(next_latitude) + dlongitude[i])

    except Exception as e:
        print("Error", e)
    else:
        # print(len(Hot_Zone_Enc_Data))
        pass
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    main()
