
DROP TABLE IF EXISTS project1.customers CASCADE;
CREATE TABLE project1.customers 
(
    customer_id SERIAL PRIMARY KEY, --we are not storing passwords. OTP or other third-party services can be used.
    name varchar(255) NOT NULL, -- Name and Family name are stored together, could be split if needed
    email varchar(255) NOT NULL,
    phone_number varchar(255) NOT NULL,
    address varchar(255) NOT NULL
);

DROP TABLE IF EXISTS project1.aircrafts CASCADE;
CREATE TABLE project1.aircrafts (
    aircraft_registration_number SERIAL PRIMARY KEY, --unique, analog to car's plate
    aircraft_type varchar(255) NOT NULL,
    aircraft_company varchar(255) NOT NULL,
    aircraft_capacity int NOT NULL
);   

DROP TABLE IF EXISTS project1.airports CASCADE;
CREATE TABLE project1.airports (
    airport_id varchar(3) NOT NULL PRIMARY KEY, --unique, like LAX or JFK
    airport_name varchar(255) NOT NULL, 
    airport_city varchar(255) NOT NULL,
    airport_country varchar(255) NOT NULL
);   

DROP TABLE IF EXISTS project1.flights CASCADE;
CREATE TABLE project1.flights (
    flight_number varchar(6) NOT NULL PRIMARY KEY, --unique, mask AA9999, one flight_nubmer is used by multiple scheduler flights, like daily
    origin varchar(3) NOT NULL,
    destination varchar(3) NOT NULL,
    airline_id INT NOT NULL,
    flight_length INTERVAL NOT NULL,
    CONSTRAINT fk_origin_airport
        FOREIGN KEY (origin) REFERENCES project1.airports (airport_id),
    CONSTRAINT fk_destination_airport
        FOREIGN KEY (destination) REFERENCES project1.airports (airport_id),
    CONSTRAINT fk_airline_id
        FOREIGN KEY (airline_id) REFERENCES project1.airlines (airline_id)
); 

DROP TABLE IF EXISTS project1.airlines CASCADE;
CREATE TABLE project1.airlines (
    airline_id SERIAL PRIMARY KEY,
    airline_name varchar(255) NOT NULL
); 

DROP TABLE IF EXISTS project1.problems CASCADE;
CREATE TABLE project1.problems (
    problem_id SERIAL PRIMARY KEY,
    problem_type varchar(255) NOT NULL
); 

DROP TABLE IF EXISTS project1.flight_statuses CASCADE;
CREATE TABLE project1.flight_statuses (
    flight_status_id SERIAL PRIMARY KEY,
    flight_status_type varchar(255) NOT NULL
); 

DROP TABLE IF EXISTS project1.flight_data CASCADE;
CREATE TABLE project1.flight_data (
    flight_id SERIAL PRIMARY KEY, -- unique for each flight any aircraft does
    flight_number varchar(6) NOT NULL,
    aircraft_registration_number INT NOT NULL,
    flight_status_id INT NOT NULL,
    problem_id INT NOT NULL,
    number_of_passengers int NOT NULL, --could be counted from seats/bookings in next iteration
    number_of_cabin_crew int NOT NULL,
    number_of_flight_crew int NOT NULL,
    available_seating int NOT NULL, --could be counted from seats/bookings in next iteration
    scheduled_departure_date DATE NOT NULL,
    scheduled_departure_time TIME NOT NULL,
    CONSTRAINT fk_flight_number
        FOREIGN KEY (flight_number) REFERENCES project1.flights (flight_number),
    CONSTRAINT fk_aircraft_registration_number
        FOREIGN KEY (aircraft_registration_number) REFERENCES project1.aircrafts (aircraft_registration_number),
    CONSTRAINT fk_flight_status_id
        FOREIGN KEY (flight_status_id) REFERENCES project1.flight_statuses (flight_status_id),
    CONSTRAINT fk_problem_id
        FOREIGN KEY (problem_id) REFERENCES project1.problems (problem_id)
); 


DROP TABLE IF EXISTS project1.seat_classes CASCADE;
CREATE TABLE project1.seat_classes 
(
    seat_number varchar(3) NOT NULL PRIMARY KEY, --1a to 40f, considering that all the aircrafts have the same seatings
    seat_class varchar(33) NOT NULL, --rows 1 - 3 are business and rows 4 - 40 are economy for all the aircrafts
    CONSTRAINT fk_seat_number
        FOREIGN KEY (seat_number) REFERENCES project1.seat_classes (seat_number)
);


DROP TABLE IF EXISTS project1.seats CASCADE;
CREATE TABLE project1.seats 
(
    seat_id SERIAL PRIMARY KEY,
    seat_number varchar(3) NOT NULL, -- foreign key
    seat_status varchar(33) NOT NULL, --available or occupied, could be pulled from bookings in next iteration
    flight_id INT NOT null, -- foreign_key
    CONSTRAINT fk_flight_id
        FOREIGN KEY (flight_id) REFERENCES project1.flight_data (flight_id),
    CONSTRAINT fk_seat_number
        FOREIGN KEY (seat_number) REFERENCES project1.seat_classes (seat_number)
);

DROP TABLE IF EXISTS project1.bookings CASCADE;
CREATE TABLE project1.bookings (
    booking_id SERIAL PRIMARY KEY, --used as confirmation code as it it unique. Now we a restricted to 1 seat per booking.
    flight_id INT NOT NULL, --might be removed from this table as thin information can be pulled from seat_id, but for ow we prefer to keep straing connection with flight_data
    customer_id INT NOT NULL,
    seat_id INT NOT NULL,
    price NUMERIC(7,2) NOT NULL,
    payment_status BOOLEAN NOT NULL,
    CONSTRAINT fk_flight_id
        FOREIGN KEY (flight_id) REFERENCES project1.flight_data (flight_id),
    CONSTRAINT fk_customer_id
        FOREIGN KEY (customer_id) REFERENCES project1.customers (customer_id),
    CONSTRAINT fk_seat_id
        FOREIGN KEY (seat_id) REFERENCES project1.seats (seat_id)
); 

DROP TABLE IF EXISTS project1.subsystems CASCADE;
CREATE TABLE project1.subsystems (
    subsystem_id SERIAL PRIMARY KEY,
    subsystem_type varchar(255) NOT NULL
); 

DROP TABLE IF EXISTS project1.maintenance_types CASCADE;
CREATE TABLE project1.maintenance_types (
    maintenance_type_id SERIAL PRIMARY KEY,
    maintenance_type_name varchar(255) NOT NULL
); 

DROP TABLE IF EXISTS project1.maintenance_events CASCADE;
CREATE TABLE project1.maintenance_events (
    maintenance_id SERIAL PRIMARY KEY,
    aircraft_registration_number INT NOT NULL,
    maintenance_starttime TIMESTAMP NOT NULL,
    duration INTERVAL NOT NULL,
    airport_id VARCHAR(3) NOT NULL, --where the maintenance is taking place
    subsystem_id INT NOT NULL, --which subsystem is being maintained
    maintenance_type_id INT NOT NULL, 
    CONSTRAINT fk_aircraft_registration_number
        FOREIGN KEY (aircraft_registration_number) REFERENCES project1.aircrafts (aircraft_registration_number),
    CONSTRAINT fk_airport_id
        FOREIGN KEY (airport_id) REFERENCES project1.airports (airport_id),
    CONSTRAINT fk_subsystem_id
        FOREIGN KEY (subsystem_id) REFERENCES project1.subsystems (subsystem_id),
    CONSTRAINT fk_maintenance_type_id
        FOREIGN KEY (maintenance_type_id) REFERENCES project1.maintenance_types (maintenance_type_id)
); 

DROP TABLE IF EXISTS project1.aircraft_slots CASCADE;
CREATE TABLE project1.aircraft_slots (
    aircraft_slot_id SERIAL PRIMARY KEY,
    aircraft_registration_number INT NOT NULL,
    slot_start TIMESTAMP NOT NULL,
    slot_end TIMESTAMP NOT NULL,
    slot_type VARCHAR(255) NOT NULL,
    slot_scheduled BOOLEAN NOT NULL,
    maintenance_id INT NOT NULL, 
    CONSTRAINT fk_aircraft_registration_number
        FOREIGN KEY (aircraft_registration_number) REFERENCES project1.aircrafts (aircraft_registration_number),
    CONSTRAINT fk_maintenance_id
        FOREIGN KEY (maintenance_id) REFERENCES project1.maintenance_events (maintenance_id)
); 

DROP TABLE IF EXISTS project1.reporteurs CASCADE;
CREATE TABLE project1.reporteurs (
    reporteur_id SERIAL PRIMARY KEY, -- can be replaced with worker_id if we will store tables with all the staff of all the airports and aircompanies
    reporteur_class varchar(255) NOT NULL,
    reporteur_name varchar(255) NOT NULL
); 

DROP TABLE IF EXISTS project1.work_orders CASCADE;
CREATE TABLE project1.work_orders (
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
    reporting_date TIMESTAMP NOT NULL, --worker_id can be added as a foreign key if we will store tables with all the staff of all the airports and aircompanies
    CONSTRAINT fk_aircraft_registration_number
        FOREIGN KEY (aircraft_registration_number) REFERENCES project1.aircrafts (aircraft_registration_number),
    CONSTRAINT fk_maintenance_id
        FOREIGN KEY (maintenance_id) REFERENCES project1.maintenance_events (maintenance_id),
    CONSTRAINT fk_airport_id
        FOREIGN KEY (airport_id) REFERENCES project1.airports (airport_id),
    CONSTRAINT fk_reporteur_id
        FOREIGN KEY (reporteur_id) REFERENCES project1.reporteurs (reporteur_id)
); 
