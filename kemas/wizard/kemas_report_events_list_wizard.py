# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import addons

class kemas_report_events_list_wizard(osv.osv_memory):
    def call_report(self, cr, uid, ids, context=None):
        datas = {}     
        if context is None:
            context = {}
        data = self.read(cr, uid, ids, [])[0]
        datas = {
            'ids': ids,
            'model': 'ir.ui.menu',
            'form': data
            }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'event_list_report',
            'datas': datas,
            }

    _name='kemas.report.events.list.wizard'
    _columns={
        'logo': fields.binary('img'),
        'collaborator_id': fields.many2one('kemas.collaborator','Collaborator',ondelete='cascade', help=''),
        'place_id': fields.many2one('kemas.place','Place',ondelete='cascade', help=''),
        'service_id': fields.many2one('kemas.service','Service',ondelete='cascade', help=''),
        'date_start': fields.date('Date start'),
        'date_end': fields.date('Date end'),
        'state': fields.selection([
            ('all','All'),
            ('draft','Draft'),
            ('on_going','On Going'),
            ('closed','Closed'),
            ('canceled','Canceled'),
            ],'State', required=True),
        }
    
    def _get_logo(self, cr, uid, context=None):
        photo_path = addons.get_module_resource('kemas','images','report.png')
        return open(photo_path, 'rb').read().encode('base64')
    _defaults = {  
        'state': 'on_going',
        'logo': _get_logo,
        }
    
    def validate_dates(self,cr,uid,ids):
        wizard = self.read(cr, uid, ids[0],['date_start','date_end'])
        if wizard['date_start'] > wizard['date_end']:
            raise osv.except_osv(u'¡Operación no válida!', _('The date from which to search for events can not be higher than the deadline.'))
        else:
            return True
            
    _constraints=[
        (validate_dates,'The date from which to search for events can not be higher than the deadline.',['date_start'])
        ]
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

