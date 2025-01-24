from django.shortcuts import render
import pyodbc

def home(request):
    # Configuración de la conexión con SQL Server
    server = 'LAPTOP-DE-ALAN'
    database = 'prueba'
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'

    # Información para las imágenes
    imagenes_postimg = {
        "logo_header": "https://i.postimg.cc/4dtttLxJ/logo-header.png",
        "main_image": "https://i.postimg.cc/RZyxJNH7/main-image.png",
        "main_ico": "https://i.postimg.cc/MGdmHj45/servicios.png"
    }

    # Inicializar la lista de productos
    productos_data = []

    if request.GET.get('consultar', False):
        try:
            # Conectar a SQL Server
            conn = pyodbc.connect(connection_string)
            cursor = conn.cursor()

            # Ejecutar la consulta para obtener los productos
            cursor.execute("SELECT codigo_producto, nombre_producto, cantidad, fecha_compra, numero_factura FROM productos_prueba")
            productos = cursor.fetchall()

            # Convertir los resultados en un formato adecuado para pasar al template
            productos_data = [{
                "codigo_producto": producto[0],
                "nombre_producto": producto[1],
                "cantidad": producto[2],
                "fecha_compra": producto[3].strftime('%Y-%m-%d'),
                "numero_factura": producto[4]
            } for producto in productos]

        except Exception as e:
            print(f"Error: {e}")
        finally:
            if conn:
                conn.close()

    # Contexto para el template
    ctx = {
        "assets": imagenes_postimg,
        "productos": productos_data,
    }
    
    return render(request, 'home.html', ctx)
