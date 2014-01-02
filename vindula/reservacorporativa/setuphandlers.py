# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName


def installReservaCorporativa(context):
	portal = context.getSite()

	#ADIÇÃO DOS INTEX DE CATALOG
	catalog = getToolByName(portal, 'portal_catalog')
	indexes = catalog.indexes()

	# Specify the indexes you want, with ('index_name', 'index_type')
	wanted = (('getRecurrent', 'FieldIndex'),
			)

	indexables = []
	for name, meta_type in wanted:
		if name not in indexes:
			catalog.addIndex(name, meta_type)
			indexables.append(name)

	if len(indexables) > 0:
		catalog.manage_reindexIndex(ids=indexables)