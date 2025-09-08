from odoo import models, fields

class Product(models.Model):
    _name = "product.product"
    _description = "Product"

    name = fields.Char(required=True)
    price = fields.Float()
    quantity = fields.Integer()


    def _create_log(self, message):
        self.env["product.log"].create({
            "username": self.env.user.name,
            "message": message
        })

    def create(self, vals_list):
        records = super(Product, self).create(vals_list)
        for record in records:
            record._create_log(f"{record.name} nomli mahsulot qo'shildi")
        return records

    def write(self, vals):
        for record in self:
            old_name = record.name
            old_price = record.price
            old_quantity = record.quantity

            result = super(Product, self).write(vals)

            if "name" in vals:
                new_name = vals["name"]
                record._create_log(f"{old_name} mahsulot nomi {new_name}ga o'zgartirildi")

            if "price" in vals:
                new_price = vals["price"]
                if new_price > old_price:
                    condition = "oshirildi"
                else:
                    condition = "pasaytirildi"
                record._create_log(f"{old_name} nomli mahsulot narxi {new_price}ga {condition}")

            if "quantity" in vals:
                new_quantity = vals["quantity"]
                difference = old_quantity - new_quantity
                if difference > 0:
                    message = f"{old_name} nomli mahsulot soni {difference}ga kamaytirildi va natijada {new_quantity}ta bo'ldi"
                else:
                    message = f"{old_name} nomli mahsulot soni {abs(difference)}ga ko'paydi va natijada {new_quantity}ta bo'ldi"
                record._create_log(message)

        return result

    def unlink(self):
        for record in self:
            record._create_log(f"{record.name} nomli mahsulot o'chirildi")
        return super(Product, self).unlink()
