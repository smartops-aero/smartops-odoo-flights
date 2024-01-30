# -*- coding: utf-8 -*-
# from odoo import http


# class FlightsPilotlog(http.Controller):
#     @http.route('/flights_pilotlog/flights_pilotlog', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/flights_pilotlog/flights_pilotlog/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('flights_pilotlog.listing', {
#             'root': '/flights_pilotlog/flights_pilotlog',
#             'objects': http.request.env['flights_pilotlog.flights_pilotlog'].search([]),
#         })

#     @http.route('/flights_pilotlog/flights_pilotlog/objects/<model("flights_pilotlog.flights_pilotlog"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('flights_pilotlog.object', {
#             'object': obj
#         })
