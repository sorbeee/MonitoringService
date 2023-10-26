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
#     device_id INTEGER REFERENCES Device(id) ON DELETE CASCADE,
#     is_online BOOLEAN,
#     last_ping TIMESTAMP,
#     last_time_online TIMESTAMP
# );
#
# CREATE TABLE DeviceResources (
#   device_id INTEGER REFERENCES Device(id) ON DELETE CASCADE,
# 	system VARCHAR(255),
# 	video_driver_model VARCHAR(255),
#   cpu_model VARCHAR(255),
#   cpu_used VARCHAR(255),
# 	physical_cores INTEGER,
#   total_cores INTEGER,
# 	cores_used VARCHAR(1024),
#   total_ram VARCHAR(255),
# 	used_free_ram VARCHAR(255),
#   disks VARCHAR(1024),
#   charge VARCHAR(255),
#   time_left VARCHAR(255),
#   boot_time TIMESTAMP,
#   request_time TIMESTAMP
# );

import psycopg2
from config_utils import read_json, config_path

DEVICE_TABLE_NAME = 'Device'
ID = 'id'
DEVICE_NAME = 'name'
DEVICE_IP = 'ip'
DEVICE_NOTIFICATION = 'notification'

DEVICE_ACTIVITY_TABLE_NAME = 'DeviceActivity'
DEVICE_ID = 'device_id'
IS_ONLINE = 'is_online'
LAST_PING = 'last_ping'
LAST_TIME_ONLINE = 'last_time_online'

DEVICE_RESOURCES_TABLE_NAME = 'DeviceResources'
SYSTEM = 'system'
DRIVER_MODEL = 'video_driver_model'
CPU_MODEL = 'cpu_model'
CPU_USED = 'cpu_used'
PHYSICAL_CORES = 'physical_cores'
CORES_USED = 'cores_used'
TOTAL_CORES = 'total_cores'
TOTAL_RAM = 'total_ram'
USED_FREE_RAM = 'used_free_ram'
DISKS = 'disks'
CHARGE = 'charge'
TIME_LEFT = 'time_left'
BOOT_TIME = 'boot_time'
REQUEST_TIME = 'request_time'


def start_db():
    try:
        config = read_json(config_path)["DATABASE"]
        global connection
        connection = psycopg2.connect(
            host=config["HOSTNAME"],
            user=config["USERNAME"],
            password=config["PASSWORD"],
            database=config["DATABASE_NAME"]
        )
        print('[INFO] Connected to db')
        return connection
    except Exception as _ex:
        print("[INFO] error database", _ex.__cause__)


def select_all_devices():
    try:
        with connection.cursor() as cursor:
            select_query = 'SELECT * FROM ' + DEVICE_TABLE_NAME + ';'
            cursor.execute(select_query)
            return cursor.fetchall()
    except Exception as ex:
        print(str(ex))


def insert_device(name, ip, notification):
    try:
        with connection.cursor() as cursor:
            insert_query = 'INSERT INTO ' + DEVICE_TABLE_NAME + \
                           '(' + \
                           DEVICE_NAME + ', ' + \
                           DEVICE_IP + ', ' + \
                           DEVICE_NOTIFICATION + \
                           ') VALUES (\'%s\', \'%s\', %s);'

            cursor.execute(insert_query % (name, ip, notification))
            connection.commit()
            print("[INFO] Data was added")
    except Exception as ex:
        print(str(ex))


def update_device(id, notification):
    try:
        with connection.cursor() as cursor:
            insert_query = 'UPDATE ' + DEVICE_TABLE_NAME + \
                           ' SET ' + DEVICE_NOTIFICATION + ' = ' + str(notification) +\
                           ' WHERE ' + ID + ' = ' + str(id) + ';'

            cursor.execute(insert_query)
            connection.commit()
            print("[INFO] Data was updated")
            return True
    except Exception as ex:
        print(str(ex))
        return False

def remove_device(id):
    try:
        with connection.cursor() as cursor:
            delete_query = \
                'DELETE FROM ' + DEVICE_TABLE_NAME + ' WHERE ' + ID + ' = ' + str(id) + ';'

            cursor.execute(delete_query)
            connection.commit()
            print("[INFO] Data was updated")
            return True
    except Exception as ex:
        print(str(ex))
        return False


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
            select_query = 'SELECT * FROM ' + \
                           DEVICE_ACTIVITY_TABLE_NAME + \
                           ' WHERE ' + DEVICE_ID + ' = %d;'
            cursor.execute(select_query % id)
            return cursor.fetchall()
    except Exception as ex:
        print(str(ex))


def insert_resources(id,
                     system,
                     video_driver_model,
                     cpu_model,
                     cpu_used,
                     physical_cores,
                     total_cores,
                     cores_used,
                     total_ram,
                     used_free_ram,
                     disks,
                     charge,
                     time_left,
                     boot_time,
                     request_time):
    insert_query = 'INSERT INTO ' + DEVICE_RESOURCES_TABLE_NAME + '(' + \
                   DEVICE_ID + ', ' + \
                   SYSTEM + ', ' + \
                   DRIVER_MODEL + ', ' + \
                   CPU_MODEL + ', ' + \
                   CPU_USED + ', ' + \
                   PHYSICAL_CORES + ', ' + \
                   TOTAL_CORES + ', ' + \
                   CORES_USED + ', ' + \
                   TOTAL_RAM + ', ' + \
                   USED_FREE_RAM + ', ' + \
                   DISKS + ', ' + \
                   CHARGE + ', ' + \
                   TIME_LEFT + ', ' + \
                   BOOT_TIME + ', ' + \
                   REQUEST_TIME + \
                   ') VALUES(' \
                   '%d, \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', ' \
                   '\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\');'
    try:
        with connection.cursor() as cursor:
            cursor.execute(insert_query % (id,
                                           system,
                                           video_driver_model,
                                           cpu_model,
                                           cpu_used,
                                           physical_cores,
                                           total_cores,
                                           cores_used,
                                           total_ram,
                                           used_free_ram,
                                           disks,
                                           charge,
                                           time_left,
                                           boot_time,
                                           request_time))
            connection.commit()
        print("[INFO] Data was added")
    except Exception as ex:
        print(str(ex))


def select_all_activity():
    try:
        with connection.cursor() as cursor:
            select_query = 'SELECT ' + \
                           DEVICE_NAME + ', ' + \
                           DEVICE_IP + ', ' + \
                           IS_ONLINE + ', ' + \
                           LAST_TIME_ONLINE + ', ' + \
                           DEVICE_NOTIFICATION + \
                           ' FROM ' + \
                           DEVICE_ACTIVITY_TABLE_NAME + \
                           ' JOIN ' + \
                           DEVICE_TABLE_NAME + \
                           ' ON ' + \
                           ID + ' = ' + DEVICE_ID + ';'
            cursor.execute(select_query)
            return cursor.fetchall()
    except Exception as ex:
        print(str(ex))


def select_all_resources(id):
    try:
        select_query = 'SELECT ' + \
                       DEVICE_NAME + ', ' + \
                       DEVICE_IP + ', ' + \
                       SYSTEM + ', ' + \
                       DRIVER_MODEL + ', ' + \
                       CPU_MODEL + ', ' + \
                       CPU_USED + ', ' + \
                       PHYSICAL_CORES + ', ' + \
                       TOTAL_CORES + ', ' + \
                       CORES_USED + ', ' + \
                       TOTAL_RAM + ', ' + \
                       USED_FREE_RAM + ', ' + \
                       DISKS + ', ' + \
                       CHARGE + ', ' + \
                       TIME_LEFT + ', ' + \
                       BOOT_TIME + ', ' + \
                       REQUEST_TIME + \
                       ' FROM ' + \
                       DEVICE_RESOURCES_TABLE_NAME + \
                       ' JOIN ' + \
                       DEVICE_TABLE_NAME + \
                       ' ON ' + \
                       ID + ' = ' + DEVICE_ID + \
                       ' WHERE  ' + DEVICE_ID + ' = ' + str(id) + \
                       ' ORDER BY ' + REQUEST_TIME + ' DESC;'
        with connection.cursor() as cursor:
            cursor.execute(select_query)
            return cursor.fetchall()
    except Exception as ex:
        print(str(ex))


def select_ids():
    try:
        select_query = 'SELECT ' + ID + ' FROM ' + DEVICE_TABLE_NAME + ';'
        with connection.cursor() as cursor:
            cursor.execute(select_query)
            return cursor.fetchall()
    except Exception as ex:
        print(str(ex))
