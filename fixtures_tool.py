import sqlite3
import json
import sys
import time
import os


DB_PATH = "database.db"


def get_tables(conn):
    cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    return [row[0] for row in cur.fetchall()]


def export_all(output_file, tables=None):
    if not os.path.exists(DB_PATH):
        print(f"Error: Database file '{DB_PATH}' not found.")
        return

    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    start_time = time.perf_counter()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    if tables is None:
        tables = get_tables(conn)
    else:
        available_tables = get_tables(conn)
        tables = [t for t in tables if t in available_tables]
        if not tables:
            print("No valid tables specified for export.")
            conn.close()
            return

    result = {}

    for table in tables:
        cur = conn.execute(f"SELECT * FROM {table}")
        rows = [ dict(row) for row in cur.fetchall() ]
        result[table] = rows
        print( f'  - export {len(rows)} rows from {table}' )

    conn.close()

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


    end_time = time.perf_counter()
    duration = end_time - start_time

    print( f'Export took {duration:.4f} seconds' )
    print( f'Exported tables to {output_file}' )


def import_all(input_file, tables=None, keep_structure=True):
    if not os.path.exists(DB_PATH):
        print(f"Error: Database file '{DB_PATH}' not found.")
        return

    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return

    start_time = time.perf_counter()

    conn = sqlite3.connect(DB_PATH)

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    cur = conn.cursor()

    if tables is None:
        tables_to_import = list(data.keys())
    else:
        tables_to_import = [t for t in tables if t in data]
        if not tables_to_import:
            print("No valid tables specified for import.")
            conn.close()
            return

    for table in tables_to_import:
        if keep_structure:
            # Удаление таблицы с последующим созданием невозможно без схемы,
            # поэтому выдаем предупреждение и пропускаем
            print( f"Skipping drop table for {table} - structure reset not supported in this mode." )
            continue
        else:
            # Очистка данных, не удаляя структуру таблицы
            cur.execute( f"DELETE FROM {table}" )

        for row in data[table]:
            columns = ", ".join(row.keys())
            placeholders = ", ".join("?" for _ in row)
            values = list(row.values())
            cur.execute(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", values)

        print(f'  - import {len(data[table])} rows into {table}')

    conn.commit()
    conn.close()

    end_time = time.perf_counter()
    duration = end_time - start_time

    print( f'Import took {duration:.4f} seconds' )
    print( f'Imported data from {input_file}' )


def main():
    if len(sys.argv) < 3:
        print("Usage:\n" +
              "export <output_file.json> [table1 table2 ...]\n" +
              "import <input_file.json> [table1 table2 ...] [--no-keep-structure]")
        return

    command = sys.argv[1].lower()
    file_path = sys.argv[2]
    tables = None
    keep_structure = False

    if command == "export":
        if len(sys.argv) > 3:
            tables = sys.argv[3:]

        export_all(file_path, tables)

    elif command == "import":
        args = sys.argv[3:]

        if "--keep-structure" in args:
            keep_structure = True
            args.remove("--keep-structure")

        if args:
            tables = args

        import_all(file_path, tables, keep_structure)

    else:
        print("Unknown command. Use 'export' or 'import'.")


if __name__ == "__main__":
    main()
