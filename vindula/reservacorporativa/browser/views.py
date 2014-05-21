# -*- coding: utf-8 -*-
import datetime, time
from DateTime import DateTime
from five import grok
from zope.interface import Interface
from vindula.reservacorporativa.content.interfaces import IContentReserve
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot
from zope.app.component.hooks import getSite

#Importando a classe para pegar os dados do usuário do BD
from vindula.myvindula.tools.utils import UtilMyvindula

from dateutil.relativedelta import relativedelta
from datetime import timedelta, date

class ReservationRequestView(grok.View):
    grok.context(IContentReserve)
    grok.require('zope2.View')
    grok.name('reservation-request')
    
    
    def getReserves(self):
        pc = getToolByName(self.context, 'portal_catalog')
        reserves = pc(portal_type='vindula.reservacorporativa.content.reserve',
                      path={'query': '/'.join(self.context.getPhysicalPath()), 'depth': 1},
                      #review_state='published',
                      review_state = ['published','internal'],
                      sort_on='sortable_title',
                      sort_order='ascending',)
        if reserves:
            L = []
            for item in reserves:
                L.append(item.getObject())
            return L
        
        
class ReserveInformationView(grok.View):
    grok.context(IContentReserve)
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
                D['additional_items'] = obj.additional_items
                D['frequency'] = obj.frequency
                D['mult_horarios'] = obj.mult_horarios
                D['duration'] = obj.duration.strftime('%H:%M')
                D['hours'] = self.getAvailableTimes(obj)
                D['context'] = obj
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
            booked_slots = pc(portal_type=('Event','EventReserve'),
                              #review_state='published',
                              path='/'.join(folder.getPhysicalPath()),
                              start={'query':[start, end], 'range':'minmax'})
            
            # Search blocks configuration within the range
            blocked_slots = pc(portal_type='BlockReserve',
                              review_state='published',
                              path='/'.join(folder.getPhysicalPath())
                              )

            #Booked Events Recorentes
            events_recorents_slots = pc(portal_type=('Event','EventReserve'),
                                        getRecurrent=True,
                                        path='/'.join(folder.getPhysicalPath()),
                                        start={'query':[start, end], 'range':'minmax'})
            for day in days:
                # Checking it day
                checked_day = {}
                for key in day.keys(): checked_day[key] = day.get(key)
                checked_day['hours'] = []
                long_date = day.get('label').split(',')[1].strip()
                
                for slot in day.get('hours'):
                    # Checking the slots of the current day
                    slot_free = True
                    slot_start = slot['start']
                    slot_end = slot['end']
                    for obj in booked_slots:
                        obj = obj.getObject()
                        if obj.startDate.strftime('%d-%m-%Y') == day.get('day').strftime('%d-%m-%Y'):
                            event_start = datetime.time(obj.startDate.hour(),obj.startDate.minute())
                            event_end = datetime.time(obj.endDate.hour(),obj.endDate.minute())
                            
                            #Verifica se o slot ja foi ocupado por algum evento nesse dia
                            if slot_free:
                                #Checando se a reserva comeca e termina antes do slot ou se a reserva comece depois do fim do slot
                                #Se um dos casos for positivo, slot esta ocupado
                                slot_free = self.checkStartAndEndSlot(slot_start, slot_end, event_start, event_end)
                    
                    if slot_free:
                        for obj in blocked_slots:
                            obj = obj.getObject()

                            block_days_of_week =[]
                            [block_days_of_week.append(i) for i in obj.getDays_of_week() if i]
                            
                            frequency = obj.getFrequency()
                            block_slot = True
                            
                            if frequency == 'quinzenal':
                                #Quando é quinzenal verifica a primeira semana selecionada no conteúdo de bloqueio, verifica se ela é par ou impar,
                                #o block_slot vai receber o inverso da condicao se é primeira semana, para bloquear os slots semana sim, semana nao 
                                mod = obj.getWhen().week() % 2
                                block_slot = not DateTime(day.get('day').strftime('%Y-%m-%d')).week() % 2 == mod
                            elif frequency == 'mensal':
                                #Quando é mensal verifica o primeiro mes selecionado no conteúdo de bloqueio, verifica se ele é par ou impar,
                                #o block_slot vai receber o inverso da condicao se é primeiro mes, para bloquear os slots mes sim, mes nao 
                                mod = obj.getWhen().month() % 2
                                block_slot = not DateTime(day.get('day').strftime('%Y-%m-%d')).month() % 2 == mod
                            
                            if DateTime(day.get('day').strftime('%Y-%m-%d')) >= DateTime(obj.getWhen().strftime('%Y-%m-%d')) and \
                               DateTime(day.get('day').strftime('%Y-%m-%d')) <= DateTime(obj.getEven_when().strftime('%Y-%m-%d')) and \
                               long_date in block_days_of_week and \
                               block_slot:
                                
                                block_start = datetime.time(time.strptime(obj.getStart_time(), '%H:%M').tm_hour, time.strptime(obj.getStart_time(), '%H:%M').tm_min)
                                block_end = datetime.time(time.strptime(obj.getEnd_time(), '%H:%M').tm_hour, time.strptime(obj.getEnd_time(), '%H:%M').tm_min)
                                
                                #Verifica se o slot ja foi ocupado por algum block nesse dia
                                if slot_free:
                                    #Checando se a regra de bloqueio comeca e termina antes do slot ou se a regra de bloqueio comece depois do fim do slot
                                    #Se um dos casos for positivo, slot esta ocupado
                                    slot_free = self.checkStartAndEndSlot(slot_start, slot_end, block_start, block_end)

                    if slot_free:
                        dt_start = day.get('day')

                        for obj in events_recorents_slots:
                            obj = obj.getObject()
 
                            frequencia = obj.getFrequency()
                            data_reserva = obj.start_date.date() #.replace(tzinfo=None)
                            # data_reserva_end = obj.end_date.date()
                            
                            hora_reserva_start = obj.start_date.time()
                            hora_reserva_end = obj.end_date.time()
                            
                            stop_recurrent = obj.end_dateRecurrent
                            
                            if stop_recurrent:
                                stop_recurrent = stop_recurrent.asdatetime() + timedelta(days=1)
                                stop_recurrent = stop_recurrent.date() #.replace(tzinfo=None)

                            def checkSlotRecursive(self,slot_free, data_reserva,stop_recurrent, slot_start, slot_end, hora_reserva_start, hora_reserva_end):
                                if not stop_recurrent:
                                    if slot_free:
                                        slot_free = self.checkStartAndEndSlot(slot_start, slot_end, hora_reserva_start, hora_reserva_end)
      
                                elif data_reserva < stop_recurrent:
                                    if slot_free:
                                        slot_free = self.checkStartAndEndSlot(slot_start, slot_end, hora_reserva_start, hora_reserva_end)
                                return slot_free

                            if frequencia == 'semanal':

                                while data_reserva < dt_start:
                                    data_reserva = data_reserva + timedelta(days=7)
                                    if data_reserva == dt_start:
                                        slot_free = checkSlotRecursive(self,slot_free, data_reserva,stop_recurrent, slot_start, slot_end, hora_reserva_start, hora_reserva_end)
                                        
                            elif frequencia == 'quinzenal': 

                                while data_reserva < dt_start:
                                    data_reserva = data_reserva + timedelta(days=14)
                                    if data_reserva == dt_start:
                                        slot_free = checkSlotRecursive(self,slot_free, data_reserva,stop_recurrent, slot_start, slot_end, hora_reserva_start, hora_reserva_end)

                            elif frequencia == 'mensal':
                                
                                while data_reserva < dt_start:
                                    data_reserva = data_reserva + relativedelta(months=+1)
                                    if data_reserva == dt_start:
                                        slot_free = checkSlotRecursive(self,slot_free, data_reserva,stop_recurrent, slot_start, slot_end, hora_reserva_start, hora_reserva_end)

                    if slot_free:
                        checked_day['hours'].append(slot)
                            
                # Adding the checked day to the list of checked days
                checked_days.append(checked_day)
        return checked_days     

    #Checando se a acao comeca e termina antes do slot ou se a acao comeca depois do fim do slot
    #Se um dos casos for positivo, slot esta ocupado
    def checkStartAndEndSlot(self, slot_start, slot_end, action_start, action_end):
        if not (( (slot_start < action_start) and (slot_end <= action_start) ) or ( (slot_start >= action_end) )):
            return False
        return True
    
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
               L.append({'label':start.strftime('%H:%M') + ' ás ' + end.strftime('%H:%M'), 
                         'start':start, 
                         'end': end
                         })
               initial += duration
            return L 
        

    def createEvent(self, form):
        obj_path = form.get('obj_path')
        hours_selected = form.get('hours-selected')
        
        if hours_selected and obj_path:
            pc = getToolByName(self.context, 'portal_catalog')
            obj = pc(portal_type='vindula.reservacorporativa.content.reserve', path=obj_path)
            if obj:
                folder = obj[0].getObject()
                if not folder.mult_horarios and len(hours_selected) > 1:
                    self.context.plone_utils.addPortalMessage('Você não pode agendar mais de um horário para esta reserva.', 'error')
                    self.request.response.redirect(folder.aq_parent.absolute_url()+'/reservation-request')
                    return
                username = self.context.portal_membership.getAuthenticatedMember().getUserName()
                if form.get('name'):
                    name = form.get('name')
                else:
                    name = username
                title = folder.title + ' - ' + name
                hours_selected = self.getHoursSelected(hours_selected)
                
                for hour_selected in hours_selected:
                    if hour_selected:
                        date  = datetime.datetime.strptime(hour_selected['date'], '%d-%m-%Y')
                        start = hour_selected['start']
                        end   = hour_selected['end']
                        id = username + '-' + date.strftime('%d-%m-%Y') + (start + end).replace(':', '')

                        if form.get('recurrent', False):
                            form['recurrent'] = True
                        else:
                            form['recurrent'] = False

                        if form.get('end_date', False):

                            end_date = form.get('end_date','')
                            if not isinstance(end_date, DateTime):
                                try:
                                    end_date = end_date.split('/')
                                    form['end_date'] = DateTime(int(end_date[2]),int(end_date[1]),int(end_date[0]))
                                except:
                                    form['end_date'] = None

                        if folder.additional_items:
                            txt = ''
                            for item in folder.additional_items:
                                txt += '%s: %s \n'%(item.get('label',''),form.get(item.get('name','')))

                            form['text'] = txt

                        self.context.createObj(folder,id,title,date.strftime('%m-%d-%Y'),start,end,form)
                        self.context.publishObj(folder[id])
                        
                        msg = createMsgEmailReserve(folder[id], 'criada')
                        if folder[id].contact_email():
                            send_email(self.context, msg, 'Reserva Corporativa: ' + folder.Title() , folder[id].contact_email())
                        if folder.contact:
                            send_email(self.context, msg, 'Reserva Corporativa: ' + folder.Title() , folder.contact)
                
                # TO DO: VERIFICAR NOVAMENTE SE O SLOT ESTA DISPONIVEL

                if form.get('edit_event'):
                    id_old = form.get('edit_event')
                    self.context.removeObj(folder,id_old)
                    msg = createMsgEmailReserve(folder[id], 'alterada')
                    send_email(self.context, msg, 'Reserva Corporativa: ' + folder.Title() , folder[id].contact_email())
                    self.context.plone_utils.addPortalMessage('Sua reserva foi alterada com sucesso.', 'info')
                    self.request.response.redirect(self.context.portal_url()+'/my-reservations')
                    return
                
                self.context.plone_utils.addPortalMessage('Sua reserva foi criada com sucesso.', 'info')
                self.request.response.redirect(self.context.portal_url()+'/my-reservations')
            else:
                self.context.plone_utils.addPortalMessage('Ocorreu um erro durante a crição da sua reserva.', 'error')
                self.request.response.redirect(folder.aq_parent.absolute_url())
    
    def getHoursSelected(self, hours_selected):
        events=[]
        hours_selected.sort()
        for hour_selected in hours_selected:
            hour_selected = hour_selected.split('|')
            exist = False
            D={}
            D['date'] = hour_selected[0]
            D['start'] = hour_selected[1]
            D['end'] = hour_selected[2]
            for event in events:
                if event['date'] == D['date'] and D['start'] == event['end']:
                    event['end'] = D['end']
                    exist = True
            if not exist:
                events.append(D)
        return events
            
                
    def getEditEvent(self):
        form = self.request.form
        D = {}
        D['name'] = ''
        D['obs'] = ''
        D['qtd_pessoas']=''
        D['mail'] = ''
        D['phone'] = '' 
        D['local'] = ''
        D['id_edit'] = ''

        D['recurrent'] = ''
        D['frequency'] = ''
        D['end_date'] = ''

        if form.get('id_edit'):
            pc = getToolByName(self.context, 'portal_catalog')
            reserve_edit = pc(portal_type=('Event','EventReserve'), id=form.get('id_edit'))
            if reserve_edit:
                obj = reserve_edit[0].getObject()
                D['name'] = obj.contact_name()
                D['mail'] = obj.contact_email()
                D['phone'] = obj.contact_phone()
                D['obs'] = obj.Description()
                D['local'] = obj.getLocation()
                D['id_edit'] = obj.id
                D['qtd_pessoas'] = obj.getAttendees()

                if obj.portal_type == 'EventReserve':
                    D['recurrent'] = obj.getRecurrent()
                    D['frequency'] = obj.getFrequency()
                    D['end_date'] = obj.getEnd_dateRecurrent()

        else:
            ms = self.context.portal_membership
            user_login = ms.getAuthenticatedMember().getUserName()
            urser_bd = UtilMyvindula().get_prefs_user(user_login)
            if urser_bd:
                D['mail'] = urser_bd.get('email','')
                D['phone'] = urser_bd.get('phone_number','') or urser_bd.get('cell_phone','')
        
        return D 
    
# View
class ContentReserveView(grok.View):
    grok.context(IContentReserve)
    grok.require('zope2.View')
    grok.name('view')                    

    def update(self):
        pass
    
    
class MyReservationsView(grok.View):
    grok.context(ISiteRoot)
    grok.require('zope2.AccessContentsInformation')
    grok.name('my-reservations')
    
    
    def checkReservations(self):
        pc = getToolByName(getSite(), 'portal_catalog')
        ms = self.context.portal_membership
        user_login = ms.getAuthenticatedMember().getUserName()
        form = self.request.form
        
        if form.get('delete-ev'):
            event_delete =  pc(portal_type=('Event','EventReserve'), id=self.request.form.get('delete-ev'))
            if event_delete:
                event_delete = event_delete[0].getObject()
                id = event_delete.id
                folder = event_delete.aq_parent
                self.context.removeObj(folder,id)
                
                msg = createMsgEmailReserve(event_delete, 'excluída')
                send_email(self.context, msg, 'Reserva Corporativa: ' + event_delete.Title() , event_delete.contact_email())
                
                self.context.plone_utils.addPortalMessage('Sua reserva foi removida com sucesso.', 'info')
                self.request.response.redirect(self.context.portal_url()+'/@@my-reservations')
        
        query={}
        if form.get('prev_reservations'):
            date_range_query = { 'query': DateTime(), 'range': 'max'}
        else:
            date_range_query = { 'query': DateTime(), 'range': 'min'}
        query['Creator'] = user_login
        query['portal_type'] = ('Event','EventReserve')
        query['review_state'] = 'published'
        query['start'] = date_range_query
        query['sort_on'] = 'start'
        result = pc(**query)
        
        reservations = []
        if result:
            for obj in result:
                obj = obj.getObject()
                if obj.aq_parent.Type() == 'Reserva Corporativa':
                    reservations.append(obj)
        

        return reservations
    
class ReservationPrintView(grok.View):
    grok.context(Interface)
    grok.require('zope2.AccessContentsInformation')
    grok.name('print_reservations')
    
    def getFuturesReservations(self):
        pc = getToolByName(getSite(), 'portal_catalog')
        folder_path = '/'.join(self.context.aq_parent.getPhysicalPath())
        query={}

        query['portal_type'] = ('Event','EventReserve')
        query['review_state'] = 'published'
        query['start'] = {'query': DateTime().Date(), 'range': 'min'}
        query['sort_on'] = 'start'
        query['path'] = {'query': folder_path, 'depth': 20}
        
        result = pc(**query)
        reservations = []
        if result:
            for obj in result:
                obj = obj.getObject()
                if obj.aq_parent.Type() == 'Reserva Corporativa':
                        reservations.append(obj)
        
        return reservations


class ReservationsWeekView(grok.View):
    grok.context(IContentReserve)
    grok.require('zope2.AccessContentsInformation')
    grok.name('reservations-week')

    def getReserves(self):
        pc = getToolByName(self.context, 'portal_catalog')
        L = []
        reserves = pc(portal_type='vindula.reservacorporativa.content.reserve',
                      path={'query': '/'.join(self.context.getPhysicalPath()), 'depth': 1},
                      #review_state='published',
                      review_state = ['published','internal'],
                      sort_on='sortable_title',
                      sort_order='ascending',)
        if reserves:
            for item in reserves:
                L.append(item.getObject())
        return L
            
    def next_week(self,today):
        next_week = today + relativedelta(weeks=+1)
        year, week, dayBase = next_week.isocalendar()
        return year, week

    def prev_week(self,today):
        prev_week = today + relativedelta(weeks=-1)
        year, week, dayBase = prev_week.isocalendar()
        return year, week

    def list_weekdays(self,weekday):
        L= ['Segunda-Feira','Terça-Feira','Quarta-Feira','Quinta-Feira','Sexta-Feira','Sabado','Domingo']
        return L[weekday]

    def daysOfWeek(self, year, week):
        L = []
        if not isinstance(year,int):
            year=int(year)
        if not isinstance(week,int):
            week=int(week)

        day = date(year, 2, 1)
        year, weekBase, dayBase = day.isocalendar()
        day += timedelta(1 - dayBase + (week - weekBase)*7)
        today = day
        delta = timedelta(1)
        for i in range(7):
            L.append(day)
            day += delta
        return L,today

    def year_now(self):
        hoje = date.today()
        return hoje.year

    def week_now(self):
        hoje = date.today()
        return hoje.isocalendar()[1]

    def get_events_day(self,reserva,day):
        pc = getToolByName(self.context, 'portal_catalog')
        query={}
        query['path'] = {'query': '/'.join(reserva.getPhysicalPath()), 'depth': 99}
        day_max = day + timedelta(1)
        date_range_query = { 'query':(day,day_max), 'range': 'min:max'}
        query['portal_type'] = ('Event','EventReserve')
        query['review_state'] = 'published'
        query['start'] = date_range_query
        query['sort_on'] = 'start'
        result = pc(**query)

        return result


def createMsgEmailReserve(event, status):
    return '<p><strong>%s</strong> reservou horário na <strong>%s</strong>: </p>' \
           '<p><label>Data: </label><strong>%s</strong></p>' \
           '<p><label>Hor&aacute;rio: </label><strong>entre as %s e as %s</strong></p>' \
           '<p><label>Local: </label><strong>%s</strong></p>' \
           '<p>Foi %s dia %s</p>' \
           '<p><a href="%s">Clique aqui</a> para mais detalhes sobre a reserva %s</p><br>' \
           '<p>Para visualizar suas reservas acesse o <a href="%s">seu perfil</a></p>' % \
           ((event.getOwner().getProperty('fullname') or event.Creator()), event.aq_parent.Title(), event.start_date.strftime('%d/%m/%Y'),
            event.start_date.strftime('%H:%M'), event.end_date.strftime('%H:%M'), event.getLocation(), 
            status, DateTime().strftime('%d/%m/%Y às %H:%M'),event.aq_parent.absolute_url(),event.aq_parent.Title(),
            '%s/my-reservations' % getSite().absolute_url(),
            )
    
def send_email(ctx, msg, assunto, mail_para, arquivos=[], to_email=None):
    #Imports para envio de email
    import smtplib
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
    from email.MIMEBase import MIMEBase
    from email.MIMEImage import MIMEImage
    from email import Encoders
    
    """
    Parte do codigo retirado de:
        - http://dev.plone.org/collective/browser/ATContentTypes/branches/release-1_0-branch/lib/imagetransform.py?rev=10162
        - http://www.thescripts.com/forum/thread22918.html
        - http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/473810
    """
    portal = getSite()

    # Cria a mensagem raiz, configurando os campos necessarios para envio da mensagem.
    mensagem = MIMEMultipart('related')
    mensagem['Subject'] = assunto

    #Pega os remetentes do email pelas configurações do zope @@mail-controlpanel
    if to_email:
        mensagem['From'] = '%s <%s>' % (to_email,to_email)
    else:
        mensagem['From'] = '%s <%s>' % (portal.getProperty('email_from_name'),
                                        portal.getProperty('email_from_address'))
    
    mensagem['To'] = mail_para
    mensagem.preamble = 'This is a multi-part message in MIME format.'
    mensagem.attach(MIMEText(msg, 'html', 'utf-8'))
    
    # Atacha os arquivos
    if arquivos:
        for f in arquivos:
            if type(f) == dict:
                parte = MIMEBase('application', 'octet-stream')
                parte.set_payload(f.get('data',f))
                Encoders.encode_base64(parte)
                parte.add_header('Content-Disposition', 'attachment; filename="%s"' % f.get('filename','image.jpeg'))
                
                mensagem.attach(parte)
    
    mail_de = mensagem['From']

    #Pegando SmtpHost Padrão do Plone
    smtp_host   = ctx.MailHost.smtp_host
    smtp_port   = ctx.MailHost.smtp_port
    smtp_userid = ctx.MailHost.smtp_uid
    smtp_pass   = ctx.MailHost.smtp_pwd
    server_all  = '%s:%s'%(smtp_host,smtp_port)

    smtp = smtplib.SMTP()
    try:
        smtp.connect(server_all)
        #Caso o Usuario e Senha estejam preenchdos faz o login
        if smtp_userid and smtp_pass:
            try:
                smtp.ehlo()
                smtp.starttls()
                smtp.login(smtp_userid, smtp_pass)
            except:
                smtp.login(smtp_userid, smtp_pass)
                
        smtp.sendmail(mail_de, mail_para, mensagem.as_string())
        smtp.quit()
    except:
        return False

    return True       