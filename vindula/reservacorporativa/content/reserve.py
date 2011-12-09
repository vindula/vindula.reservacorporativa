# -*- coding: utf-8 -*-
from five import grok
from zope import schema
from plone.directives import form
from vindula.reservacorporativa import MessageFactory as _


# Interface and schema

class IReserve(form.Schema):
    """ Reserve Folder for Events """

    
    frequency = schema.Choice(
        title=_(u"Frequência"),
        description=_(u"Informe a frequencia com que os eventos ocorrem."),
        values=['semanal', 'quinzenal', 'mensal'],  
        default=_(u"semanal"),
        )
    
    duration = schema.Time(
        title=_(u"Duração"),
        description=_(u"Informe a duração dos eventos. Ex.: 01:00 (uma hora)."),
        )
    
    local = schema.TextLine(
        title=_(u"Local"),
        description=_(u"Informe o local onde os eventos deverão ocorrer."),
        required=False,
        )
    
    contact = schema.TextLine(
        title=_(u"Contato"),
        description=_(u"Dados de contato para dúvidas e informações, nome, e-mail ou telefone."),
        required=False,
        )
    
    
    # Monday
    monday = schema.Bool(
        title=_(u"Segunda"),
        description=_(u"Selecione a opção caso haja reservas disponíveis nas segundas e indique os horários de início e término."),
        )
    
    mon_start = schema.Time(
        title=_(u"Hora que começa"),
        required=False,
        )
    
    mon_end = schema.Time(
        title=_(u"Hora que termina"),
        required=False,
        )
    
    
    # Tuesday
    tuesday = schema.Bool(
        title=_(u"Terça"),
        description=_(u"Selecione a opção caso haja reservas disponíveis nas terças e indique os horários de início e término."),
        default=False
        )
    
    tue_start = schema.Time(
        title=_(u"Hora que começa"),
        required=False,
        )
    
    tue_end = schema.Time(
        title=_(u"Hora que termina"),
        required=False,
        )
    
    
    # Wednesday
    wednesday = schema.Bool(
        title=_(u"Quarta"),
        description=_(u"Selecione a opção caso haja reservas disponíveis nas quartas e indique os horários de início e término."),
        default=False
        )
    
    wed_start = schema.Time(
        title=_(u"Hora que começa"),
        required=False,
        )
    
    wed_end = schema.Time(
        title=_(u"Hora que termina"),
        required=False,
        )
    
    
    # Thursday
    thursday = schema.Bool(
        title=_(u"Quinta"),
        description=_(u"Selecione a opção caso haja reservas disponíveis nas quintas e indique os horários de início e término."),
        default=False
        )
    
    thu_start = schema.Time(
        title=_(u"Hora que começa"),
        required=False,
        )
    
    thu_end = schema.Time(
        title=_(u"Hora que termina"),
        required=False,
        )
    
    
    # Friday
    friday = schema.Bool(
        title=_(u"Sexta"),
        description=_(u"Selecione a opção caso haja reservas disponíveis nas sextas e indique os horários de início e término."),
        default=False
        )
    
    fri_start = schema.Time(
        title=_(u"Hora que começa"),
        required=False,
        )
    
    fri_end = schema.Time(
        title=_(u"Hora que termina"),
        required=False,
        )
    
    
    # Saturday
    saturday = schema.Bool(
        title=_(u"Sábado"),
        description=_(u"Selecione a opção caso haja reservas disponíveis nos sábados e indique os horários de início e término."),
        default=False
        )
    
    sat_start = schema.Time(
        title=_(u"Hora que começa"),
        required=False,
        )
    
    sat_end = schema.Time(
        title=_(u"Hora que termina"),
        required=False,
        )
    
    
    # Sunday
    sunday = schema.Bool(
        title=_(u"Domingo"),
        description=_(u"Selecione a opção caso haja reservas disponíveis nos domingos e indique os horários de início e término."),
        default=False
        )
    
    sun_start = schema.Time(
        title=_(u"Hora que começa"),
        required=False,
        )
    
    sun_end = schema.Time(
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