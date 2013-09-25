# -*- coding: utf-8 -*-
from datetime import datetime
from five import grok
from zope import schema
from plone.directives import form
from Products.CMFCore.utils import getToolByName
from vindula.reservacorporativa import MessageFactory as _

from zope.lifecycleevent.interfaces import IObjectModifiedEvent, IObjectCreatedEvent


# Interface and schema

class IReserve(form.Schema):
    """ Reserve Folder for Events """

    
    frequency = schema.Choice(
        title=_(u"Frequência"),
        description=_(u"Informe a frequência com que os eventos ocorrem."),
        values=['semanal', 'quinzenal', 'mensal'],  
        default=_(u"semanal"),
        )

    local = schema.TextLine(
        title=_(u"Local"),
        description=_(u"Informe o local onde os eventos deverão ocorrer."),
        )
    
    duration = schema.Time(
        title=_(u"Duração"),
        description=_(u"Informe a duração dos eventos. Ex.: 01:00 (uma hora)."),
        )
    
    contact = schema.TextLine(
        title=_(u"Contato"),
        description=_(u"Insira o email do usuário que vai receber notificações das reservas efetuadas."),
        required=False,
        )
    
    mult_horarios = schema.Bool(
        title=_(u"Permitir mais de um horário"),
        description=_(u"Selecione se essa reserva irá permitir que o usuário selecione mais de um horário por reserva."),
        required=False,
        )

    recurrent = schema.Bool(
        title=_(u"Permitir agendamento recorrente"),
        description=_(u"Selecione se essa reserva irá permitir que o usuário um agendamento recorrente nessa reserva."),
        required=False,
        )
        
    replic_semana = schema.Bool(
        title=_(u"Replicar na semana"),
        description=_(u"Selecione esta opção caso haja reservas disponíveis para todos os dias da semana, informando nos campos abaixo os horários de inicio e término.\
                        Caso não deseje esta opção desconsidere os dois próximos campos abaixo."),

        required=False,
        )
    
    replic_start = schema.Time(
        title=_(u"Hora que começa (Replicar na semana)"),
        required=False,
        )
    
    replic_end = schema.Time(
        title=_(u"Hora que termina (Replicar na semana)"),
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
    
@grok.subscribe(IReserve, IObjectCreatedEvent)
def ReplicReserve(obj, event):
    
    if obj.replic_semana:
        start = obj.replic_start
        end = obj.replic_end
        
        week = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        week_start = ['mon_start','tue_start','wed_start','thu_start','fri_start','sat_start','sun_start']
        week_end = ['mon_end','tue_end','wed_end','thu_end','fri_end','sat_end','sun_end']
            
        
        for i in week:
            obj.__setattr__(i,True)
            
        for j in week_start:
            obj.__setattr__(j,start)
        
        for m in week_end:
            obj.__setattr__(m,end)
            
    
@grok.subscribe(IReserve, IObjectModifiedEvent)
def ReplicReserveEdit(obj, event):
    if obj.replic_semana:
        start = obj.replic_start
        end = obj.replic_end
        
        week = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        week_start = ['mon_start','tue_start','wed_start','thu_start','fri_start','sat_start','sun_start']
        week_end = ['mon_end','tue_end','wed_end','thu_end','fri_end','sat_end','sun_end']
            
        
        for i in week:
            obj.__setattr__(i,True)
            
        for j in week_start:
            obj.__setattr__(j,start)
        
        for m in week_end:
            obj.__setattr__(m,end)


# View
   
class ReserveView(grok.View):
    grok.context(IReserve)
    grok.require('zope2.View')
    grok.name('view')
  
    def getEvents(self):
        pc = getToolByName(self.context, 'portal_catalog')
        now = datetime.now()
        events = pc(portal_type='Event',
                    #review_state='published',
                    review_state = ['published','internal'],
                    sort_on='start',
                    path='/'.join(self.context.getPhysicalPath()),
                    end={'query':[now,],'range':'min'})
        
        if events:
            L = []
            for item in events:
                obj = item.getObject()
                D = {}
                D['title'] = obj.Title()
                D['url'] = obj.absolute_url()
                D['date'] = obj.startDate.strftime('%d/%m/%Y - %Hh %Mmin')
                L.append(D)
            return L 
        