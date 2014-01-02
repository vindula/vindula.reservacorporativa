# -*- coding: utf-8 -*-
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from vindula.reservacorporativa import MessageFactory as _
from Products.Archetypes.atapi import *

from Products.ATContentTypes.content.event import ATEvent
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from vindula.reservacorporativa.config import *

from vindula.reservacorporativa.content.interfaces import IContentReserve, IEventReserve

event_reserve_schema = ATEvent.schema.copy() + Schema((


    BooleanField(
        name='recurrent',
        widget=BooleanWidget(
            label=_(u"Ativar evento recorrente"),
            description=_(u"Selecione para marcar este evento como recorrente"),
            label_msgid='vindula_themedefault_label_recurrent',
            description_msgid='vindula_themedefault_help_recurrent',
            i18n_domain='vindula_themedefault',
        ),
        default=False         
    ),
    
    StringField(
        name='frequency',
        widget=SelectionWidget(
            label=_(u"Frequência"),
            description=_(u"Informe a frequência com que os eventos ocorrem."),
            label_msgid='vindula_tile_label_frequency',
            description_msgid='vindula_tile_help_frequency',
            i18n_domain='vindula_themedefault',
            format='select',
        ),
        vocabulary=[("unico",_(u"Evento sem repedição")),
                    ("semanal", _(u"Evento Semanal")),
                    ("quinzenal", _(u"Evento Quinzenal")),
                    ("mensal", _(u"Evento Mensal")),
                   ],
        default='unico',
        required=True,
    ),

    DateTimeField(
            name='end_dateRecurrent',
            widget=CalendarWidget(
                label=_(u"Data Final da repedição"),
                description=_(u"Selecione o período en que esse evento sera repetido\
                                ou deixe em branco para evento sem fim."),
                show_hm = 0,
                format = '%d/%m/%Y',
            ),
        required=False,
    ),
    


))


finalizeATCTSchema(event_reserve_schema, folderish=False)

class EventReserve(ATEvent):
    """ Event Content """
    
    implements(IEventReserve)    
    portal_type = 'EventReserve'
    _at_rename_after_creation = True
    schema = event_reserve_schema

registerType(EventReserve, PROJECTNAME) 
