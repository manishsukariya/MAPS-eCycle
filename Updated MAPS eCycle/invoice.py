from fpdf import FPDF
import os

class InvoicePDF:
    def __init__(self, app):
        self.app = app

    def generate_invoice(self, order_id):
        self.app.db.cursor.nextset()
        self.app.db.cursor.execute("""
            SELECT b.name 
            FROM orders d 
            JOIN buyer b ON d.buyer_id = b.buyer_id 
            WHERE d.order_id = %s
        """, (order_id,))
        buyer = self.app.db.cursor.fetchone()

        if not buyer:
            print("No buyer found for this order.")
            return None

        buyer_name = buyer[0]

        self.app.db.cursor.nextset()
        self.app.db.cursor.execute("""
            SELECT i.name, oi.quantity, oi.price_per_unit 
            FROM order_item oi
            JOIN inventory i ON oi.inventory_id = i.inventory_id
            WHERE oi.order_id = %s
        """, (order_id,))
        items = self.app.db.cursor.fetchall()

        if not items:
            print("No items found for this order.")
            return None

        # Create invoice PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Add logo if exists
        logo_path = "images/logo1.png"
        if os.path.exists(logo_path):
            pdf.image(logo_path, x=10, y=8, w=33)
        pdf.ln(40)

        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, f"INVOICE", ln=True, align='C')
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, f"Order ID: {order_id}", ln=True, align='L')
        pdf.cell(200, 10, f"Buyer Name: {buyer_name}", ln=True, align='L')
        pdf.ln(10)

        # Table Header
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(60, 10, "Item", border=1)
        pdf.cell(30, 10, "Quantity", border=1)
        pdf.cell(40, 10, "Price/Unit", border=1)
        pdf.cell(40, 10, "Total", border=1, ln=True)

        # Table Rows
        pdf.set_font("Arial", size=12)
        grand_total = 0
        for name, qty, price in items:
            total = qty * price
            grand_total += total
            pdf.cell(60, 10, name, border=1)
            pdf.cell(30, 10, str(qty), border=1)
            pdf.cell(40, 10, f"Rs. {price}", border=1)
            pdf.cell(40, 10, f"Rs. {total}", border=1, ln=True)

        # Grand Total
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(130, 10, "Grand Total", border=1)
        pdf.cell(40, 10, f"Rs. {grand_total}", border=1, ln=True)

        # Save the PDF
        filename = f"invoice_{order_id}.pdf"
        file_path = os.path.join("invoices", filename)
        os.makedirs("invoices", exist_ok=True)
        pdf.output(file_path)

        return file_path
