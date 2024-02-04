import aiosql
import psycopg
from psycopg.rows import dict_row
import yaml

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

queries = aiosql.from_path("queries.sql", "psycopg")

foreigntables = []

conn = psycopg.connect(config['main']['connstring'], row_factory=dict_row)
connft = psycopg.connect(config['fdw']['connstring'], row_factory=dict_row)


def concatecolumns(columns: dict) -> str:
    result = ""
    for value in columns.values():
        result += str(value) + " "
    return result


def comparecolumns(columns: list, column: dict) -> None:
    """

    :param columns:
    :param column:
    :return:
    """
    for row in columns:
        if row['column_name'] == column['column_name']:
            print("comparing colunn: " + str(column['column_name']))
            values = concatecolumns(row)
            ftvalues = concatecolumns(column)
            if values != ftvalues:
                print("ALARM")



def compareforeigntable(table: str, schema: str, columns: list) -> None:
    """
    compares the given columns with the columns of the given table
    :param table:
    :param schema:
    :param columns:
    :return:
    """
    tabledefinition = queries.get_table_definition(connft, table_name=table, table_schema=schema)
    print("comparing table: " + str(table) + "." + str(schema))
    for column in tabledefinition:
        comparecolumns(columns, column)


def getforeigntables() -> None:
    """
    Is getting all the foreign tables and their column definitions.
    """
    fts = queries.get_foreign_tables(conn, foreignserver=config['main']['foreignserver'])
    for ft in fts:
        print(ft)
        foreigntables.append(ft)

    for table in foreigntables:
        tabledefinition = queries.get_table_definition(conn, table_name=table['foreign_table_name'], table_schema=table['foreign_table_schema'])
        columns = []
        for column in tabledefinition:
            columns.append(column)
        compareforeigntable(table['table_name'], table['schema_name'], columns)


if __name__ == "__main__":
    print("Hello World!")
    getforeigntables()
    conn.close()
    connft.close()