"""
1. Análisis y procesamiento de datos: (Puntaje 30%)
"""

import pdfplumber
import pandas as pd

# Lista para almacenar los datos extraídos
data = []

# Extraer los datos de un archivo PDF
def extract_pdf_data(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        # Leer cada página del PDF
        for page in pdf.pages:
            # Extraer el texto de la página
            text = page.extract_text()

            # Buscar los datos de la factura y los productos
            lines = text.splitlines()

            # Extracción del número de factura y fecha de compra
            numero_factura = lines[0].split(' ')[1]
            fecha_compra = lines[1].split(' ')[1]
            
            # Extraer los productos y su cantidad
            productos = []
            for line in lines[3:]:
                columns = line.split()
                if len(columns) >= 3:
                    codigo_producto = columns[0]
                    nombre_producto = " ".join(columns[1:-1])
                    cantidad = columns[-1]
                    productos.append([numero_factura, fecha_compra, codigo_producto, nombre_producto, cantidad])

            # Añadir los productos a la lista de datos
            data.extend(productos)

# Extraer datos de los dos PDFs
extract_pdf_data('docs/FAC001.pdf')
extract_pdf_data('docs/FAC002.pdf')

# Crear un DataFrame con los datos extraídos
df_pdfs = pd.DataFrame(data, columns=["numero_factura", "fecha_compra", "codigo_producto", "nombre_producto", "cantidad"])

# Archivos de Excel
excel_path = 'docs/BASE_DATOS_FACTURAS.xlsx'
output_path = 'docs/BASE_DATOS_ACTUALIZADA.xlsx'
df_base = pd.read_excel(excel_path)

# Unir el DataFrame extraído de los PDFs con el DataFrame base
df_base = df_base.merge(df_pdfs[['codigo_producto', 'fecha_compra', 'numero_factura']], on='codigo_producto', how='left')

# Reemplazar los valores NaN en 'fecha_compra_x' y 'numero_factura_x' con los valores de 'fecha_compra_y' y 'numero_factura_y'
df_base['fecha_compra'] = df_base['fecha_compra_x'].fillna(df_base['fecha_compra_y'])
df_base['numero_factura'] = df_base['numero_factura_x'].fillna(df_base['numero_factura_y'])

# Eliminar las columnas duplicadas
df_base = df_base.drop(columns=['fecha_compra_x', 'numero_factura_x', 'fecha_compra_y', 'numero_factura_y'])

# Guardar los cambios en el archivo Excel
df_base.to_excel(output_path, index=False)
print("Base de datos actualizada correctamente.")

