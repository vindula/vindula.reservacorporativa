# -*- coding: utf-8 -*-
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from vindula.reservacorporativa import MessageFactory as _
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from vindula.reservacorporativa.config import *

from vindula.reservacorporativa.content.interfaces import IContentReserve
from zope.app.component.hooks import getSite
from zope.component import adapter
from zope.app.container.interfaces import IObjectAddedEvent

contentReserve_schema = ATFolder.schema.copy() + Schema(())


finalizeATCTSchema(contentReserve_schema, folderish=True)

class ContentReserve(ATFolder):
    """ Reserve Content for Events, Colection, Reserve Corp"""
    
    implements(IContentReserve)    
    portal_type = 'ContentReserve'
    _at_rename_after_creation = True
    schema = contentReserve_schema

registerType(ContentReserve, PROJECTNAME) 


    
@adapter(IContentReserve, IObjectAddedEvent)
def CreatElemetsFormReserve(context, event):
    portal = getSite()
    portal_workflow = getToolByName(portal, 'portal_workflow')
    
    objects = {'type_name':'Topic',
               'id': 'calendario',
               'title':'Calendário',
               'description':'Calendário de reservas corporativa da intranet.'}

    context.invokeFactory(**objects)  
    
    if 'calendario' in context.keys():
        colection = context['calendario']
        portal_workflow.doActionFor(colection, 'publish')
        
        theCriteria = colection.addCriterion('Type','ATSelectionCriterion')
        theCriteria.setValue("Event")
        
        theCriteria = colection.addCriterion('path','ATPathCriterion')
        theCriteria.setValue(context)
        theCriteria.setRecurse(True)
        
        #theCriteria = colection.addCriterion('review_state','ATSelectionCriterion')
        #theCriteria.setValue('published')
        #theCriteria.setOperator('and')
        
        colection.setLayout('solgemafullcalendar_view')
        
        


