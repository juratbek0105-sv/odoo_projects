from odoo import models, fields, api

class KitchenDisplay(models.TransientModel):
    _name = "fast.food.kitchen.display"
    _description = "Kitchen Display Order Creation"

    order_type = fields.Selection([
        ("dine_in", "Dine In"),
        ("takeaway", "Takeaway")
    ], default="dine_in", string="Order Type", required=True)

    table_number = fields.Integer(string="Table Number")
    line_ids = fields.One2many("fast.food.kitchen.display.line", "display_id", string="Products")



    @api.onchange('order_type')
    def table_number_invisibility(self):
        for record in self:
            if record.order_type == "takeaway":
                record.table_number =False


    @api.model
    def default_get(self, fields_list):
        """Load all products into the display grid by default"""
        res = super().default_get(fields_list)
        products = self.env["fast.food.product"].search([])
        res["line_ids"] = [(0, 0, {"product_id": p.id, "quantity": 0}) for p in products]
        return res

    def action_confirm_order(self):
        """Create Order from selected products"""
        # filter lines with quantity > 0
        selected_lines = self.line_ids.filtered(lambda l: l.quantity > 0)
        if not selected_lines:
            return None

        order_vals = {
            "order_type": self.order_type,
            "table_number": self.table_number if self.order_type == "dine_in" else False,
        }
        order = self.env["fast.food.order"].create(order_vals)

        for line in selected_lines:
            self.env["fast.food.order.line"].create({
                "order_id": order.id,
                "product_id": line.product_id.id,
                "quantity": line.quantity,
                "price_unit": line.product_id.price,
            })

        order.action_confirm()

        # open order in form view
        return {
            "type": "ir.actions.act_window",
            "res_model": "fast.food.order",
            "res_id": order.id,
            "view_mode": "form",
            "target": "current",
        }



