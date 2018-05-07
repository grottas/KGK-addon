# -*- coding: utf-8 -*-

from odoo import models, fields, api

class commission_hierarchy(models.Model):
    _name = 'commission.hierarchy'
    _description = 'sales person hierarchy'
    _parent_name = 'parent_id'
    _parent_store = True
    _parent_order = 'name'
    _order = 'parent_left'

    name = fields.Char(string = 'Node', required = True, size = 30, Translate = True)
    parent_id = fields.Many2one('commission.hierarchy', 'Parent node', index=True, ondelete='restrict')
    child_id = fields.One2many('commission.hierarchy', 'parent_id', 'Child nodes')
    parent_left = fields.Integer('Left Parent', index=1)
    parent_right = fields.Integer('Right Parent', index=1)
    team_ids = fields.Many2many('crm.team', 'comm_hierarchy_team', 'hierarchy_id', 'team_id', string = 'Sales teams')
    manager = fields.Many2one('res.users', string = 'Manager')

    @api.multi
    def name_get(self):
        def get_names(cat):
            """ Return the list [cat.name, cat.parent_id.name, ...] """
            res = []
            while cat:
                res.append(cat.name)
                cat = cat.parent_id
            return res

        return [(cat.id, " / ".join(reversed(get_names(cat)))) for cat in self]


    @api.constrains('parent_id')
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('Error ! You cannot create recursive nodes.'))
        return True

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if not args:
            args = []
        if name:
            # Be sure name_search is symetric to name_get
            node_names = name.split(' / ')
            parents = list(node_names)
            child = parents.pop()
            domain = [('name', operator, child)]
            if parents:
                names_ids = self.name_search(' / '.join(parents), args=args, operator='ilike', limit=limit)
                node_ids = [name_id[0] for name_id in names_ids]
                if operator in expression.NEGATIVE_TERM_OPERATORS:
                    nodes = self.search([('id', 'not in', node_ids)])
                    domain = expression.OR([[('parent_id', 'in', nodes.ids)], domain])
                else:
                    domain = expression.AND([[('parent_id', 'in', node_ids)], domain])
                for i in range(1, len(node_names)):
                    domain = [[('name', operator, ' / '.join(node_names[-1 - i:]))], domain]
                    if operator in expression.NEGATIVE_TERM_OPERATORS:
                        domain = expression.AND(domain)
                    else:
                        domain = expression.OR(domain)
            nodes = self.search(expression.AND([domain, args]), limit=limit)
        else:
            nodes = self.search(args, limit=limit)
        return nodes.name_get()



    @api.model
    def child_nodes_deep(self, node_id):
        # return all child nodes below this node
        if not node_id:
            node_id = 1

        result = []

        node = self.browse([node_id])
        if not node:
            return result

        children = node.child_id
        if not children:
            return result
        result = self.__children(node)
        return result

    @api.model
    def parent_node(self, node_id):
        # return the parent node 
        if not node_id:
            node_id = 1
        
        node = self.browse([node_id])
        if not node:
            return None
        return node.parent_id


    @api.model
    def sales_agents(self, node_id):
        # return all sales agents below this node
        if not node_id:
            node_id = 1

    
    def __children(self, node):
        result = []

        tmp_node = self.browse([(node.id)])

        for child in tmp_node[0].child_id:
            result.append(child)
            result.extend(self.__children(child))

        return result
