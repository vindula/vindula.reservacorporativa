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
            D['obj_path'] = obj.absolute_url_path()
            D['title'] = obj.title
            D['description'] = obj.description
            D['local'] = obj.local
            D['contact'] = obj.contact
            D['frequency'] = obj.frequency
            D['hours'] = self.getAvailableTimes(obj)
            return D
        
        
    def getAvailableTimes(self, obj):
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        oneweek = datetime.timedelta(days=7)
        days = []
        
        # L - label || F = field || W = weekday || H = hours
        fields = [{'L':'segunda','F':obj.monday,   'W':0,'H': self.getHours(obj.mon_start, obj.mon_end, obj.duration)},
                  {'L':'terça',  'F':obj.tuesday,  'W':1,'H': self.getHours(obj.tue_start, obj.tue_end, obj.duration)},
                  {'L':'quarta', 'F':obj.wednesday,'W':2,'H': self.getHours(obj.wed_start, obj.wed_end, obj.duration)},
                  {'L':'quinta', 'F':obj.thursday, 'W':3,'H': self.getHours(obj.thu_start, obj.thu_end, obj.duration)},
                  {'L':'sexta',  'F':obj.friday,   'W':4,'H': self.getHours(obj.fri_start, obj.fri_end, obj.duration)},
                  {'L':'sábado', 'F':obj.saturday, 'W':5,'H': self.getHours(obj.sat_start, obj.sat_end, obj.duration)},
                  {'L':'domingo','F':obj.sunday,   'W':6,'H': self.getHours(obj.sun_start, obj.sun_end, obj.duration)}]
        
        for field in fields:
            if field['F']:
                # Get next day this week, next Monday for example.
                weekday = today
                while weekday.weekday() != field['W']:
                    weekday += oneday
                    
                # Take the next four days a week. The next four Mondays, for example.
                L = []
                cont = 4
                while cont != 0:
                    L.append({'day': weekday,'label':weekday.strftime('%d/%m/%y, ') + field['L'], 'hours': field['H']})
                    weekday = weekday + oneweek
                    cont -= 1
                days += L
        days.sort()
        return days     
    
    
    def getHours(self, time_start=None, time_end=None, duration=None):
        if time_start and time_end and duration:
            # Convert from datetime.time to minutes
            initial = (time_start.hour * 60) + time_start.minute
            final = (time_end.hour * 60) + time_end.minute
            duration = (duration.hour * 60) + duration.minute
            
            L = []
            while initial < final:
               time_event =  initial + duration
               # Convert from minutes  to datetime.time
               start = datetime.time(initial / 60, initial % 60)
               end = datetime.time(time_event / 60, time_event % 60)
               L.append({'label':start.strftime('%H:%M') + ' às ' + end.strftime('%H:%M'), 'start':start, 'end': end})
               initial += duration
            return L 
    
    
    def checkHour(self):
        pass
    
    
class SchedulingReservationView(grok.View):
    grok.context(Interface)
    grok.require('cmf.ManagePortal')
    grok.name('scheduling-reservation')
    
    
    def createEvent(self):
        form = self.request.form
        pc = self.context.portal_catalog
        username = self.context.portal_membership.getAuthenticatedMember().getUserName()
        
        if form.get('obj_path'):
            obj = pc.searchResults(path=form.get('obj_path'))
            if obj:
                folder = obj[0].getObject()
                
                id = username + '-' + datetime.datetime.now().strftime('%d-%m-%y-%H%M%S')
                title = folder.title + ' - ' + username
                
                folder.invokeFactory('Event', 
                                      id=id, 
                                      title=title, 
                                      description='', 
                                      start_date=form.get('event_date'), 
                                      end_date=form.get('event_date'), 
                                      start_time=form.get('event_start'), 
                                      stop_time=form.get('event_end'))
                
                event = folder[id]
                portal_workflow = getToolByName(event, 'portal_workflow')
                portal_workflow.doActionFor(event, 'publish')
                
                link = event.absolute_url()
                return link