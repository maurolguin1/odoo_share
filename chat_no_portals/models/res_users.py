from openerp.osv import osv, fields


class res_users(osv.Model):
    _inherit = "res.users"

    def im_search(self, cr, uid, name, limit=20, context=None):
        """ search users with a name and return its id, name and im_status """
        result = [];
        # find the employee group
        group_employee = self.pool['ir.model.data'].get_object_reference(cr, uid, 'base', 'group_user')[1]

        where_clause_base = " U.active = 't' "
        query_params = ()
        if name:
            where_clause_base += " AND P.name ILIKE %s "
            query_params = query_params + ('%'+name+'%',)

        if(len(result) < limit):
            cr.execute('''SELECT U.id as id, P.name as name, COALESCE(S.status, 'offline') as im_status
                FROM res_users U
                    LEFT JOIN im_chat_presence S ON S.user_id = U.id
                    LEFT JOIN res_partner P ON P.id = U.partner_id
                WHERE   '''+where_clause_base+'''
                        AND U.id != %s
                        AND EXISTS (SELECT 1 FROM res_groups_users_rel G WHERE G.gid = %s AND G.uid = U.id)
                ORDER BY P.name
                LIMIT %s
            ''', query_params + (uid, group_employee, limit))
            result = result + cr.dictfetchall()

        return result