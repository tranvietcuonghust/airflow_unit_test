class DatabaseTableBuilder:
  def __init__(self, database, schema):
    self.database = database
    self.schema = schema

  def create_template_table_sql(self, table_name, columns, data_types):
    #Ensure the number of columns matches the number of data types
    if len(columns) != len(data_types):
      raise ValueError("Number of columns must match number of data types.")

    #Zip together columns and data types
    column_definitions = [f"{col} {dtype}" for col, dtype in zip(columns, data_types)]

    #Generate the SQL query template
    sql_template = (
        f"CREATE TABLE IF NOT EXISTS ({self.database}.{self.schema}.{table_name} (\n"
        + ",\n".join(column_definitions)
        + "\n)"
    )

    return sql_template
  def update_template_table_sql(self, table_name, target_table, update_columns):
  
    # Set clause with comma-separated assignments
    set_clause = ", ".join([f"{target_table}.{col} = {table_name}.{col}" for col in update_columns])

    # Generate the UPDATE statement
    sql = f"""UPDATE {self.database}.{self.schema}.{target_table} AS {target_table}
               SET {set_clause}
               FROM {self.database}.{self.schema}.{table_name} AS {table_name}
               WHERE {target_table}.ID = {table_name}.ID"""
    return sql