"""
Extra - Insertar los datos a la base de datos automaticamente los datos que esten en excel (ESTO EJECUTA EL PROCEDURE CREADO)
"""

import pandas as pd
import pyodbc

# Configurar la conexión a SQL Server
server = 'LAPTOP-DE-ALAN' # Cambiar
db = 'prueba' # Cambiar
cone = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={db};Trusted_Connection=yes'

# Leer el archivo Excel 
excel_file = 'BASE_DATOS_ACTUALIZADA.xlsx'
df = pd.read_excel(excel_file)

# Conectar a SQL Server y ejecutar el procedimiento almacenado para insertar los datos
try:
    # Conectar a SQL Server
    conn = pyodbc.connect(cone)
    cursor = conn.cursor()
    print("Conexión exitosa a SQL Server")
    
    # Recorrer las filas del DataFrame y llamar al procedimiento almacenado para insertar cada registro
    for index, row in df.iterrows():
        # Extraer los valores de cada fila
        codigo_producto = row['codigo_producto']
        nombre_producto = row['nombre_producto']
        cantidad = row['cantidad']
        fecha_compra = row['fecha_compra'].strftime('%Y-%m-%d') 
        numero_factura = row['numero_factura']
        
        # Ejecutar el procedimiento almacenado con los valores de la fila
        cursor.execute('EXEC InsertarProductoPrueba ?, ?, ?, ?, ?',
                       (codigo_producto, nombre_producto, cantidad, fecha_compra, numero_factura))
        
        # Confirmar la transacción para cada fila
        conn.commit()
        print(f"Producto {codigo_producto} insertado exitosamente")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    if conn:
        conn.close()
        print("Conexión cerrada")
