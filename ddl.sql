DROP TABLE IF EXISTS customers;
CREATE TABLE customers 
(
    customer_id SERIAL PRIMARY KEY,
    name varchar(255) NOT NULL,
    email varchar(255) NOT NULL,
    phone_number varchar(255) NOT NULL,
    address varchar(255) NOT NULL
);

DROP TABLE IF EXISTS aircrafts;
CREATE TABLE aircrafts (
    aircraft_registration_number SERIAL PRIMARY KEY,
    aircraft_type varchar(255) NOT NULL,
    aircraft_company varchar(255) NOT NULL,
    aircraft_capacity int NOT NULL
);   

DROP TABLE IF EXISTS airports;
CREATE TABLE airports (
    airport_id varchar(3) NOT NULL PRIMARY KEY,
    airport_name varchar(255) NOT NULL,
    airport_city varchar(255) NOT NULL,
    airport_country varchar(255) NOT NULL
);   

DROP TABLE IF EXISTS flights;
CREATE TABLE flights (
    flight_number varchar(6) NOT NULL PRIMARY KEY,
    origin varchar(3) NOT NULL,
    destination varchar(3) NOT NULL,
    date DATE NOT NULL,
    time TIMESTAMP NOT NULL,
    CONSTRAINT fk_origin_airport
        FOREIGN KEY (origin) REFERENCES airports (airport_id),
    CONSTRAINT fk_destination_airport
        FOREIGN KEY (destination) REFERENCES airports (airport_id)
); 

DROP TABLE IF EXISTS airlines;
CREATE TABLE airlines (
    airline_id SERIAL PRIMARY KEY,
    airline_name varchar(255) NOT NULL
); 

DROP TABLE IF EXISTS problems;
CREATE TABLE problems (
    problem_id SERIAL PRIMARY KEY,
    problem_type varchar(255) NOT NULL
); 

DROP TABLE IF EXISTS flight_statuses;
CREATE TABLE flight_statuses (
    flight_status_id SERIAL PRIMARY KEY,
    flight_status_type varchar(255) NOT NULL
); 

DROP TABLE IF EXISTS flight_data;
CREATE TABLE flight_data (
    flight_id SERIAL PRIMARY KEY,
    flight_number varchar(6) NOT NULL,
    aircraft_registration_number INT NOT NULL,
    airline_id INT NOT NULL,
    flight_status_id INT NOT NULL,
    problem_id INT NOT NULL,
    number_of_passengers int NOT NULL,
    number_of_cabin_crew int NOT NULL,
    number_of_flight_crew int NOT NULL,
    available_seating int NOT NULL,
    CONSTRAINT fk_flight_number
        FOREIGN KEY (flight_number) REFERENCES flights (flight_number),
    CONSTRAINT fk_aircraft_registration_number
        FOREIGN KEY (aircraft_registration_number) REFERENCES aircrafts (aircraft_registration_number),
    CONSTRAINT fk_airline_id
        FOREIGN KEY (airline_id) REFERENCES airlines (airline_id),
    CONSTRAINT fk_flight_status_id
        FOREIGN KEY (flight_status_id) REFERENCES flight_statuses (flight_status_id),
    CONSTRAINT fk_problem_id
        FOREIGN KEY (problem_id) REFERENCES problems (problem_id)
); 

DROP TABLE IF EXISTS bookings;
CREATE TABLE bookings (
    booking_id SERIAL PRIMARY KEY,
    flight_id INT NOT NULL,
    customer_id INT NOT NULL,
    seat_class VARCHAR(255) NOT NULL,
    price NUMERIC(7,2) NOT NULL,
    payment_status BOOLEAN NOT NULL,
    CONSTRAINT fk_flight_id
        FOREIGN KEY (flight_id) REFERENCES flight_data (flight_id),
    CONSTRAINT fk_customer_id
        FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
); 

DROP TABLE IF EXISTS subsystems;
CREATE TABLE subsystems (
    subsystem_id SERIAL PRIMARY KEY,
    subsystem_type varchar(255) NOT NULL
); 

DROP TABLE IF EXISTS maintenance_types;
CREATE TABLE maintenance_types (
    maintenance_type_id SERIAL PRIMARY KEY,
    maintenance_type_name varchar(255) NOT NULL
); 

DROP TABLE IF EXISTS maintenance_events;
CREATE TABLE maintenance_events (
    maintenance_id SERIAL PRIMARY KEY,
    aircraft_registration_number INT NOT NULL,
    maintenance_starttime TIMESTAMP NOT NULL,
    duration INTERVAL NOT NULL,
    airport_id VARCHAR(3) NOT NULL,
    subsystem_id INT NOT NULL,
    maintenance_type_id INT NOT NULL,
    CONSTRAINT fk_aircraft_registration_number
        FOREIGN KEY (aircraft_registration_number) REFERENCES aircrafts (aircraft_registration_number),
    CONSTRAINT fk_airport_id
        FOREIGN KEY (airport_id) REFERENCES airports (airport_id),
    CONSTRAINT fk_subsystem_id
        FOREIGN KEY (subsystem_id) REFERENCES subsystems (subsystem_id),
    CONSTRAINT fk_maintenance_type_id
        FOREIGN KEY (maintenance_type_id) REFERENCES maintenance_types (maintenance_type_id)
); 

DROP TABLE IF EXISTS aircraft_slots;
CREATE TABLE aircraft_slots (
    aircraft_slot_id SERIAL PRIMARY KEY,
    aircraft_registration_number INT NOT NULL,
    slot_start TIMESTAMP NOT NULL,
    slot_end TIMESTAMP NOT NULL,
    slot_type VARCHAR(255) NOT NULL,
    slot_scheduled BOOLEAN NOT NULL,
    maintenance_id INT NOT NULL,
    CONSTRAINT fk_aircraft_registration_number
        FOREIGN KEY (aircraft_registration_number) REFERENCES aircrafts (aircraft_registration_number),
    CONSTRAINT fk_maintenance_id
        FOREIGN KEY (maintenance_id) REFERENCES maintenance_events (maintenance_id)
); 

DROP TABLE IF EXISTS reporteurs;
CREATE TABLE reporteurs (
    reporteur_id SERIAL PRIMARY KEY,
    reporteur_class varchar(255) NOT NULL,
    reporteur_name varchar(255) NOT NULL
); 

DROP TABLE IF EXISTS work_orders;
CREATE TABLE work_orders (
    work_order_id SERIAL PRIMARY KEY,
    aircraft_registration_number INT NOT NULL,
    maintenance_id INT NOT NULL,
    airport_id VARCHAR(3) NOT NULL,
    execution_date TIMESTAMP NOT NULL,
    scheduled BOOLEAN NOT NULL,
    forecasted_date TIMESTAMP NOT NULL,
    forecasted_manhours NUMERIC(7,2) NOT NULL,
    frequency INT NOT NULL,
    reporteur_id INT NOT NULL,
    due_date TIMESTAMP NOT NULL,
    reporting_date TIMESTAMP NOT NULL,
    CONSTRAINT fk_aircraft_registration_number
        FOREIGN KEY (aircraft_registration_number) REFERENCES aircrafts (aircraft_registration_number),
    CONSTRAINT fk_maintenance_id
        FOREIGN KEY (maintenance_id) REFERENCES maintenance_events (maintenance_id),
    CONSTRAINT fk_airport_id
        FOREIGN KEY (airport_id) REFERENCES airports (airport_id),
    CONSTRAINT fk_reporteur_id
        FOREIGN KEY (reporteur_id) REFERENCES reporteurs (reporteur_id)
); 
