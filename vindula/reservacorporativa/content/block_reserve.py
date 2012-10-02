# coding=utf-8
from five import grok
from vindula.reservacorporativa import MessageFactory as _

from zope.app.component.hooks import getSite 
from zope.interface import Interface
from vindula.reservacorporativa.content.interfaces import IBlockReserve

from AccessControl import ClassSecurityInfo
from zope.interface import implements
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.document import ATDocumentSchema
from Products.ATContentTypes.content.document import ATDocumentBase
from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from vindula.reservacorporativa.config import *

from datetime import datetime, time
from DateTime import DateTime

BlockReserve_schema = ATDocumentSchema.copy() + Schema((
                                                        
#    StringField(
#        name='reserves',
#        widget=SelectionWidget(label=_(u"Reserva relacionada."),
#                               description=_(u"Selecione qual reserva corporativa vai ser bloqueada."),
#                               ),
#        required=True,
#        vocabulary='voc_reserves',
#    ),  
                                                          
    StringField(
            name='start_time',
            widget=StringWidget(
                label=_(u"Horário inicial"),
                description=_(u"Selecione o horário inicial que a reserva será bloqueada."),
            ),
        required=True,
    ),
    
    StringField(
            name='end_time',
            widget=StringWidget(
                label=_(u"Horário final"),
                description=_(u"Selecione até que horário a reserva será bloqueada."),
            ),
        required=True,
    ),  
    
    DateTimeField(
            name='when',
            default_method = 'getDefaultTime',
            widget=CalendarWidget(
                label=_(u"De quando"),
                description=_(u"Selecione o período inicial que esse bloqueio permanecerá ativo."),
                show_hm = 0,
                format = '%d/%m/%Y',
            ),
        required=False,
    ),
    
    DateTimeField(
            name='even_when',
            default_method = 'getDefaultTime',
            widget=CalendarWidget(
                label=_(u"Até quando"),
                description=_(u"Selecione até quando esse bloqueio permanecerá ativo."),
                show_hm = 0,
                format = '%d/%m/%Y',
            ),
        required=False,
    ),
    
    StringField(
        name='days_of_week',
        widget=InAndOutWidget(label=_(u"Dias da semana."),
                               description=_(u"Selecione os dias da semana que o bloqueio deve ser aplicado."),
                               ),
        required=False,
        vocabulary=DisplayList((('segunda', 'Segunda-Feira'), ('terça', 'Terça-Feira'), ('quarta', 'Quarta-Feira'), ('quinta', 'Quinta-Feira'), ('sexta', 'Sexta-Feira'), ('sábado', 'Sábado'), ('domingo', 'Domingo'))),
    ),  
    
    StringField(
        name='frequency',
        widget=SelectionWidget(label=_(u"Frequência."),
                               description=_(u"Informe a frequência com que os bloqueios deverão ocorrer.<br>" +
                                              "<strong>Durante o período:</strong> O bloqueio será ativado em todos os dias que houver horários disponíveis, durante o período definido acima.<br>" +
                                              "<strong>Quinzenal:</strong> O bloqueio será ativado a cada <i>quinze dias</i> que houver horários disponíveis, durante o periodo definido acima.<br>" +
                                              "<strong>Mensal:</strong> O bloqueio será feito <i>uma vez por mês</i> nos dias que houver horários disponíveis, durante o periodo todo definido acima."),
                               ),
        required=True,
        vocabulary=DisplayList((('period', 'Durante o período'), ('quinzenal', 'Quinzenal'), ('mensal', 'Mensal'))),
        default=_(u"period"),
    ),  

))

invisivel = {'view':'invisible','edit':'invisible',}
BlockReserve_schema['description'].widget.visible = invisivel
BlockReserve_schema['text'].widget.visible = invisivel
# Dates
L = ['effectiveDate','expirationDate','creation_date','modification_date']   
# Categorization
L += ['subject','relatedItems','location','language']
# Ownership
L += ['creators','contributors','rights']
# Settings
L += ['excludeFromNav','presentation','tableContents']

for i in L:
    BlockReserve_schema[i].widget.visible = invisivel 

BlockReserve_schema['allowDiscussion'].default = False

finalizeATCTSchema(BlockReserve_schema, folderish=False)

class BlockReserve(ATDocumentBase):
    """ Reserve Content for Events, Colection, Reserve Corp"""
    security = ClassSecurityInfo()
    
    implements(IBlockReserve)    
    portal_type = 'BlockReserve'
    _at_rename_after_creation = True
    schema = BlockReserve_schema
    
    def voc_reserves(self):
        reserves = []
        items = self.aq_parent.objectValues()
        for item in items:
            if item.Type() == 'Reserva Corporativa':
                reserves.append((item.id, item.Title()))
        
        return DisplayList(reserves)
    
    def getDefaultTime(self):
        return DateTime()
        
registerType(BlockReserve, PROJECTNAME)