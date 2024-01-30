# -*- coding: utf-8 -*-
# from odoo import http


# class Flights(http.Controller):
#     @http.route('/flights/flights', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/flights/flights/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('flights.listing', {
#             'root': '/flights/flights',
#             'objects': http.request.env['flights.flights'].search([]),
#         })

#     @http.route('/flights/flights/objects/<model("flights.flights"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('flights.object', {
#             'object': obj
#         })
