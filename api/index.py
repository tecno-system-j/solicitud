from flask import Flask, render_template, request, send_file, jsonify
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Table, TableStyle
from datetime import datetime
import os

app = Flask(__name__)

class FormularioProveedorPDF:
    def __init__(self):
        self.width, self.height = landscape(letter)  # Usando orientación horizontal
        
    def generar_pdf(self, datos, nombre_archivo="formato_proveedor.pdf"):
        c = canvas.Canvas(nombre_archivo, pagesize=landscape(letter))
        
        # Colores
        gris_claro = colors.Color(0.9, 0.9, 0.9)
        
        # Título principal con fondo gris
        c.setFillColor(gris_claro)
        c.rect(0, self.height - 40, self.width, 40, fill=True)
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(self.width/2, self.height - 25, "SOLICITUD REQUERIMIENTO DE MATERIA PRIMA")
        
        # Marco para fecha y tipo
        c.setStrokeColor(colors.black)
        # Fecha
        c.rect(30, self.height - 80, 100, 25)  # Marco para "FECHA:"
        c.rect(130, self.height - 80, 400, 25)  # Marco para el valor de la fecha
        
        # Tipo (JOSH/SIMEON)
        c.rect(530, self.height - 80, 100, 25)  # Marco para JOSH
        c.rect(530, self.height - 105, 100, 25)  # Marco para SIMEON
        
        # Textos de los encabezados
        c.setFont("Helvetica-Bold", 10)
        c.drawString(35, self.height - 70, "FECHA:")
        c.drawString(535, self.height - 70, "JOSH")
        c.drawString(535, self.height - 95, "SIMEON")
        
        # Marca de selección para JOSH/SIMEON
        if datos.get('tipo', '').lower() == 'josh':
            c.rect(610, self.height - 75, 15, 15, fill=True)
        else:
            c.rect(610, self.height - 100, 15, 15, fill=True)
            
        # Información del proveedor
        c.rect(30, self.height - 130, 150, 25)  # Marco para "NOMBRE PROVEEDOR:"
        c.rect(180, self.height - 130, 350, 25)  # Marco para el valor del nombre
        c.rect(530, self.height - 130, 50, 25)  # Marco para "NIT:"
        c.rect(580, self.height - 130, 150, 25)  # Marco para el valor del NIT
        
        c.setFont("Helvetica-Bold", 10)
        c.drawString(35, self.height - 120, "NOMBRE PROVEEDOR:")
        c.drawString(535, self.height - 120, "NIT:")
        
        # Valores de los campos
        c.setFont("Helvetica", 10)
        c.drawString(135, self.height - 70, datos.get('fecha', ''))
        c.drawString(185, self.height - 120, datos.get('nombre_proveedor', ''))
        c.drawString(585, self.height - 120, datos.get('nit', ''))
        
        # Tabla de items
        headers = [['DESCRIPCION', 'CANTIDAD', 'UNIDAD DE MEDIDA']]
        data = [[item.get('descripcion', ''), 
                str(item.get('cantidad', '')), 
                item.get('unidad', '')] for item in datos.get('items', [])]
        
        # Añadir filas vacías hasta completar 15 filas
        while len(data) < 15:
            data.append(['', '', ''])
            
        table_data = headers + data
        col_widths = [400, 100, 150]
        
        table = Table(table_data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), gris_claro),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (2, -1), 'CENTER'),
        ]))
        
        # Dibujar la tabla
        table.wrapOn(c, 30, 30)
        table.drawOn(c, 30, self.height - 450)
        
        # Firma
        c.setFont("Helvetica-Bold", 10)
        c.drawString(30, 50, "FIRMA PROVEEDOR:")
        c.line(150, 50, 400, 50)
        c.setFont("Helvetica", 10)
        c.drawString(150, 60, datos.get('firma', ''))
        
        c.save()
        return nombre_archivo

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generar-pdf', methods=['POST'])
def generar_pdf():
    try:
        datos = request.get_json()
        generador = FormularioProveedorPDF()
        nombre_archivo = f"solicitud_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        ruta_archivo = os.path.join('temp', nombre_archivo)
        os.makedirs('temp', exist_ok=True)
        generador.generar_pdf(datos, ruta_archivo)
        return send_file(ruta_archivo, as_attachment=True, download_name=nombre_archivo)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
