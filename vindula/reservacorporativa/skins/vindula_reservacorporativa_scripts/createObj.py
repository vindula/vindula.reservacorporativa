## Script (Python) "createObj"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=folder,id,title,date,start,end,form
##title=
##


folder.invokeFactory('EventReserve', 
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

event = folder[id]
event.setRecurrent(form.get('recurrent'))
event.setFrequency(form.get('frequency'))
event.setEnd_dateRecurrent(form.get('end_date'))
event.reindexObject()