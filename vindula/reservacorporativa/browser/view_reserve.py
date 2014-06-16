# -*- coding: utf-8 -*-
from five import grok
from zope.interface import Interface
from vindula.reservacorporativa.content.interfaces import IVindulaReserve

from hashlib import md5

grok.templatedir('templates')

class ViewReserve(grok.View):
    grok.context(IVindulaReserve)
    grok.require('zope2.View')
    grok.name('view')    

    url_frame = '%s/vindula-api/reserva_corporativa/%s/make-reserve/%s/?iframe_id=%s'                

    def update(self):
        context = self.context
        self.portal_type = context.portal_type
        self.UID = context.UID()

    def get_id_frame(self):
        return md5(self.portal_type + self.UID).hexdigest()

    def get_url_frame(self):
        url = self.context.portal_url()
        user_token = self.request.SESSION.get('user_token')

        return self.url_frame %(url,user_token,self.UID,self.get_id_frame())
    