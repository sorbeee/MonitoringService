-- CREATE DATABASE MonitoringService;

CREATE TABLE Device (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    ip VARCHAR(255),
    can_get_info BOOLEAN
);

CREATE TABLE DeviceActivity (
    device_id INTEGER REFERENCES Device(id) ON DELETE CASCADE,
    is_online BOOLEAN,
    last_ping TIMESTAMP,
    last_time_online TIMESTAMP
);


CREATE TABLE DeviceResources (
    device_id INTEGER REFERENCES Device(id) ON DELETE CASCADE,
    system VARCHAR(255),
    video_driver_model VARCHAR(255),
    cpu_model VARCHAR(255),
    cpu_used VARCHAR(255),
    physical_cores INTEGER,
    total_cores INTEGER,
    cores_used VARCHAR(1024),
    total_ram VARCHAR(255),
    used_free_ram VARCHAR(255),
    disks VARCHAR(1024),
    charge VARCHAR(255),
    time_left VARCHAR(255),
    boot_time TIMESTAMP,
    request_time TIMESTAMP
);


CREATE TABLE Action(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    execution_string_Windows VARCHAR(255),
    execution_string_Linux VARCHAR(255),
    execution_string_Darwin VARCHAR(255)
);


CREATE TABLE ActionList(
    device_id INTEGER REFERENCES Device(id) ON DELETE CASCADE,
    action_id INTEGER REFERENCES Action(id) ON DELETE CASCADE
);
