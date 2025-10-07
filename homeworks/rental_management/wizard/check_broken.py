from odoo import models, fields

class Check_Broken(models.TransientModel):
    _name = "rental.check.broken.wizard"
    _description = "Check Broken"

    rental_order_id = fields.Many2one("rental.order", required=True, string="Order")
    product_id = fields.Many2one("rental.product", required=True, string="Product")
    is_broken = fields.Boolean(string="Is it broken", default=False)

    def action_confirm_return(self):
        order = self.rental_order_id
        product = self.product_id

        product_vals = {
            "future_availability_date": False,
            "broken": self.is_broken,
        }

        product.write(product_vals)

        order.write({
            "returned_date": fields.Datetime.now(),
            "status": "returned",
        })

        return {"type": "ir.actions.act_window_close"}



