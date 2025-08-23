# -*- coding: utf-8 -*-
from odoo import models, fields

class EduProductSimple(models.Model):
    _name = "edu.product.simple"
    _description = "Educational Product (Only Char, Text, Integer, Float)"

    # --- Char fields ---
    name = fields.Char(required=True)                 # Mahsulot nomi
    sku = fields.Char(string="SKU")                   # Mahsulot kodi
    barcode = fields.Char(string="Barcode")           # Shtrix-kod
    brand = fields.Char(string="Brand")               # Brendi
    category = fields.Char(string="Category")         # Toifasi
    color = fields.Char(string="Color")               # Rangi

    # --- Text fields ---
    description = fields.Text(string="Description")   # Tavsif
    notes = fields.Text(string="Internal Notes")      # Ichki eslatmalar

    # --- Integer fields ---
    qty_on_hand = fields.Integer(string="Qty On Hand", default=0)      # Ombordagi miqdor
    min_qty = fields.Integer(string="Min Qty", default=0)              # Minimal miqdor
    max_qty = fields.Integer(string="Max Qty", default=0)              # Maksimal miqdor
    reorder_step = fields.Integer(string="Reorder Step", default=1)    # Qayta buyurtma qadam
    sold_month = fields.Integer(string="Sold This Month", default=0)   # Ushbu oyda sotilgan miqdor

    # --- Float fields ---
    list_price = fields.Float(string="List Price", default=0.0)        # Sotuv narxi
    cost = fields.Float(string="Cost", default=0.0)                    # Tannarx
    discount_percent = fields.Float(string="Discount %", default=0.0)  # Chegirma foizi (%)
    weight = fields.Float(string="Weight (kg)", default=0.0)           # Og'irligi (kg)
    volume = fields.Float(string="Volume (m3)", default=0.0)           # Hajmi (m3)
    rating = fields.Float(string="Rating", default=0.0)                # Reyting
    tax_rate = fields.Float(string="Tax Rate %", default=0.0)          # Soliq stavkasi (%)
    length_cm = fields.Float(string="Length (cm)", default=0.0)        # Uzunligi (sm)
    width_cm  = fields.Float(string="Width (cm)", default=0.0)         # Kengligi (sm)
    height_cm = fields.Float(string="Height (cm)", default=0.0)        # Balandligi (sm)

    def test_method(self):
        self.env["edu.product.simple"].search([("category", "=", "Electronics")])  #1
        self.env["edu.product.simple"].search([("brand", "=", "Apple"), ("list_price", ">", 500)] )  # 2
        self.env["edu.product.simple"].search(["|",("brand", "=", "Samsung"), ("brand", "=", "Xiaomi")])  # 3
        self.env["edu.product.simple"].search([("last_price", "<", 300) , "|",("brand", "=", "Sony"), ("brand", ">", "LG")])  # 4
        self.env["edu.product.simple"].search([("name", "ilike", "pro")])  #5
        self.env["edu.product.simple"].search([("sku", "=like", "ABC%")])  #6
        self.env["edu.product.simple"].search([("barcode", "=like", "%789")])  #7
        self.env["edu.product.simple"].search([("description", "ilike", "waterproof")])  #8
        self.env["edu.product.simple"].search([("qty_on_hand", ">=", 10), ("qty_on_hand", "<=", 100)] )  # 9
        self.env["edu.product.simple"].search([("weight", ">=", 0.5), ("weight", "<=", 2)] )  # 10
        self.env["edu.product.simple"].search([], limit=5, order="list_price desc")  #11
        self.env["edu.product.simple"].search([], offset=5, limit=5, order="list_price desc")  #12
        self.env["edu.product.simple"].search([("sku", "!=", False)])  #13
        self.env["edu.product.simple"].search([("barcode", "=", False)])  #14
        self.env["edu.product.simple"].search([("discount_percent", ">=", 10), ("list_price", ">", 0)])  # 15
        self.env["edu.product.simple"].search([("sold_month", ">=", 50)])  #16
        self.env["edu.product.simple"].search(["|",("qty_on_hand", "<=", "min_qty"), ("qty_on_hand", "+", "reorder_step", "<=", "min_qty")])  # 17
        self.env["edu.product.simple"].search([("volume", ">", 0)], order="weight asc, volume desc" )  # 18
        self.env["edu.product.simple"].search([("rating", ">=", 4.5), ("list_price", ">=", 1000)] )  # 19
        self.env["edu.product.simple"].search(["|", ("category", "ilike", "phone"), ("category", "ilike", "tablet")])  #20
        self.env["edu.product.simple"].search(["|", ("length_cm", ">=", 10), ("width_cm", ">=", 5), ("height_cm", ">=", 2)])  #21
        self.env["edu.product.simple"].search([("tax_rate", "=", "12"), ("tax_rate", ">", 15)] )  # 22
        self.env["edu.product.simple"].search([("brand", "=like", "S%"), ("color", "=like", "%red")] )  # 23
        self.env["edu.product.simple"].search([("list_price", ">=", 1000), ("discount_percent", ">=", 20)] )  # 24
        self.env["edu.product.simple"].search([("notes", "ilike", "fragile")])  #25
        self.env["edu.product.simple"].search([("brand", "in", ["Apple", "Samsung", "Xiaomi"]), ("category", "ilike", "phone")] )  # 26
        self.env["edu.product.simple"].search([("qty_on_hand", ">=", 100), ("sold_month", "<=", 5)] )  # 27
        self.env["edu.product.simple"].search(["|",("list_price", "=", 0), ("cost", "=", 0)])  # 28
        self.env["edu.product.simple"].search(["|",("discount_percent", "<", 0), ("discount_percent", ">", 100)])  # 29
        self.env["edu.product.simple"].search([], order="brand asc, list_price desc")



















