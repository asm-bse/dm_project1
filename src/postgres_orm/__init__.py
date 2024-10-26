import psycopg2
from datetime import timedelta
from faker import Faker
import psycopg2._psycopg

class PostgresORM:
    def __init__(self, host: str, port: str, username: str, password: str, db_name: str, schema_name: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.db_name = db_name

        self.schema_name = schema_name

        self.connection = self.get_connection()
        if self.connection is None:
            raise ConnectionError(f'Can not connect to {self.db_name}')
    
        self.cursor = self.get_cursor()
        
        self.faker = Faker()

        self.filling_mapper = {
            table: getattr(self, f'_PostgresORM__fill_{table}')
            for table in self.get_tables()
        }

    def get_connection(self) -> psycopg2._psycopg.connection:
        try:
            connection = psycopg2.connect(
                dbname=self.db_name,
                user=self.username,
                password=self.password,
                host=self.host,
                port=self.port
            )
            print(f'Successfully connected to {self.db_name}')
            return connection
        except Exception as e:
            print(e)
            return None

    def get_cursor(self) -> psycopg2._psycopg.cursor:
        if self.connection:
            return self.connection.cursor()
        else:
            return None

    def get_tables(self) -> list[str]:
        try:
            self.cursor.execute(f"""SELECT table_name FROM information_schema.tables 
                               WHERE table_schema = '{self.schema_name}'""")
            
            return [table[0] for table in self.cursor.fetchall()]
        except Exception as e:
            print(f'Can not get tables from {self.db_name}')

    def get_table_ids(self, table: str, column: str) -> list[int]:
        query = f"SELECT {column} FROM {self.schema_name}.{table}"
        
        self.cursor.execute(query)
        
        results = self.cursor.fetchall()
        
        return [result[0] for result in results]

    def get_table_content(self, table: str) -> list[dict]:
        try:
            self.cursor.execute(f"SELECT * FROM {self.schema_name}.{table}")

            columns = [desc[0] for desc in self.cursor.description]

            return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Error retrieving data from {table}. Error - {e}")
            return []
            
    def __fill_airlines(self, fillings: int) -> bool:
        try:
            for _ in range(fillings):
                airline_name = f'{self.faker.company()} Air'
                self.cursor.execute(
                    f'INSERT INTO {self.schema_name}.airlines (airline_name) VALUES (%s)',
                    (airline_name,)
                )
                self.connection.commit()
        except Exception as e: 
            print(e)

            return False
    
        return True
    
    def occupy_seats(self, seat_ids: list[int]) -> None:
        try:
            query = f"UPDATE {self.schema_name}.seats SET seat_status = 'Occupied' WHERE seat_id = ANY(%s)"
            
            self.cursor.execute(query, (seat_ids,))
            
            self.connection.commit()

            print(f"Successfully updated {len(seat_ids)} seats to 'Occupied' status.")
        except Exception as e:
            print(f"Failed to update seat status: {e}")

            return False
        
        return True
    
    def __fill_seats(self, fillings: int) -> bool:
        try:
            flight_ids = self.get_table_ids("flight_data", "flight_id")

            rows = range(1, 41)
            seat_letters = ["A", "B", "C", "D", "E", "F"]

            for flight_id in flight_ids:
                for row in rows:
                    for letter in seat_letters:
                        seat_number = f"{row}{letter}"
                        seat_class =  "Business" if row <= 3 else "First Class" if row <= 6 else "Economy"
                        seat_status = "Available"

                        self.cursor.execute(
                            f"INSERT INTO {self.schema_name}.seats (seat_number, seat_class, seat_status, flight_id) VALUES (%s, %s, %s, %s)",
                            (seat_number, seat_class, seat_status, flight_id)
                        )

                        self.connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

            return False
        
        return True
        
    def __fill_customers(self, fillings: int) -> bool:
        try:
            for _ in range(fillings):
                name = self.faker.name()
                email = self.faker.email(domain="google.com")
                phone_number = self.faker.phone_number()
                address = self.faker.address()
                self.cursor.execute(
                    f'INSERT INTO {self.schema_name}.customers (name, email, phone_number, address) VALUES (%s, %s, %s, %s)',
                    (name, email, phone_number, address)
                )
                self.connection.commit()
        except Exception as e:
            print(e)

            return False
        
        return True
    
    def __fill_bookings(self, fillings: int) -> bool:
        occupied_seats = []
        try:
            for _ in range(fillings):
                customer_id = self.faker.random.choice(self.get_table_ids(table="customers", column="customer_id"))
                flight_id = self.faker.random.choice(self.get_table_ids(table="flight_data", column="flight_id"))

                seat = self.faker.random.choice(self.get_table_ids(table="seats", column="seat_id"))
                occupied_seats.append(seat)

                price = round(self.faker.random.uniform(50, 1000), 2)
                payment_status = self.faker.boolean()

                self.cursor.execute(
                    f'INSERT INTO {self.schema_name}.bookings (flight_id, customer_id, seat_id, price, payment_status) VALUES (%s, %s, %s, %s, %s)',
                    (flight_id, customer_id, seat, price, payment_status)
                )

                self.connection.commit()
        except Exception as e:
            print(f"Failed to fill bookings table: {e}")

            return False

        self.occupy_seats(occupied_seats)

        return True

    def __fill_work_orders(self, fillings: int) -> bool:
        try:
            aircraft_ids = self.get_table_ids("aircrafts", "aircraft_registration_number")
            maintenance_ids = self.get_table_ids("maintenance_events", "maintenance_id")
            airport_ids = self.get_table_ids("airports", "airport_id")
            reporteur_ids = self.get_table_ids("reporteurs", "reporteur_id")
            
            for _ in range(fillings):
                aircraft_id = self.faker.random.choice(aircraft_ids)
                maintenance_id = self.faker.random.choice(maintenance_ids)
                airport_id = self.faker.random.choice(airport_ids)
                reporteur_id = self.faker.random.choice(reporteur_ids)
                
                reporting_date = self.faker.date_between(start_date="-2y", end_date="today")
                forecasted_date = self.faker.date_between(start_date=reporting_date, end_date="+1y")
                due_date = self.faker.date_between(start_date=forecasted_date, end_date="+1y")
                execution_date = self.faker.date_between(start_date=reporting_date, end_date="+1y")
                
                scheduled = self.faker.boolean()
                forecasted_manhours = self.faker.random_number(fix_len=True, digits=1)
                frequency = self.faker.random_number(fix_len=True, digits=1)
                
                self.cursor.execute(
                    f"INSERT INTO {self.schema_name}.work_orders (aircraft_registration_number, maintenance_id, airport_id, execution_date, scheduled, forecasted_date, forecasted_manhours, frequency, reporteur_id, due_date, reporting_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (aircraft_id, maintenance_id, airport_id, execution_date, scheduled, forecasted_date, forecasted_manhours, frequency, reporteur_id, due_date, reporting_date)
                )
            
                self.connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

            return False
        
        return True
    
    def __fill_aircrafts(self, fillings: int) -> bool:
        try:
            for _ in range(fillings):
                aircraft_type = self.faker.random.choice(['Boeing 737', 'Airbus A320', 'Boeing 777', 'Airbus A350'])
                aircraft_company = f'{self.faker.company()}'
                aircraft_capacity = 300 #self.faker.random.randint(100, 400)

                self.cursor.execute(
                    f'INSERT INTO {self.schema_name}.aircrafts (aircraft_type, aircraft_company, aircraft_capacity) VALUES (%s, %s, %s)',
                    (aircraft_type, aircraft_company, aircraft_capacity)
                )

                self.connection.commit() 
        except Exception as e:
            print(e)
            
            return False
    
        return True
    
    def __fill_airports(self, fillings: int = 100) -> bool:
        try:
            for _ in range(fillings): 
                airport_id = self.faker.bothify(text='???').upper()
                if airport_id in self.get_table_ids(table="airports", column="airport_id"):
                    continue
                airport_name = f'{self.faker.company()} Airport'
                airport_city = self.faker.city()
                airport_country = self.faker.country()

                self.cursor.execute(
                    f'INSERT INTO {self.schema_name}.airports (airport_id, airport_name, airport_city, airport_country) VALUES (%s, %s, %s, %s)',
                    (airport_id, airport_name, airport_city, airport_country)
                )

                self.connection.commit()  
        except Exception as e:
            print(f"Failed to fill airports table: {e}")
            
            return False

        return True
    
    def __fill_aircraft_slots(self, fillings: int) -> bool:
        try:
            aircraft_ids = self.get_table_ids("aircrafts", "aircraft_registration_number")
            maintenance_ids = self.get_table_ids("maintenance_events", "maintenance_id")
            slot_types = ["Maintenance", "Cleaning", "Inspection", "Repair"]
            scheduled_statuses = [True, False] 

            for _ in range(fillings):
                aircraft_registration_number = self.faker.random.choice(aircraft_ids)
                maintenance_id = self.faker.random.choice(maintenance_ids)
                slot_type = self.faker.random.choice(slot_types)
                slot_scheduled = self.faker.random.choice(scheduled_statuses)

                start_time = self.faker.date_time_between(start_date="-1y", end_date="now")
                end_time = start_time + self.faker.random_element(elements=[timedelta(hours=h) for h in range(1, 13)])  # Добавляем от 1 до 12 часов

                self.cursor.execute(
                    f"INSERT INTO {self.schema_name}.aircraft_slots (aircraft_registration_number, slot_start, slot_end, slot_type, slot_scheduled, maintenance_id) VALUES (%s, %s, %s, %s, %s, %s)",
                    (aircraft_registration_number, start_time, end_time, slot_type, slot_scheduled, maintenance_id)
                )

                self.connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

            return False
        
        return True
    
    def __fill_flights(self, fillings: int) -> bool:
        try: 
            airports = self.get_table_ids(table="airports", column="airport_id")
            for _ in range(int(fillings / 5)):
                flight_number = f'{self.faker.bothify(text="??").upper()}{self.faker.random_number(fix_len=True, digits=4)}'

                origin = self.faker.random.choice(airports)
                destination = self.faker.random.choice(airports)
                
                date = self.faker.date_between(start_date="-1y", end_date="today").isoformat()
                time = self.faker.date_time_between(start_date="-1y", end_date="now").strftime('%Y-%m-%d %H:%M:%S')

                self.cursor.execute(
                    f'INSERT INTO {self.schema_name}.flights (flight_number, origin, destination, date, time) VALUES (%s, %s, %s, %s, %s)',
                    (flight_number, origin, destination, date, time)
                    )
            
                self.connection.commit()
        except Exception as e:
            print(f'An error occurred: {e}')

            return False
        
        return True
    
    def __fill_maintenance_events(self, fillings: int) -> bool:
        try:
            aircraft_ids = self.get_table_ids("aircrafts", "aircraft_registration_number")
            airport_ids = self.get_table_ids("airports", "airport_id")
            subsystem_ids = self.get_table_ids("subsystems", "subsystem_id")
            maintenance_type_ids = self.get_table_ids("maintenance_types", "maintenance_type_id")

            for _ in range(fillings):
                aircraft_reg = self.faker.random.choice(aircraft_ids)
                airport_id = self.faker.random.choice(airport_ids)
                subsystem_id = self.faker.random.choice(subsystem_ids)
                maintenance_type_id = self.faker.random.choice(maintenance_type_ids)

                maintenance_starttime = self.faker.date_time_between(start_date="-1y", end_date="now").strftime('%Y-%m-%d %H:%M:%S')
                
                duration_hours = self.faker.random.randint(1, 12)  
                duration = f"{duration_hours} hours" 

                self.cursor.execute(
                    f"INSERT INTO {self.schema_name}.maintenance_events (aircraft_registration_number, maintenance_starttime, duration, airport_id, subsystem_id, maintenance_type_id) VALUES (%s, %s, %s, %s, %s, %s)",
                    (aircraft_reg, maintenance_starttime, duration, airport_id, subsystem_id, maintenance_type_id)
                )

                self.connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

            return False
        
        return True
    
    def __fill_subsystems(self, fillings: int) -> bool:
        try:
            subsystem_types = ["Engine", "Avionics", "Hydraulics", "Landing Gear", "Fuel System", "Electrical System"]
            for _ in range(6):
                subsystem_type = self.faker.random.choice(subsystem_types)

                self.cursor.execute(
                    f"INSERT INTO {self.schema_name}.subsystems (subsystem_type) VALUES (%s)",
                    (subsystem_type,)
                )
                self.connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

            return False

        return True
    
    def __fill_maintenance_types(self, fillings: int) -> bool:
        try:
            maintenance_type_names = ["Routine Check", "Engine Repair", "Scheduled Maintenance", "Emergency Repair", "Software Update"]
            for _ in range(fillings):
                maintenance_type_name = self.faker.random.choice(maintenance_type_names)

                self.cursor.execute(
                    f"INSERT INTO {self.schema_name}.maintenance_types (maintenance_type_name) VALUES (%s)",
                    (maintenance_type_name,)
                )
                self.connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

            return False
        
        return True
    
    def __fill_reporteurs(self, fillings: int):
        try:
            for _ in range(fillings):
                reporteur_class = self.faker.random.choice(["Steward", "Pilot", "Mechanic"])
                reporteur_name = self.faker.name()

                self.cursor.execute(
                        f'INSERT INTO {self.schema_name}.reporteurs (reporteur_class, reporteur_name) VALUES (%s, %s)',
                        (reporteur_class, reporteur_name)
                    )
                
                self.connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

            return False
        
        return True
    
    def __fill_reportuers(self, fillings: int):
        try:
            for _ in range(fillings):
                reporteur_class = self.faker.random.choice(["class1", "class2", "class3"])
                reporteur_name = self.faker.random.choice(["name1", "name2", "name3"])

                self.cursor.execute(
                        f'INSERT INTO {self.schema_name}.reporteurs (reporteur_class, reporteur_name) VALUES (%s, %s)',
                        (reporteur_class, reporteur_name)
                    )
                
                self.connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

            return False
        
        return True
    
    def __get_capacity_of_aircraft(self, aircraft: int) -> int:
        query = f"SELECT aircraft_capacity FROM {self.schema_name}.aircrafts WHERE aircraft_registration_number = %s"
        
        self.cursor.execute(query, (aircraft,))
        
        result = self.cursor.fetchone() 
        
        return result[0] if result else None
    
    def __fill_flight_data(self, fillings: int = 100) -> bool:
        pks = {
            "airlines": "airline_id",
            "flights": "flight_number",
            "airports": "airport_id",
            "flight_statuses": "flight_status_id",
            "aircrafts": "aircraft_registration_number",
            "problems": "problem_id"
        }
        pks_content = {}

        for table, column in pks.items():
            ids = self.get_table_ids(table, column)
            pks_content[column] = ids

        try:
            for _ in range(100):
                aircraft_reg = self.faker.random.choice(pks_content["aircraft_registration_number"])
                capacity_of_aircraft = self.__get_capacity_of_aircraft(aircraft=aircraft_reg)
                number_of_passangers = int(0.9 * capacity_of_aircraft)
                number_of_cabin_crew = self.faker.random_number(fix_len=True, digits=1)
                number_of_flight_crew = self.faker.random_number(fix_len=True, digits=1)
                available_seating = capacity_of_aircraft - number_of_passangers

                self.cursor.execute(
                    f'INSERT INTO {self.schema_name}.flight_data (flight_number, aircraft_registration_number, airline_id, flight_status_id, problem_id, number_of_passengers, number_of_cabin_crew, number_of_flight_crew, available_seating) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (
                        self.faker.random.choice(pks_content["flight_number"]),
                        aircraft_reg,
                        self.faker.random.choice(pks_content["airline_id"]),
                        self.faker.random.choice(pks_content["flight_status_id"]),
                        self.faker.random.choice(pks_content["problem_id"]),
                        number_of_passangers,
                        number_of_cabin_crew,
                        number_of_flight_crew,
                        available_seating
                    )
                )

                self.connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

            return False
        
        return True
    
    def __fill_flight_statuses(self, fillings: int) -> bool:
        try:
            flight_statuses = [
                "Cancelled",
                "Delayed",
                "On-time"
            ]
            for status in flight_statuses:
                self.cursor.execute(
                    f'INSERT INTO {self.schema_name}.flight_statuses (flight_status_type) VALUES (%s)',
                    (status,)
                )

            self.connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

            return False
        
        return True
    
    def __fill_problems(self, fillings: int) -> bool:
        try:
            problem_types = [
                "Engine Failure",
                "Avionics Issue",
                "Fuel System Leak",
                "Hydraulic Failure",
                "Tire Damage",
                "Wing Deformity",
                "Sensor Malfunction",
                "Landing Gear Issue",
                "Cabin Pressure Problem",
                "Electrical System Issue"
            ]
            
            for problem_type in problem_types:
                self.cursor.execute(
                    f'INSERT INTO {self.schema_name}.problems (problem_type) VALUES (%s)',
                    (problem_type,)
                )

            self.connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

            return False
        
        return True
    
    def fill_table(self, table: str, fillings: int = 100) -> bool:
        fill = self.filling_mapper[table](fillings)
        if fill:
            print(f'Successfully filled {table} with {fillings}')
        else:
            print(f'Can not fill {table}')