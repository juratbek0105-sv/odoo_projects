from odoo import models, fields


class Book(models.Model):
    _name = "ecommercy.book"
    _description = "Book"

    name = fields.Char()
    description = fields.Text()
    author_ids = fields.Many2one("commercy.author")



class Author(models.Model):
    _name = "ecommercy.author"
    _description = "Author"

    name = fields.Char()
    book_ids = fields.One2many("ecommercy.book")


class Student(models.Model):
    _name = "ecommercy.student"
    _description = "Student"

    name = fields.Char()
    book_ids = fields.Many2many