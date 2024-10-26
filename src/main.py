from postgres_orm import PostgresORM

HOST = "localhost"
PORT = "5432"
USERNAME = "admin"
PASSWORD = "pass"
DB_NAME = "local_dm"
SCHEMA_NAME = "dm"

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
    "seats",
    "bookings",
    "subsystems",
    "maintenance_types",
    "maintenance_events",
    "aircraft_slots",
    "work_orders"
)

for table in filling_order:
    orm.fill_table(table=table, fillings=100)