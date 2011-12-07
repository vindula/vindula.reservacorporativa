# -*- coding: utf-8 -*-
from five import grok
from zope.interface import Interface


class ReservationRequestView(grok.View):
    grok.context(Interface)
    grok.require('cmf.ManagePortal')
    grok.name('reservation-request')