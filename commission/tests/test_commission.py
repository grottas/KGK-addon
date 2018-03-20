
# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
import datetime
from .commissiondata import CommissionData as cd

class TestCommission(TransactionCase):
  arr_schemes = []
  arr_groups = []
  arr_users = []
  arr_leads = []
  arr_teams = []

  # set basic data
  def setUp(self, *args, **kwargs):
    super(TestCommission, self).setUp(*args, **kwargs)
    # set all groups to inactive
    self.env['commission.group'] \
      .search([('active', '=', True)]) \
      .write({'active' : False})

    # set all schemes inactive
    self.env['commission.scheme'] \
      .search([('active', '=', True)]) \
      .write({'active': False})

    # set all teams inactive
    #self.env['crm.team'] \
    #  .search([('active', '=', True)]) \
    #  .write({'active': False})
  
  # test the commission configuraton
  def test_populate_commission(self):
    self.populate_scheme()

    self.populate_hierarchy()

    #self.populate_user()
  
    self.populate_team()
  
  def test_calculate_commission(self):
    self.calculate_commission()
  
    

###################################################################################################################################
# private helper methods
  # create the tiers, schemes and groups
  def populate_scheme(self):
    print('populate scheme')
    # use demo user
    demo_user = self.env.ref('base.user_demo')

    # create two schemes for two products with two tiers each
    scheme = self.env['commission.scheme']
    self.scheme1 = scheme.create(cd.scheme_a1)
    self.scheme2 = scheme.create(cd.scheme_a2)

    self.arr_schemes.append(self.scheme1.id)
    self.arr_schemes.append(self.scheme2.id)

    tier = self.env['commission.tier']

    count = len(scheme.search([('active', '=', True)]))
    self.assertEqual(count, 2, 'error creating schemes')

    count = len(tier.search([('scheme.id', 'in', [self.scheme1.id, self.scheme2.id])]))
    self.assertEqual(count, 4, 'error creating agent tiers')

    # create manager commission scheme
    self.scheme3 = scheme.create(cd.scheme_m1)
    self.scheme4 = scheme.create(cd.scheme_m2)
    self.arr_schemes.append(self.scheme3.id)

    # create two commission groups
    group = self.env['commission.group']
    self.group1 = group.create({
      'name' : 'manager',
      'active' : True
    })
    self.group2 = group.create({
      'name' : 'agent',
      'active' : True,
    })

    self.arr_groups.append(self.group1.id)
    self.arr_groups.append(self.group2.id)

    self.group2.scheme_ids += self.scheme1
    self.group2.scheme_ids += self.scheme2
    self.group1.scheme_ids += self.scheme3
    self.group1.scheme_ids += self.scheme4

    #assign team to groups
    self.team1 = self.env['crm.team'].search([('id', '=', cd.team_id1)])
    self.manager_team1 = self.env['crm.team'].search([('id', '=', cd.manager_team_id1)])
    self.group1.team_ids += self.manager_team1[0]
    self.group2.team_ids += self.team1[0]

    count = len(scheme.search([('active', '=', True)]))
    self.assertEqual(count, 4, 'error creating schemes')

    count = len(tier.search([('scheme.id', 'in', [self.scheme3.id])]))
    self.assertEqual(count, 1, 'error creating manager tiers')

    count = len(group.search([('active', '=', True)]) )
    self.assertEqual(count, 2, 'wrong group count')

    count = len(group.search([('team_ids', '=', cd.manager_team_id1)]))
    self.assertEqual(count, 1, 'manager group - team count')
    count = len(self.group2.team_ids)
    self.assertEqual(count, 1, 'agent group - team count')

  # create the commission hierarchy
  def populate_hierarchy(self):
    hierarchy = self.env['commission.hierarchy']
    
    # default run
    if len(self.arr_teams) == 0:
      self.node1 = hierarchy.create({
        'name' : 'hq',
        'team' : 1
      })
      self.node2 = hierarchy.create({
        'name' : 'region1',
        'parent_id' : self.node1.id,
        'team' : 2
      })
      self.node3 = hierarchy.create({
        'name': 'team lead1',
        'parent_id' : self.node2.id,
        'team' : 3
      })
      self.node4 = hierarchy.create({
        'name' : 'team1',
        'parent_id' : self.node3.id,
        'team' : 1
      })

      count = len(hierarchy.search([('id', '>=', self.node1.id)]))
      self.assertEqual(count, 4, 'creating hierarchy')
      return

    start_count = hierarchy.search_count([])

    # create all nodes first
    for team in self.arr_teams:
      self.node1 = hierarchy.create({
        'name' : team.name,
        'team' : team.id,
      })

    # add parent node
    for node in cd.arr_hierarchy:
      if node[1] == '':
        continue
      
      parent = hierarchy.search([('name', '=', node[1])])
      self.assertEqual(len(parent), 1, 'parent legnth')
      child = hierarchy.search([('name', '=', node[0])])
      self.assertEqual(len(child), 1, 'child length')
      child[0].parent_id = parent[0]      
      
    # check that the last entries parent matches
    node = cd.arr_hierarchy[-1]
    child = hierarchy.search([('name', '=', node[0])])
    parent = child.parent_id
    self.assertEqual(parent.name, node[1], 'parent match')
    count = hierarchy.search_count([])
    self.assertEqual(count - start_count, len(self.arr_teams), 'hierarchy count')


  #create new useres
  def populate_user(self):
    users = self.env['res.users']
    self.arr_users = []

    for x in range(1, 21):
      name = 'user ' + str(x)

      self.user1 = users.create({
        'company_id': self.env.ref("base.main_company").id,
        'name': name,
        'login': name,
        'email': 'agent@kgk.vn',
        'groups_id': [(6, 0, [self.ref('sales_team.group_sale_manager')])]
      })
      self.arr_users.append(self.user1)
      
    count = len(users.search([('email', '=', 'agent@kgk.vn')]))
    self.assertEqual(count, 20, 'create salesman')
    self.assertEqual(len(self.arr_users), 20, 'user count')

    #create leads
    for name in cd.arr_leads:
      self.lead1 = users.create({
        'company_id': self.env.ref("base.main_company").id,
        'name': name,
        'login': name,
        'email': 'lead@kgk.vn',
        'groups_id': [(6, 0, [self.ref('sales_team.group_sale_manager')])]
      })
      self.arr_leads.append(self.lead1)
      
    count = len(users.search([('email', '=', 'lead@kgk.vn')]))
    self.assertEqual(len(self.arr_leads), count, 'lead count')



  # create salesteams
  def populate_team(self):
    team = self.env['crm.team']

    # default run
    if len(self.arr_users) == 0:
      agents = [1,5]
      for x in agents:
        name = 'team ' + str(x)
        self.team1 = team.create({
          'name' : name,
          'active' : True,
          'user_id' : x
        })
        #self.arr_teams.append(self.team1)

      name = 'team ' + str(agents[0])
      count = len(team.search([('name', '=', name)]))
      self.assertEqual(count, 1, 'create team')
      return

    # create teams for leads
    for lead in self.arr_leads:
      self.team1 = team.create({
        'name': lead.name,
        'active' : True,
        'user_id' : lead.id
      })
      self.arr_teams.append(self.team1)
    count = len(team.search([('active', '=', True)]))
    self.assertEqual(count, len(self.arr_leads), 'count for lead teams')

    # add users to the leads teams
    x = 0
    for agent in self.arr_users:
      if x < 5:
        self.arr_teams[-1].member_ids += agent
        x += 1
      else:
        self.arr_teams[len(self.arr_teams) - 2].member_ids += agent

    name = self.arr_teams[-1].name
    lead_team = team.search([('name', '=', name)])
    members = len(lead_team.member_ids)
    self.assertEqual(members, 5, 'lead 2 member team count')


  # commission calculation
  def calculate_commission(self):
    #self.populate_user()
    self.populate_scheme()
    self.populate_team()
    self.populate_hierarchy()
    # get user_ids for agents
    arr_agents = []
    for user in self.arr_users:
      arr_agents.append(user.id)
    #self.create_sales(arr_agents)
    #elf.execute_calc()


  # create sales order
  def create_sales(self, agents = [cd.agent_id1]):
    for agent in agents:
      sales = self.env['sale.order'].sudo(agent)
      partners = self.env['res.partner'].search([('customer', '=', True)])
      partner = partners[0]
      product = self.env['product.product'].search([('id', '=', cd.prod_id1)])
      start_count = len(self.env['sale.order.line'].search([('salesman_id', '=', agent)]))
      order_count = len(sales.search([('partner_id', '=', partner.id)]))

      self.so = sales.create({
        'partner_id': partner.id,
        'partner_invoice_id': partner.id,
        'partner_shipping_id': partner.id,
        'order_line': [(0, 0, {'name': product.name, 'product_id': product.id, 
          'product_uom_qty': 2, 
          'product_uom': product.uom_id.id,
          'price_unit': product.list_price, 
          'salesman_id' : agent
        })]
      })

      so_id = self.so.id
      count = len(sales.search([('id', '=', so_id)]))
      self.assertEqual(count, 1, 'verify order')
      count = len(sales.search([('partner_id', '=', partner.id)]))
      self.assertEqual(count - order_count, 1, 'order count')
      count = len(self.env['sale.order.line'].search([('salesman_id', '=', agent)]))
      self.assertEqual(count - start_count, 1, 'verify order line')

      product = self.env['product.product'].search([('id', '=', cd.prod_id2)])
      self.so1 = sales.create({
        'partner_id': partner.id,
        'partner_invoice_id': partner.id,
        'partner_shipping_id': partner.id,
        'order_line': [(0, 0, {'name': product.name, 'product_id': product.id, 
          'product_uom_qty': 1, 
          'product_uom': product.uom_id.id,
          'price_unit': product.list_price, 
          'salesman_id' : agent
        })]
      })

  # call the calculation method
  def execute_calc(self):
    self.env['commission'].calculate()