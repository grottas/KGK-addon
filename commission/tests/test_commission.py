
# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.tests.common import SingleTransactionCase
import datetime
from .commissiondata import CommissionData as cd
from .commissiondata import TestCase1 as t1
from .commissiondata import TestCase2 as t2
from .commissiondata import TestCase3 as t3
import time

class TestCommission(TransactionCase):
  arr_schemes = []
  arr_groups = []
  arr_users = []
  arr_leads = []
  arr_teams = []
  prefix = 'UT_'

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
    self.env['crm.team'] \
      .search([('active', '=', True)]) \
      .write({'active': False})
  
  # test the commission configuraton
  def test_populate_commission(self):
    print('test run configuration')
    #self.populate_scheme()

    #self.populate_hierarchy()

    #self.populate_user()
  
    #self.populate_team()
  
  def test_calculate_commission(self):
    self.calculate_commission(t3())
    #self.__create_sales(t1().salelines)
    #self.env['commission'].calculate()
    
  
    

###################################################################################################################################
# private helper methods
  # create the tiers, schemes and groups
  def populate_scheme(self):
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
  def populate_hierarchy(self, arr_teams=None, testcase=None):
    hierarchy = self.env['commission.hierarchy']
    
    # default run
    if testcase == None:
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

    #testcase run
    start_count = hierarchy.search_count([])

    # create all nodes first
    for node in testcase.nodes:
      self.node1 = hierarchy.create({
        'name' : self.prefix + node.get('name'),
      })
      #assign manager
      temp = self.env['res.users'].search([('login', '=', self.prefix + node.get('manager'))])
      if len(temp) > 0:
        self.node1.manager = temp[0]
      #assign teams
      for team in node.get('teams'):
        tmp_team = self.env['crm.team'].search([('name', '=', self.prefix + team)])
        if len(tmp_team) > 0:
          self.node1.team_ids += tmp_team[0]

    # add parent node
    for node in testcase.nodes: 
      if node.get('parent') == '':
        continue
      
      parent = hierarchy.search([('name', '=', self.prefix + node.get('parent'))])
      self.assertEqual(len(parent), 1, 'parent length for ' + node.get('name'))
      child = hierarchy.search([('name', '=', self.prefix + node.get('name'))])
      self.assertEqual(len(child), 1, 'child length ' + node.get('name') )
      child[0].parent_id = parent[0]      
      
  
    count = hierarchy.search_count([])
    self.assertEqual(count - start_count, len(testcase.nodes), 'wrong hierarchy count')


  #create new useres
  def populate_user(self, arr_names=[]):
    users = self.env['res.users']
    self.arr_users = []

    #default run
    if len(arr_names) == 0:
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
      return

    #create users based on the names provided
    before_count = users.search_count([])
    for user in arr_names:
      name = str(user)
      self.user1 = users.create({
          'company_id': self.env.ref("base.main_company").id,
          'name': name,
          'login': self.prefix + name,
          'email': 'agent_test@kgk.vn',
          'groups_id': [(6, 0, [self.ref('sales_team.group_sale_manager')])]
        })
      self.arr_users.append(self.user1)
    count = users.search_count([])
    self.assertEqual(len(arr_names), count - before_count, 'user setup count')

    return self.arr_users



  # create salesteams
  def populate_team(self, arr_tems):
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

    # create teams for testcase
    for team in arr_teams:
      self.team1 = team.create({
        'name': self.prefix + team.name,
        'active' : True,
        'use_opportunities' : False,
        'use_quotations' : False,
      })
      #assign members
      for member in team.members:
        temp = self.env['res.users'].search([('login', '=', self.prefix + member)])
        if len(temp) > 0:
          self.team1.member_ids += temp[0].id 

      self.arr_teams.append(self.team1)
    count = len(team.search([('active', '=', True)]))
    self.assertEqual(count, len(self.arr_teams), 'wrong count of teams')
   


  # commission calculation
  def calculate_commission(self, testcase):
    self.__setup_config(testcase)
    self.execute_calc(testcase.results)

  # setup configuration based on testcase
  def __setup_config(self, testcase):
    arr_agents = self.populate_user(testcase.users)
    arr_groups = self.__setup_scheme(testcase)
    arr_teams = self.__setup_teams(testcase.teams)
    self.__asign_teams(arr_groups, arr_teams, testcase)
    self.populate_hierarchy(arr_teams, testcase)
    self.__create_sales(testcase.salelines)


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


  #create group, schemes and tiers
  def __setup_scheme(self, testcase):
    arr_groups = []
    groups = testcase.groups
    dict_schemes = testcase.dict_schemes
    dict_tiers = testcase.dict_tiers
    

    o_schemes = self.env['commission.scheme']
    o_groups = self.env['commission.group']
    o_tiers = self.env['commission.tier']

    group_count = o_groups.search_count([])
    scheme_count = o_schemes.search_count([])
    tier_count = o_tiers.search_count([])
    expected_tiers = 0

    num_schemes = 0
    for group in groups:
      _group1 = o_groups.create ({
        'name' : group['name'],
        'active' : True
      })
      for name in group['schemes']:
        arr_tiers = []
        scheme = dict_schemes[name]
        for name in scheme['tiers']:
          tier = dict_tiers[name]
          arr_tiers.append((0, 0, tier))

        #check if scheme exist
        temp = o_schemes.search([('name', '=', scheme['name']), ('active', '=', True)])
        _scheme1 = None
        if len(temp) > 0:
          _scheme1 = temp[0]
        else:
          _scheme1 = o_schemes.create({
            'name' : scheme['name'],
            'active' : True,
            'product' : scheme['product'],
            'points' : scheme['points'],
            'aggregation' : scheme['aggregation'],
            'tier_ids' : arr_tiers
          })
          expected_tiers += len(arr_tiers)
          num_schemes += 1
          
        _group1.scheme_ids += _scheme1
      
      arr_groups.append(_group1)

    count = o_tiers.search_count([])
    self.assertEqual(expected_tiers, count - tier_count, 'setup schemes - wrong tier count')
    count = o_schemes.search_count([])
    self.assertEqual(num_schemes, count - scheme_count, 'setup schemes - wrong scheme count')
    count = o_groups.search_count([])
    self.assertEqual(len(groups), count - group_count, 'setup schemes - wrong group count')

    return arr_groups


  # call the calculation method
  def execute_calc(self, dict_results):
    self.env['commission'].calculate()

    o_summary = self.env['commission.summary']

    print(dict_results)

    for agent in list(dict_results.keys()):
      agent_id = 0
      if type(agent) == str:
        temp = self.env['res.users'].search([('login', '=', self.prefix + agent)])
        if len(temp) == 0:
          print('agent not found %s' % agent)
          continue
        agent_id = temp[0].id
      else:
        agent_id = agent
      result = o_summary.search([('sales_agent', '=', agent_id)], order='id desc')
      summary = []
      amount = 0
      if(len(result) == 0):
        amount = 0
      else:
        summary = result[0]
        amount = summary.amount

      print('number of summaries %d' % len(summary))      
      expected = dict_results.get(agent)
      print('expected amount %d  actual %d for agent %s' % (expected, amount, agent))

      if expected != amount:
        self.__dump_agent_info(agent_id)

      self.assertEqual(amount, expected, 'wrong amount for: ' +str(agent))


  # create teams for list of provided 
  def __setup_teams(self, arr_teams):
    arr_result = []
    o_team = self.env['crm.team']

    team_count = o_team.search_count([])

    # create teams for testcase
    for team in arr_teams:
      self.team1 = o_team.create({
        'name': self.prefix + team.get('name'),
        'active' : True,
        'use_opportunities' : False,
        'use_quotations' : False,
      })
      #assign members
      for member in team.get('members'):
        temp = self.env['res.users'].search([('login', '=', self.prefix + member)])
        if len(temp) > 0:
          self.team1.member_ids += temp[0] 

      arr_result.append(self.team1)

    count_after = o_team.search_count([])
    self.assertEqual(count_after - team_count, len(arr_teams), 'wrong team count')

    return arr_result


  # iterate through all teams and lookup team members in the dictionary
  def  __asign_teammember(self, arr_teams, dict_teammembers):
    for team in arr_teams:
      members = dict_teammembers.get(team.name)
      if members is not None:
        for member in members:
          user = self.env['res.users'].browse([member])
          team.member_ids += user


  #create sales lines, pick default company and first customer
  def __create_sales(self, salelines):
    o_sales = self.env['sale.order']
    o_user = self.env['res.users']
    customer = self.env['res.partner'].search([('customer', '=', True)])[0]
    o_product = self.env['product.product']
    line_count = self.env['sale.order.line'].search_count([])
    order_count = o_sales.search_count([])

    for saleline in salelines:
      product = o_product.browse([saleline.get('product_id')])[0]
      users = o_user.search([('login', '=', self.prefix + saleline.get('salesman_id'))])
      self.assertEqual(len(users), 1, 'sales line user not found')
      user_id = users[0].id

      _so1 = o_sales.create({
        'partner_id': customer.id,
        'partner_invoice_id': customer.id,
        'partner_shipping_id': customer.id,
        'order_line': [(0, 0, {'name': product.name, 'product_id': product.id, 
          'product_uom_qty': saleline.get('qty'), 
          'product_uom': product.uom_id.id,
          'price_unit': product.list_price, 
          'salesman_id' : user_id,
          'price_total' : saleline.get('price_total')
        })]
      })

      _so1.order_line.write({'salesman_id' : user_id})
      _so1.order_line.write({'price_total' : saleline.get('price_total')})


      sol = self.env['sale.order.line'].search([('product_id', '=', product.id), ('salesman_id', '=', user_id)], order='id desc')
      
      self.assertEqual(len(sol), 1, 'failed to create sales lines for ' + product.name)
      self.assertEqual(saleline['qty'], sol[0].product_uom_qty, 'wrong quantity')

      print('line product: %d amount: %d qty: %d agent %d' % (sol.product_id.id, sol.price_total, sol.product_uom_qty, sol.salesman_id))

    count = self.env['sale.order.line'].search_count([])
    self.assertEqual(len(salelines), count - line_count, 'create_sales - wrong line count')
    count = o_sales.search_count([])
    self.assertEqual(len(salelines), count - order_count, 'create_sales - wrong order count')


  # assign teams to the group
  def __asign_teams(self, arr_groups, arr_teams, testcase):
    tc_groups = testcase.groups
    dict_teams = dict()
    dict_groups = dict()
    o_group = self.env['commission.group']

    for team in arr_teams:
      dict_teams.update({team.name : team})
    
    for group in arr_groups:
      dict_groups.update({group.name : group})

    for group_name in tc_groups:
      team_names = group_name['teams']
      if team_names is None:
        continue
      for name in team_names:
        team = dict_teams.get(self.prefix + name)
        if team is None:
          continue
        group = dict_groups.get(group_name['name'])
        group.team_ids += team

      _groups = o_group.search([('name', '=', group_name.get('name')), ('active', '=', True)])
      expect = len(group_name.get('teams'))
      count = len(_groups[0].team_ids)
      self.assertEqual(count, expect, 'wrong team count for ' + str(group_name.get('name')) )


  def __dump_agent_info(self, agent_id):
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print('agent info for - %d' % agent_id)
    node = None
    isManager = False

    #team
    temp = self.env['res.users'].browse(agent_id)
    team = temp[0].sale_team_id
    print('agent name %s' % temp[0].login)
    print('member of team %s - %d'% (team.name, team.id))

    #see if manager
    temp = self.env['commission.hierarchy'].search([('manager', '=', agent_id)])
    if len(temp) > 0:
      node = temp[0]
      isManager = True
      print('manages this node: %s' % node.name)

    #find node team belongs to
    temp = self.env['commission.hierarchy'].search([('team_ids', '=', team.id)])
    if len(temp) > 0:
      node = temp[0]
      print('her team belongs to the following node: %s' % node.name)

    #reports
    arr_reports = []
    if node and isManager:
      nodes = self.env['commission.hierarchy'].child_nodes_deep(node.id)
      for _node in nodes:
        print('child nodes - %s' % _node.name)
        for _team in _node.team_ids:
          print('team - %s' % _team.name)
          arr_reports.extend(_team.member_ids)
      for _team in node.team_ids:
        print('team - %s' % _team.name)
        arr_reports.extend(_team.member_ids)

    print('reports - number %d - list %s' %(len(arr_reports), [user.login for user in arr_reports]) )

    #group
    temp = self.env['commission.group'].search([('team_ids', '=', team.id)])
    for group in temp:
      print('member of group: %s' % group.name)
      for scheme in group.scheme_ids:
        print('scheme applies: %s - product %s' % (scheme.name, scheme.product.name))
        for tier in scheme.tier_ids:
          print('tier start %d - amount %d - percent %d' % (tier.tier_start, tier.amount, tier.percent))
    
    #saleslines
    if isManager:
      ids = [user.id for user in arr_reports]
    else:
      ids = [agent_id]
      
    temp = self.env['sale.order.line'].search([('salesman_id', 'in', ids)])
    for line in temp:
      print('product %s - qty %d - amount %d' %(line.name, line.product_uom_qty, line.price_total))


    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')  
    