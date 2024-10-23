from postgres_orm import PostgresORM

HOST = ""
PORT = ""
USERNAME = ""
PASSWORD = ""
DB_NAME = ""
SCHEMA_NAME = ""

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
    "bookings",
    "subsystems",
    "maintenance_types",
    "maintenance_events",
    "aircraft_slots",
    "work_orders"
)

for table in filling_order:
    orm.fill_table(table=table, fillings=100)