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



{
	'name': 'Congruencial Method',
	'category': '',
	'version': '11.0',
	'author': 'Brayhan Andres Jaramillo Castaño, Juan Camilo Zuluaga Serna' ,
	'license': 'LGPL-3',
	'maintainer': 'brayhanjaramillo@hotmail.com, juancamilozuluagaserna@hotmail.com',
	'website': '',
	'summary': '',
	'images': [],
	'description': """

	Módulo que permite generar números aleatorios a través del método Congruencial Multiplicativo, además de esto realiza dos tipos de pruebas para estos números generados los cuales son:

	-	Prueba del Punto Medio
	-	Prueba de Kolmogórov-Smirnov


	""",
	'depends': [

	],
	'data': [
		'views/congruencial_method_view.xml',
		'views/menu.xml',

	],


	'installable': True,
	'application': True,
	'auto_install': False,


}


