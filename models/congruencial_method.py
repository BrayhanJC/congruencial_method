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
import threading

class CongruencialMethod(models.Model):

	_name = 'congruencial.method'

	_description = "Congruencial Method"


	def load_interval():
		data = []

		for i in range(90, 100):
			data.append((i, str(i)))
		return data

	def load_interval_level_confidence():
		data = []
		data.append((0.001, 0.001))
		data.append((0.005, 0.005))
		data.append((0.01, 0.01))
		data.append((0.02, 0.02))
		data.append((0.025, 0.025))
		data.append((0.03, 0.03))
		data.append((0.04, 0.04))
		data.append((0.05, 0.05))
		data.append((0.10, 0.10))
		data.append((0.15, 0.15))
		data.append((0.20, 0.20))
		data.append((0.25, 0.25))
		data.append((0.30, 0.30))
		data.append((0.35, 0.35))
		data.append((0.04, 0.04))
		return data



	name = fields.Char(string=u'Nombres', default="Metodo Congruencial" )
	data_number = fields.Integer(string=u'Número de datos', required=True)
	module = fields.Integer(string=u'Modulo', required=True)
	seed = fields.Integer(string=u'Xo', required=True)
	multiplicity_constant = fields.Integer(string=u'Constante Multiplicativa', required=True)
	congruencial_method_data_ids = fields.One2many('congruencial.method_data', 'congruencial_method_id', String= "Resultado")
	confidence_interval = fields.Selection(load_interval(), String="Intervalo de Confianza")
	confidence_level = fields.Selection(load_interval_level_confidence(), String="Nivel de Confianza")
	range_half = fields.Char(String="Rango")
	chi_cuadrado_result = fields.Char(String="Rango")
	show_message_period = fields.Char(string = 'Period')
	test_method = fields.Selection([('chi', "Prueba de Ji Cuadrado"), ('half', "Prueba de la Media")], String="Prueba")

	@api.depends('data_number', 'module', 'seed', 'multiplicity_constant')
	def calculate_numbers(self):

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

	
	def load_random_numbers(self):

			t = threading.Thread(target=self.calculate_numbers())
			t.start()
			t = threading.Thread(target=self.calculate_period())
			t.start()
			



	@api.depends('data_number', 'module', 'seed', 'multiplicity_constant')
	def calculate_period(self):
		"""
			Calcula los números aleatorios por el metodo congruencial multiplicativo
		"""
		_logger.info("entra")
		if self.data_number and self.module and self.seed and self.multiplicity_constant:

			data = []
			iterator = 1
			m = float(self.module)
			Xo= float(self.seed)
			a = float(self.multiplicity_constant)

			for x in range(1, int(10**10)):


				load_Xo = ((Xo * a)/m)
				new_Xo = (abs(load_Xo) - abs(int(load_Xo))) * m

				rn = m - 1
				random_number = (new_Xo / rn)

				Xo= new_Xo

				if new_Xo in data:
					self.show_message_period = u"El periodo es de " + str(iterator) 
					break

				data.append(Xo)
				iterator += 1
				



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


			self.range_half =   "El rango de esta prueba esta en "  + '[ ' + str(result_negative) + ', ' + str(result_positive) + ' ]' + " .Por lo cual indica que " + option + " tiene uniformidad en los datos."
		



	@api.onchange('confidence_level')
	def calculate_ji_cuadrado(self):

		"""
			Funcion que calcula la prueba de la media 
		"""

		if self.confidence_level:

			interval = self.confidence_interval

			gdl = float((self.data_number / 5) - 1)

			fe = float((self.data_number / 5))

			data = self.load_numbers()

			d_calculate = self.calculate_observed_frequency(data, fe)

			d_teorico = self.calculate_d_teorico(self.confidence_level)

			option = 'no'

			if d_calculate <= d_teorico:

				option = 'si'

			self.chi_cuadrado_result = u"Los números generados " + option + " tiene uniformidad en los datos. Con un D Teorico de: "+str(d_teorico)+", y un D Calculado de "+str(d_calculate)



	def calculate_observed_frequency(self, data, fe):

		values = [0.0, 0.0, 0.0, 0.0, 0.0]
		result = 0.0 
		# traverse in the list1 
		for x in data: 
			# condition check 
			if x > 0.0 and x <= 0.2: 
				values[0] += 1.0
			if x > 0.2 and x <= 0.4: 
				values[1] += 1.0
			if x > 0.4 and x <= 0.6: 
				values[2] += 1.0
			if x > 0.6 and x <= 0.8: 
				values[3] += 1.0
			if x > 0.8 and x <= 1.0: 
				values[4] += 1.0

		
		result = self.calculate_observed_frequency_sum(values, fe)	
		return result


	def calculate_observed_frequency_sum(self, values, fe):


		result = 0.0

		for x in values:
			
			result += (((x - fe) ** 2) / fe)	

		return result


	def calculate_d_teorico(self, confidence_level):


		d_teorico = 0.0

		if confidence_level == 0.001:

			d_teorico = 18.467

		elif confidence_level == 0.005:

			d_teorico = 14.860

		elif confidence_level == 0.01:

			d_teorico = 13.277

		elif confidence_level == 0.02:

			d_teorico = 11.668

		elif confidence_level == 0.025:

			d_teorico = 11.143

		elif confidence_level == 0.03:

			d_teorico = 10.712

		elif confidence_level == 0.04:

			d_teorico = 10.026

		elif confidence_level == 0.05:

			d_teorico = 9.488

		elif confidence_level == 0.10:

			d_teorico = 7.779

		elif confidence_level == 0.15:

			d_teorico = 6.745

		elif confidence_level == 0.2:

			d_teorico = 5.989

		elif confidence_level == 0.25:

			d_teorico = 5.385

		elif confidence_level == 0.3:

			d_teorico = 4.878

		elif confidence_level == 0.35:

			d_teorico = 4.438

		elif confidence_level == 0.4:

			d_teorico = 4.045


		return d_teorico	

CongruencialMethod()