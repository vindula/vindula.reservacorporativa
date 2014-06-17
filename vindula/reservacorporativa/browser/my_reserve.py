# -*- coding: utf-8 -*-
from five import grok
from zope.interface import Interface

from .view_reserve import ViewReserve


grok.templatedir('templates')

class MyReserves(ViewReserve):
    grok.context(Interface)
    grok.name('minhas-reservas')

    url_frame = '%s/vindula-api/reserva_corporativa/%s/my-reserves/?iframe_id=%s'

    def get_url_frame(self):
        url = self.context.portal_url()
        user_token = self.request.SESSION.get('user_token')

        return self.url_frame %(url,user_token,self.get_id_frame())
    