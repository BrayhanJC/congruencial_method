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
from math import sqrt
import statistics as stats
import math

class CongruencialMethod(models.Model):

	_name = 'congruencial.method'

	_description = "Congruencial Method"


	def load_interval():
		data = []

		for i in range(90, 101):
			data.append((i, str(i)))
		return data


	name = fields.Char(string=u'Nombres', default="Metodo Congruencial" )
	data_number = fields.Integer(string=u'Número de datos', required=True)
	module = fields.Integer(string=u'Modulo', required=True)
	seed = fields.Integer(string=u'Xo', required=True)
	multiplicity_constant = fields.Integer(string=u'Constante Multiplicativa', required=True)
	congruencial_method_data_ids = fields.One2many('congruencial.method_data', 'congruencial_method_id', String= "Resultado")
	confidence_interval = fields.Selection(load_interval(), String="Intervalo de Confianza")
	range_half = fields.Char(String="Rango")
	test_method = fields.Selection([('chi', "Prueba de Ji Cuadrado"), ('half', "Prueba de la Media")], String="Prueba")





	@api.depends('data_number', 'module', 'seed', 'multiplicity_constant')
	def load_random_numbers(self):
		"""
			Calcula los números aleatorios por el metodo congruencial multiplicativo
		"""
		if self.data_number and self.module and self.seed and self.multiplicity_constant:

			data = []
			m = float(self.module)
			Xo= float(self.seed)
			a = float(self.multiplicity_constant)

			for x in range(1, int(self.data_number)+1):


				load_Xo = ((Xo * a)/m)
				new_Xo = (abs(load_Xo) - abs(int(load_Xo))) * m

				rn = m - 1
				random_number = (new_Xo / rn)

				Xo= new_Xo

				vals = {

				'data_number': x,
				'new_seed': new_Xo,
				'random_number': random_number
				}

				data.append((0,_, vals))
			self.congruencial_method_data_ids = None
			self.congruencial_method_data_ids = data


	def load_numbers(self):
		"""
			Funcion que permite cargar los números aleatorios
		"""

		data = []

		if len(self.congruencial_method_data_ids) > 0:
			for x in self.congruencial_method_data_ids:
				data.append(x.random_number)

		return data

 
	def calculate_averege(self, data):
		"""
			Funcion que permite calcular la media de los datos
		"""
		return stats.mean(data)
 

	def calculate_standard_deviation(self, data):
		"""
			Funcion que permite calcular la varianza de los datos
		"""
		return stats.pstdev(data)


	@api.onchange('confidence_interval')
	def calculate_test_half(self):

		"""
			Funcion que calcula la prueba de la media 
		"""

		if self.confidence_interval:

			interval = float(self.confidence_interval)/100

			alpha = 1 - interval

			alpha_ = alpha/2

			alpha_half = 1 - alpha_



			data = self.load_numbers()

			average = self.calculate_averege(data)

			standard_deviation = self.calculate_standard_deviation(data)

			raiz = math.sqrt(len(data))

			z = 1

			if alpha_half == 0.95:
				z = 1.65

			if alpha_half == 0.955:
				z = 1.69

			if alpha_half == 0.96:
				z = 1.76

			if alpha_half == 0.965:
				z = 1.81

			if alpha_half == 0.97:
				z = 1.89

			if alpha_half == 0.975:
				z = 1.96

			if alpha_half == 0.98:
				z = 2.06

			if alpha_half == 0.985:
				z = 2.17

			if alpha_half == 0.99:
				z = 2.33

			if alpha_half == 0.995:
				z = 2.57

		
			result_positive = average + z*alpha_half*(standard_deviation/raiz)
			result_negative = average - z*alpha_half*(standard_deviation/raiz)

			option = ''

			if result_negative < 0.5 and result_positive > 0.5:
				option = 'Si'
			else:
				option = 'No'

			_logger.info('[ ' + str(result_negative) + ', ' + str(result_positive) + ' ]')

			self.range_half =   "El rango de esta prueba esta en "  + '[ ' + str(result_negative) + ', ' + str(result_positive) + ' ]' + " .Por lo cual indica que " + option + " tiene uniformidad en los datos."
		


CongruencialMethod()