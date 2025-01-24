
"""
2. Creación de base de datos: (Puntaje 30%)
"""

import pyodbc

# Configurar la conexión a SQL Server
server = 'LAPTOP-DE-ALAN' # Cambiar
db = 'prueba' # Cambiar 
cone = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={db};Trusted_Connection=yes'

# Conectar a la base de datos
try:
    # Conectar a SQL Server
    conn = pyodbc.connect(cone)
    cursor = conn.cursor()
    print("Conexión exitosa a SQL Server")

    # Crear la tabla productos_prueba
    create_table_query = '''
    CREATE TABLE productos_prueba (
        id INT IDENTITY(1,1) PRIMARY KEY,      
        codigo_producto NVARCHAR(20) NOT NULL,
        nombre_producto NVARCHAR(100) NOT NULL, 
        cantidad INT NOT NULL,               
        fecha_compra DATE NOT NULL,          
        numero_factura NVARCHAR(50) NOT NULL  
    );
    '''
    cursor.execute(create_table_query)
    print("Tabla 'productos_prueba' creada exitosamente")
    
    # Crear el procedimiento almacenado para insertar datos
    create_procedure_query = '''
    CREATE PROCEDURE InsertarProductoPrueba
        @codigo_producto NVARCHAR(20),
        @nombre_producto NVARCHAR(100),
        @cantidad INT,
        @fecha_compra DATE,
        @numero_factura NVARCHAR(50)
    AS
    BEGIN
        INSERT INTO productos_prueba (codigo_producto, nombre_producto, cantidad, fecha_compra, numero_factura)
        VALUES (@codigo_producto, @nombre_producto, @cantidad, @fecha_compra, @numero_factura);
    END;
    '''
    cursor.execute(create_procedure_query)
    print("Procedimiento almacenado 'InsertarProductoPrueba' creado exitosamente")

    # Confirmar cambios en la base de datos
    conn.commit()
    print("Cambios guardados exitosamente")

except Exception as e:
    print(f"Error: {e}")
finally:
    # Cerrar la conexión
    if conn:
        conn.close()
        print("Conexión cerrada")