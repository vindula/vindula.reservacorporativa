## Script (Python) "publishObj"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=obj
##title=
##
from Products.CMFCore.utils import getToolByName
portal_workflow = getToolByName(obj, 'portal_workflow')
portal_workflow.doActionFor(obj, 'publish')