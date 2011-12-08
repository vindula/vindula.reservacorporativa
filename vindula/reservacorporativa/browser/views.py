# -*- coding: utf-8 -*-
import datetime
from five import grok
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName


class ReservationRequestView(grok.View):
    grok.context(Interface)
    grok.require('cmf.ManagePortal')
    grok.name('reservation-request')
    
    def getReserves(self):
        self.pc = getToolByName(self.context, 'portal_catalog')
        reserves = self.pc(portal_type='vindula.reservacorporativa.content.reserve',
                           review_state='published',
                           sort_on='sortable_title',
                           sort_order='ascending',)
        if reserves:
            L = []
            for item in reserves:
                L.append(item.getObject())
            return L
        
        
class ReserveInformationView(grok.View):
    grok.context(Interface)
    grok.require('cmf.ManagePortal')
    grok.name('reserve-information')
    
    def getInfoReserve(self, id):
        self.pc = getToolByName(self.context, 'portal_catalog')
        reserve = self.pc(portal_type='vindula.reservacorporativa.content.reserve', id=id)
        if reserve:
            obj = reserve[0].getObject()
            D = {}
            D['title'] = obj.title
            D['description'] = obj.description
            D['local'] = obj.local
            D['contact'] = obj.contact
            D['hours'] = self.getAvailableTimes(obj)
            return D
        
    def getAvailableTimes(self, obj):
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        oneweek = datetime.timedelta(days=7)
        days = []
        
        fields = [{'label':'segunda', 'weekday':obj.monday,    'calendar':0},
                  {'label':'terça',   'weekday':obj.tuesday,   'calendar':1},
                  {'label':'quarta',  'weekday':obj.wednesday, 'calendar':2},
                  {'label':'quinta',  'weekday':obj.thursday,  'calendar':3},
                  {'label':'sexta',   'weekday':obj.friday,    'calendar':4},
                  {'label':'sábado',  'weekday':obj.saturday,  'calendar':5},
                  {'label':'domingo', 'weekday':obj.sunday,    'calendar':6}]
        
        for field in fields:
            if field['weekday']:
                weekday = today
                while weekday.weekday() != field['calendar']:
                    weekday += oneday
                L = []
                cont = 4
                while cont != 0:
                    if cont != 4:
                        weekday = weekday + oneweek
                    L.append({'day': weekday,'label':weekday.strftime('%d/%m, ') + field['label'], 'hours': 'horas disponiveis'})
                    cont -= 1
                days += L
        days.sort()
        return days        