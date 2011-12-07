# -*- coding: utf-8 -*-
from five import grok
from zope import schema
from plone.directives import form
from vindula.reservacorporativa import MessageFactory as _

# Interface and schema

class IReserve(form.Schema):
    """ Reserve Folder for Events """
    
    monday = schema.Bool(
        title=_(u"Segunda"),
        )
    
    tuesday = schema.Bool(
        title=_(u"Terça"),
        default=False
        )
    
    wednesday = schema.Bool(
        title=_(u"Quarta"),
        default=False
        )

    thursday = schema.Bool(
        title=_(u"Quinta"),
        default=False
        )
    
    friday = schema.Bool(
        title=_(u"Sexta"),
        default=False
        )
    
    saturday = schema.Bool(
        title=_(u"Sábado"),
        default=False
        )
     
    sunday = schema.Bool(
        title=_(u"Domingo"),
        default=False
        )
    
    monday_time_start = schema.Time(
        title=_(u"Hora que começa"),
        required=False,
        )
    
    monday_time_end = schema.Time(
        title=_(u"Hora que termina"),
        required=False,
        )
 
    
# View
    
class ReserveView(grok.View):
    grok.context(IReserve)
    grok.require('zope2.View')
    grok.name('view')
  
    def getEvents(self):
        return 'Reserve View'