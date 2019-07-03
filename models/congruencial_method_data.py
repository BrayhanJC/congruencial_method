# -*- coding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    Autor: Brayhan Andres Jaramillo Castaño
#    Correo: brayhanjaramillo@hotmail.com
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################

from odoo import api, fields, models, _
import time
from datetime import datetime, timedelta, date
import logging
_logger = logging.getLogger(__name__)
from odoo import modules
from odoo.addons import decimal_precision as dp

class CongruencialMethodData(models.Model):

	_name = 'congruencial.method_data'

	_description = "Congruencial Method Data"

	congruencial_method_id = fields.Many2one('congruencial.method', String="Metodo Congruencial")
	#numero de iteración
	data_number = fields.Integer(string=u'Número Iteración', required=True)
	#Operación con el módulo (Xo * a)Mod m
	#module = fields.Float(string=u'(Xo * a)Mod m', required=True)
	#Generación de la nueva semilla -> module*m
	new_seed = fields.Integer(string=u'Xo', required=True)
	#Número aleatorio
	random_number = fields.Float(string=u'Número Aleatorio', required=True, digits=(12,6))


CongruencialMethodData()