# CREATE DATABASE MonitoringService;
#
# CREATE TABLE Device (
#     id SERIAL PRIMARY KEY,
#     name VARCHAR(255),
#     ip VARCHAR(255),
#     can_get_info BOOLEAN
# );
#
# CREATE TABLE DeviceActivity (
#     device_id INTEGER REFERENCES Device(id),
#     is_online BOOLEAN,
#     last_ping TIMESTAMP,
#     last_time_online TIMESTAMP
# );
#
# CREATE TABLE DeviceResources (
#     device_id INTEGER REFERENCES Device(id),
#     cpu_used VARCHAR(255),
#     memory_used VARCHAR(255),
#     cpu_model VARCHAR(255),
#     cpu_cores INTEGER,
#     video_driver_model VARCHAR(255),
#     disks VARCHAR(255),
#     charge VARCHAR(255),
#     time_left VARCHAR(255),
#     boot_time TIMESTAMP,
#     request_time TIMESTAMP
# );

from config import *
import psycopg2

DEVICE_TABLE_NAME = 'Device'
ID = 'id'
DEVICE_NAME = 'name'
DEVICE_IP = 'ip'
DEVICE_CAN_GET_INFO = 'can_get_info'
DEVICE_NOTIFICATION = 'notification'

DEVICE_ACTIVITY_TABLE_NAME = 'DeviceActivity'
DEVICE_ID = 'device_id'
IS_ONLINE = 'is_online'
LAST_PING = 'last_ping'
LAST_TIME_ONLINE = 'last_time_online'

DEVICE_RESOURCES_TABLE_NAME = 'DeviceResources'
CPU_USED = 'cpu_used'
MEMORY_USED = 'memory_used'
CPU_MODEL = 'cpu_model'
CPU_CORES = 'cpu_cores'
DRIVER_MODEL = 'video_driver_model'
DISKS = 'disks'
CHARGE = 'charge'
TIME_LEFT = 'time_left'
BOOT_TIME = 'boot_time'
REQUEST_TIME = 'request_time'


def start_db():
    try:
        global connection
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        print('[INFO] Connected to db')
        return connection
    except Exception as _ex:
        print("[INFO] error database", _ex)


def select_all_devices():
    try:
        with connection.cursor() as cursor:
            select_query = 'SELECT * FROM ' + DEVICE_TABLE_NAME + ';'
            cursor.execute(select_query)
            return cursor.fetchall()
    except Exception as ex:
        print(str(ex))


def insert_device(name, ip, can_get_info, notification):
    try:
        with connection.cursor() as cursor:
            insert_query = 'INSERT INTO ' + DEVICE_TABLE_NAME + \
                           '(' + DEVICE_NAME + ', ' + \
                            DEVICE_IP + ', ' + \
                            DEVICE_CAN_GET_INFO + ', ' + \
                            DEVICE_NOTIFICATION + \
                           ') VALUES (\'%s\', \'%s\', %s, %s);'

            cursor.execute(insert_query % (name, ip, can_get_info, notification))
            connection.commit()
            print("[INFO] Data was added")
    except Exception as ex:
        print(str(ex))


def insert_activity(id, is_online, last_ping, last_time_online):
    try:
        with connection.cursor() as cursor:
            insert_query = 'INSERT INTO ' + DEVICE_ACTIVITY_TABLE_NAME + '(' + \
                           DEVICE_ID + ', ' + \
                           IS_ONLINE + ', ' + \
                           LAST_PING + ', ' + \
                           LAST_TIME_ONLINE + \
                           ') VALUES (%d, %s, \'%s\', \'%s\');'
            cursor.execute(insert_query % (id, is_online, last_ping, last_time_online))
        connection.commit()
        print("[INFO] Data was added")
    except Exception as ex:
        print(str(ex))


def select_ips():
    try:
        with connection.cursor() as cursor:
            select_query = 'SELECT ' + ID + ', ' + DEVICE_IP + ' FROM ' + DEVICE_TABLE_NAME + ';'
            cursor.execute(select_query)
            return cursor.fetchall()
    except Exception as ex:
        print(str(ex))


def update_activity(id, is_online, last_ping, last_time_online):
    try:
        with connection.cursor() as cursor:
            update_query = 'UPDATE ' + DEVICE_ACTIVITY_TABLE_NAME + \
                ' SET ' + \
                IS_ONLINE + ' = ' + '%s, ' + \
                LAST_PING + ' = ' + ' \'%s\', ' + \
                LAST_TIME_ONLINE + ' = ' + ' \'%s\'' + \
                'WHERE ' + DEVICE_ID + ' = %d;'
            cursor.execute(update_query % (is_online, last_ping, last_time_online, id))
            connection.commit()
            print("[INFO] Data was updated")
    except Exception as ex:
        print(str(ex))


def select_activity(id):
    try:
        with connection.cursor() as cursor:
            select_query = 'SELECT * FROM ' + DEVICE_ACTIVITY_TABLE_NAME + ' WHERE ' + DEVICE_ID + ' = %d;'
            cursor.execute(select_query % id)
            return cursor.fetchall()
    except Exception as ex:
        print(str(ex))


def insert_resources(id,
                     cpu_used,
                     memory_used,
                     cpu_model,
                     cpu_cores,
                     video_driver_model,
                     disks,
                     charge,
                     time_left,
                     boot_time,
                     request_time):
    try:
        with connection.cursor() as cursor:
            insert_query = 'INSERT INTO ' + DEVICE_RESOURCES_TABLE_NAME + '(' + \
                DEVICE_ID + ', ' + \
                CPU_USED + ', ' + \
                MEMORY_USED + ', ' + \
                CPU_MODEL + ', ' + \
                CPU_CORES + ', ' + \
                DRIVER_MODEL + ', ' + \
                DISKS + ', ' + \
                CHARGE + ', ' + \
                TIME_LEFT + ', ' + \
                BOOT_TIME + ', ' + \
                REQUEST_TIME + \
                ') VALUES(%d, \'%s\', \'%s\', \'%s\', %d, \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\');'
            cursor.execute(insert_query % (id,
                                           cpu_used,
                                           memory_used,
                                           cpu_model,
                                           cpu_cores,
                                           video_driver_model,
                                           disks,
                                           charge,
                                           time_left,
                                           boot_time,
                                           request_time))
            connection.commit()
        print("[INFO] Data was added")
    except Exception as ex:
        print(str(ex))
