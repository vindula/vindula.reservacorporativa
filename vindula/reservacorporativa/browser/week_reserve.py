# -*- coding: utf-8 -*-
from five import grok

from .view_reserve import ViewReserve


grok.templatedir('templates')

class WeekReserve(ViewReserve):
    grok.name('reservations-week')

    url_frame = '%s/vindula-api/reserva_corporativa/%s/week-reserves/%s/?iframe_id=%s'
