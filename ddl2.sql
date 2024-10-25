DROP TABLE IF EXISTS seats;
CREATE TABLE seats 
(
    seat_id SERIAL PRIMARY KEY,
    seat_number varchar(3) NOT NULL, --1a to 40f
    seat_class varchar(33) NOT NULL, --rows 1 - 3 are business and rows 4 - 40 are economy
    seat_status varchar(33) NOT NULL, --available or occupied
    flight_id INT NOT NULL -- foreign key
    CONSTRAINT fk_flight_id
        FOREIGN KEY (flight_id) REFERENCES flight_data (flight_id)
);


ALTER TABLE bookings
    DROP COLUMN seat_class;
ALTER TABLE bookings
    ADD seat_id INT;
ALTER TABLE bookings
    ADD CONSTRAINT fk_seat_id
        FOREIGN KEY (seat_id) REFERENCES seats (seat_id)
        