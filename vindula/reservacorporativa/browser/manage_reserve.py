# -*- coding: utf-8 -*-
from five import grok

from .view_reserve import ViewReserve


grok.templatedir('templates')

class ManageReserve(ViewReserve):
    grok.name('gerenciar')

    url_frame = '%s/vindula-api/reserva_corporativa/%s/reserves/%s/?iframe_id=%s'
