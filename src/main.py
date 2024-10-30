from postgres_orm import PostgresORM

HOST = "89.110.124.197"
PORT = "5432"
USERNAME = "smolin"
PASSWORD = "smolin_pass1"
DB_NAME = "dmdb1"
SCHEMA_NAME = "project1"

orm = PostgresORM(
    host=HOST,
    port=PORT,
    username=USERNAME,
    password=PASSWORD,
    db_name=DB_NAME,
    schema_name=SCHEMA_NAME
)

filling_order = (
    "customers",
    "airlines",
    "airports",
    "flights",
    "reporteurs",
    "aircrafts",
    "flight_statuses",
    "problems",
    "flight_data",
    "seat_classes",
    "seats",
    "bookings",
    "subsystems",
    "maintenance_types",
    "maintenance_events",
    "aircraft_slots",
    "work_orders"
)

for table in filling_order:
    result = orm.fill_table(table=table, fillings=100)