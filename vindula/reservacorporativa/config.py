# -*- coding: utf-8 -*-
from Products.CMFCore.permissions import setDefaultRoles

PROJECTNAME = 'vindula.reservacorporativa'

# Permissions
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner'))
ADD_CONTENT_PERMISSIONS = {
    'ContentReserve': 'vindula.reservacorporativa: Add ContentReserve',
   
}

setDefaultRoles('vindula.reservacorporativa: Add ContentReserve', ('Manager','Owner'))


product_globals = globals()