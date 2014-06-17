# coding=utf-8
from AccessControl import ClassSecurityInfo
from zope.interface import implements
from Products.Archetypes.atapi import *
from Products.Archetypes.public import *

from Products.ATContentTypes.content.base import ATCTContent, ATContentTypeSchema
from Products.ATContentTypes.content import schemata

from vindula.reservacorporativa import MessageFactory as _
from vindula.reservacorporativa.config import *
from vindula.reservacorporativa.content.interfaces import IVindulaReserve



VindulaReserve_schema = ATContentTypeSchema + Schema((

    BooleanField(
        name='activ_portletLeft',
        default=False,
        widget=BooleanWidget(
            label=_(u'Portlet Esquerda'),
            description=_(u'Se selecionado, ativa a visualização dos portet na coluna da esquerda.'),
        ),
        required=False,
    ),

    BooleanField(
        name='activ_portletRight',
        default=False,
        widget=BooleanWidget(
            label=_(u'Portlet Direita'),
            description=_(u'Se selecionado, ativa a visualização dos portet na coluna da direita.'),
        ),
        required=False,
    ),
    

))

schemata.finalizeATCTSchema(VindulaReserve_schema, folderish=False)

class VindulaReserve(ATCTContent):
    """ Reserve Content for Events, Colection, Reserve Corp"""
    
    implements(IVindulaReserve)    
    portal_type = 'VindulaReserve'
    _at_rename_after_creation = True
    schema = VindulaReserve_schema

registerType(VindulaReserve, PROJECTNAME) 

            