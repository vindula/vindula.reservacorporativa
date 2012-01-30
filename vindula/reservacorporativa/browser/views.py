# -*- coding: utf-8 -*-
import datetime
from DateTime import DateTime
from five import grok
from zope.interface import Interface
from vindula.reservacorporativa.content.interfaces import IContentReserve
from Products.CMFCore.utils import getToolByName


class ReservationRequestView(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('reservation-request')
    
    
    def getReserves(self):
        pc = getToolByName(self.context, 'portal_catalog')
        reserves = pc(portal_type='vindula.reservacorporativa.content.reserve',
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
    grok.require('zope2.View')
    grok.name('reserve-information')


    def getInfoReserve(self, id):
        form = self.request.form

        if form.get('create_event'):
            self.createEvent(form)
        
        else:    
            pc = getToolByName(self.context, 'portal_catalog')
            reserve = pc(portal_type='vindula.reservacorporativa.content.reserve', id=id)
            if reserve:
                obj = reserve[0].getObject()
                D = {}
                D['obj_path'] = '/'.join(obj.getPhysicalPath())
                D['title'] = obj.title
                D['description'] = obj.description
                D['local'] = obj.local
                D['contact'] = obj.contact
                D['frequency'] = obj.frequency
                D['duration'] = obj.duration.strftime('%H:%M')
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
                    L.append({'day': weekday,
                              'label':weekday.strftime('%d/%m/%y, ') + field['L'], 
                              'hours':field['H'],
                              })
                    weekday = weekday + oneweek
                    cont -= 1
                days += L
        days.sort()
        days = self.checkAvailableSlots(obj,days) 
        return days
         
         
    def checkAvailableSlots(self,folder,days):
        checked_days = []
        if len(days) > 0:
            pc = getToolByName(self.context, 'portal_catalog',)
            start = DateTime(days[0]['day'].strftime('%Y/%m/%d'))
            end = DateTime((days[len(days)-1]['day'] + datetime.timedelta(days=1)).strftime('%Y/%m/%d'))
            
            # Search events within the range
            booked_slots = pc(portal_type='Event',
                              review_state='published',
                              path='/'.join(folder.getPhysicalPath()),
                              start={'query':[start, end], 'range':'minmax'})            

            for day in days:
                # Checking it day
                checked_day = {}
                for key in day.keys(): checked_day[key] = day.get(key)
                checked_day['hours'] = []
                for slot in day.get('hours'):
                    # Checking the slots of the current day
                    slot_free = True
                    for obj in booked_slots:
                        obj = obj.getObject()
                        if obj.startDate.strftime('%d-%m-%Y') == day.get('day').strftime('%d-%m-%Y'):
                            event_start = datetime.time(obj.startDate.hour(),obj.startDate.minute())
                            event_end = datetime.time(obj.endDate.hour(),obj.endDate.minute())
                            slot_start = slot['start']
                            slot_end = slot['end']
                            if not (( (slot_start < event_start) and (slot_end <= event_start) ) or ( (slot_start >= event_end) )):
                                slot_free = False

                    if slot_free == True:
                        checked_day['hours'].append(slot)
                            
                # Adding the checked day to the list of checked days
                checked_days.append(checked_day)
        return checked_days     
        
    
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
               L.append({'label':start.strftime('%H:%M') + ' às ' + end.strftime('%H:%M'), 
                         'start':start, 
                         'end': end
                         })
               initial += duration
            return L 
        

    def createEvent(self, form):
        date = form.get('event_date')
        start = form.get('event_start')
        end = form.get('event_end')
        obj_path = form.get('obj_path')
 
        if date and start and end and obj_path:
            pc = getToolByName(self.context, 'portal_catalog')
            obj = pc(portal_type='vindula.reservacorporativa.content.reserve', path=obj_path)
            if obj:
                folder = obj[0].getObject()
                username = self.context.portal_membership.getAuthenticatedMember().getUserName()
                id = username + '-' + datetime.datetime.now().strftime('%d-%m-%y-%H%M%S')
                if form.get('name'):
                    name = form.get('name')
                else:
                    name = username
                title = folder.title + ' - ' + name
                
                # TO DO: VERIFICAR NOVAMENTE SE O SLOT ESTA DISPONIVEL
                
                folder.invokeFactory('Event', 
                                      id=id, 
                                      title=title, 
                                      description=form.get('obs'), 
                                      start_date=date, 
                                      end_date=date, 
                                      start_time=start, 
                                      stop_time=end, 
                                      location=form.get('local'),
                                      contact_name=form.get('name'),
                                      contact_phone=form.get('phone'),
                                      contact_email=form.get('mail')) 

                self.context.publishObj(folder[id])
                self.context.plone_utils.addPortalMessage('Sua reserva foi criada com sucesso.', 'info')
                self.request.response.redirect(folder[id].absolute_url())
            else:
                self.context.plone_utils.addPortalMessage('Ocorreu um erro durante a crição da sua reserva.', 'error')
                self.request.response.redirect(self.context.portal_url())   
                
                
                
    
# View
class ContentReserveView(grok.View):
    grok.context(IContentReserve)
    grok.require('zope2.View')
    grok.name('view')                    
    
    
    def update(self):
        pass
    