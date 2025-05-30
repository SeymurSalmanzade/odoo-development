# -*- coding: utf-8 -*-

from odoo import models, fields, api


class mb_sellers(models.Model):
    _name="mb_sellers"
    _description="mb_sellers"

    name = fields.Char('Name', copy=False, required=True)
    seller_birth = fields.Date('Birth')
    seller_company = fields.Many2one('mb_companies')
    seller_mobile = fields.Char('Mobile', copy=False, required=True)
    seller_email = fields.Char('Email', copy=False)
    seller_image = fields.Image('Image')


class mb_companies(models.Model):
    _name="mb_companies"
    _description="mb_companies"

    name = fields.Char('Company Name', required=True)
    company_logo = fields.Binary('Company Logo')
    street = fields.Char()
    city = fields.Char()
    state_id = fields.Char()
    zip = fields.Char()
    country_id = fields.Char()
    company_vat = fields.Char('Tax ID')
    company_registry_id = fields.Char('Company ID')
    company_phone = fields.Char('Phone')
    company_mobile = fields.Char('Mobile')
    company_email = fields.Char('Email')
    company_website = fields.Char('Website')
    company_color = fields.Char('Color')
    company_members_id = fields.One2many('mb_sellers','seller_company')
    

    
class book_store(models.Model):
    _name = 'book_store.book_store'
    _description = 'This is the list of books'


    # genres = fields.Many2many("genre_list","book_genre_relation","book_store","genre_list",
    #                          required=True, help='Select at least one genre')
    
    genres = fields.Selection("_get_genre_list", required=True)
    def _get_genre_list(self):
        return [('mystery','Mystery'),
                ('fantasy','Fantasy'),
                ('thriller','Thriller'),
                ('horror','Horror'),
                ('romance','Romance'),
                ('science','Science'),
                ('historical','Historical'),
                ('memoir','Memoir')]

    name = fields.Char(copy=False, translate=True)
    seller_reference_id = fields.Reference([('mb_companies','Company'),
                               ('mb_sellers','Person')
                              ])
    seller_person = fields.Many2one('mb_sellers')
    mobile = fields.Char(related='seller_person.seller_mobile')
    seller_company = fields.Many2one('mb_companies')
    email = fields.Char(related='seller_company.company_email', readonly=False)
    is_new_book = fields.Boolean("New?", default=False, copy=False, required=True)
    author = fields.Char(copy=False, size=30)
    create_date = fields.Date("Created on", copy=False, default=fields.Date.today)
    release_date = fields.Date(copy=False)
    price = fields.Monetary(string="Price", copy=False)
    discount_price = fields.Monetary('Discount')
    final_price = fields.Monetary("Final Price", compute='_compute_final_price_cal', copy=False, store=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.ref('base.AZN'), store=True, copy=False)
    
    @api.depends('price','discount_price')
    def _compute_final_price_cal(self):
        for record in self:
            record.final_price = record.price - record.discount_price

    book_images = fields.Many2many('ir.attachment', string='Images', help='Upload at least 1 image of the book to see its quality')     
    description = fields.Text(copy=False, translate=True, help='Write some words for selling if you want')
    description_compute = fields.Text()
    
    @api.onchange("description")
    def onchange_description_field(self):
        for record in self:
            record.description_compute = record.description


class res_currency(models.Model):
    _inherit = 'res.currency'

    book_lists_id = fields.One2many('book_store.book_store','currency_id')
    # movie_lists_id = fields.One2many('movie_list','currency_id')

class movie_list(models.Model):
    _name = 'movie_list'
    _description = 'This is the list of movies'

    categories = fields.Many2many("category_list","movie_categorie_relation","movie_list","category_list",
                                    help='Select at least one category')

    # category = fields.Selection("_get_category_list")
    # def _get_category_list(self):
    #     return [('mystery','Mystery'),
    #             ('fantasy','Fantasy'),
    #             ('crime','Crime'),
    #             ('thriller','Thriller'),
    #             ('horror','Horror'),
    #             ('romance','Romance'),
    #             ('science','Science'),
    #             ('blu-ray','Blu-Ray'),
    #             ('western','Western'),
    #             ('historical','Historical'),
    #             ('documentary','Documentary'),
    #             ('memoir','Memoir')]

    name = fields.Char(copy=False, translate=True)
    is_new_movie = fields.Selection([('yes','Yes'),('no','No')],"New?", required=True)
    author = fields.Char(copy=False, size=15)
    release_date = fields.Date("Release Date", copy=False, default=fields.Date.today)
    premiere_night = fields.Datetime(copy=False, default=fields.Datetime.now)
    price = fields.Monetary(string="Price", currency_field='my_currency_id', copy=False)
    my_currency_id = fields.Many2one('res.currency', string="Currency", default=lambda self: self.env.ref('base.AZN'), store=True, copy=False)
    description = fields.Html(copy=False, help='Write some words for selling if you want')
    movie_image = fields.Image()
    movie_trailer = fields.Binary(string='Upload Trailer')
    trailer_file_name = fields.Char()
    quality = fields.Selection([
        ('0','None'),
        ('1','Very Low'),
        ('2','Low'),
        ('3','Normal'),
        ('4','High'),
        ('5','Very High')], required=True)

    def print_movie_report(self):
        return self.env.ref("book_store.movie_store_report_temp").report_action(self)


class genre_list(models.Model):
    _name = 'genre_list'
    _description = 'This is the genre list'

    name = fields.Char()
    color = fields.Integer()
class category_list(models.Model):
    _name = 'category_list'
    _description = 'This is the category list'

    name = fields.Char()
    color = fields.Integer()