
class CommissionData():
    prod_id1 = 1
    prod_id2 = 2
    agent_id1 = 688
    agent_id2 = 668
    team_id1 = 220
    team_id2 = 221
    lead_super_id1 = 215
    manager_team_id1 = 211
    prod_lp = 42
    prod_lm = 43
    prod_ins = 44
    
    tier1 = {
        'type' : 'q',
        'tier_start' : 0,
        'tier_end' : 2,
        'trigger' : 's',
        'amount' : 20
    }

    tier2 = {
        'type' : 'q',
        'tier_start' : 3,
        'tier_end' : 9,
        'trigger' : 's',
        'amount' : 30
    }

    tier3 = {
        'type' : 'q',
        'tier_start' : 0,
        'tier_end' : 2,
        'trigger' : 's',
        'amount' : 15
    }
    tier4 = {
        'type' : 'q',
        'tier_start' : 3,
        'tier_end' : 9,
        'trigger' : 's',
        'amount' : 30
    }

    scheme_a1 = {
        'name' : 'scheme1',
        'active' : True,
        'product' : prod_id1,
        'tier_ids' : ((0, 0, tier1), (0, 0, tier2))
    }

    scheme_a2 = {
        'name' : 'scheme2',
        'active' : True,
        'product' : prod_id2,
        'tier_ids' : ((0, 0, tier3), (0, 0, tier4))
    }
    # manager data
    tier5 = {
        'type' : 'v',
        'tier_start' : 0,
        'tier_end' : 99,
        'trigger' : 'c',
        'percent' : 5.0
    }

    scheme_m1 = {
        'name' : 'manager scheme',
        'active' : True,
        'product' : prod_id1,
        'tier_ids' : [(0, 0, tier5)]
    }

    tier6 = {
        'type' : 'v',
        'tier_start' : 0,
        'tier_end' : 99,
        'trigger' : 'c',
        'percent' : 10.0
    }

    scheme_m2 = {
        'name' : 'manager scheme2',
        'active' : True,
        'product' : prod_id2,
        'tier_ids' : [(0, 0, tier6)]
    }

    # user data
    arr_leads = ['HQ', 'Manager North', 'Manager South', 'North Lead 1', 'North Lead 2']
    arr_hierarchy = [
        ['HQ', ''],
        ['Manager North', 'HQ'],
        ['Manager South', 'HQ'],
        ['North Lead 1', 'Manager North'],
        ['North Lead 2', 'Manager North']
    ]

class TestCase1():
    prod_lp = 42
    prod_lm = 43
    prod_ins = 44
    

    def __init__(self):
        self.dict_tiers = dict()
        self.dict_schemes = dict()

        self.users = [
            'Manager',
            'Super north',
            'Super central',
            'Lead central 1',
            'Lead central 2',
            'DSA1',
            'DSA2'
        ]

        team1 = {
            'name' : 'DS1',
            'members' : ['DSA1']
        }
        team2 = {
            'name' : 'DS2',
            'members' : ['DSA2']
        }

        self.teams = [team1, team2]

        nodeHQ = {
            'name' : 'HQ',
            'parent' : '',
            'manager' : '',
            'teams' : ''
        }
        nodeSM = {
            'name' : 'SM',
            'parent' : 'HQ',
            'manager' : 'Manager',
            'teams' : ''
        }
        nodeSN = {
            'name' : 'Super north',
            'parent' : 'SM',
            'manager' : 'Super north',
            'teams' : ''
        }
        nodeSC = {
            'name' : 'Super central',
            'parent' : 'SM',
            'manager' : 'Super central',
            'teams' : ''
        }
        nodeLC1 = {
            'name' : 'Lead central 1',
            'parent' : 'Super central',
            'manager' : 'Lead central 1',
            'teams' : ['DS1', 'DS2']
        }
        nodeLC2 = {
            'name' : 'Lead central 2',
            'parent' : 'Super central',
            'manager' : 'Lead central 2',
            'teams' : ''
        }
        self.nodes = [nodeHQ, nodeSM, nodeSN, nodeSC, nodeLC1, nodeLC2]

        tier1 = {
            'type' : 'q',
            'tier_start' : 1,
            'tier_end' : 3,
            'amount' : 700000,
            'percent' : 0,
            'trigger' : 's'    
        }
        tier2 = {
            'type' : 'q',
            'tier_start' : 4,
            'tier_end' : 5,
            'amount' : 800000,
            'percent' : 0,
            'trigger' : 's'    
        }
        tier3 = {
            'type' : 'q',
            'tier_start' : 6,
            'tier_end' : 0,
            'amount' : 900000,
            'percent' : 0,
            'trigger' : 's'    
        }
        self.dict_tiers.update({'tier1' : tier1})
        self.dict_tiers.update({'tier2' : tier2})
        self.dict_tiers.update({'tier3' : tier3})
        scheme_lp = {
            'name' : 'loan insurance',
            'points' : 5,
            'product' : self.prod_lp,
            'aggregation' : 'c',
            'tiers' : ['tier1', 'tier2', 'tier3']
        }

        tier21 = {
            'type' : 'q',
            'tier_start' : 1,
            'tier_end' : 3,
            'amount' : 500000,
            'percent' : 0,
            'trigger' : 's'    
        }
        tier22 = {
            'type' : 'q',
            'tier_start' : 4,
            'tier_end' : 5,
            'amount' : 600000,
            'percent' : 0,
            'trigger' : 's'    
        }
        tier23 = {
            'type' : 'q',
            'tier_start' : 6,
            'tier_end' : 0,
            'amount' : 700000,
            'percent' : 0,
            'trigger' : 's'    
        }
        self.dict_tiers.update({'tier21' : tier21})
        self.dict_tiers.update({'tier22' : tier22})
        self.dict_tiers.update({'tier23' : tier23})
        scheme_lm = {
            'name' : 'loan no insurance',
            'points' : 5,
            'product' : self.prod_lm,
            'aggregation' : 'c',
            'tiers' : ['tier21', 'tier22', 'tier23']
        }

        self.dict_schemes.update({'scheme_lp' : scheme_lp}) 
        self.dict_schemes.update({'scheme_lm' : scheme_lm})

        group_ds1 = {
            'name': 'group_ds1',
            'schemes': ['scheme_lp', 'scheme_lm'],
            'teams': ['DS1'],
        }

        self.groups = [group_ds1]

        saleline1 = {
            'product_id' : self.prod_lp,
            'qty' : 6,
            'price_total' : 0,
            'salesman_id' : 'DSA1'
        }
        saleline2 = {
            'product_id' : self.prod_lm,
            'qty' : 1,
            'price_total' : 0,
            'salesman_id' : 'DSA1'
        }

        self.salelines = [saleline2, saleline1]

        self.results = {
            'DSA1' : 6100000,
        }
        

class TestCase2(TestCase1):
    def __init__(self):
        super().__init__()

        tier10 = {
            'type' : 'q',
            'tier_start' : 1,
            'tier_end' : 0,
            'amount' : 500000,
            'percent' : 0,
            'trigger' : 's'    
        }

        self.dict_tiers.update({'tier10' : tier10})

        scheme_lead = {
            'name' : 'leads',
            'points' : 5,
            'product' : self.prod_lp,
            'aggregation' : 'c',
            'tiers' : ['tier10']
        }

        self.dict_schemes.update({'scheme_lead' : scheme_lead}) 

        group_lead = {
            'name': 'group_lead',
            'schemes': ['scheme_lead'],
            'teams': ['lead'],
        }

        self.groups.append(group_lead)

        team_lead = {
            'name' : 'lead',
            'members' : ['Lead central 1', 'Lead central 2']
        }

        self.teams.append(team_lead)
       
        self.results.update({'Lead central 1' : 3000000})


class TestCase3(TestCase2):
    def __init__(self):
        super().__init__()
        
        self.users.append('DSA11')
        self.users.append('DSA12')
        self.users.append('Super south')
        self.users.append('Lead south 1')

        # add lead south 1 to team 'lead'
        for team in self.teams:
            if team.get('name') == 'lead':
                team.get('members').append('Lead south 1')

        team3 = {
            'name' : 'DS10',
            'members' : ['DSA11', 'DSA12']
        }

        self.teams.append(team3)

        nodeLS1 = {
            'name' : 'Lead south 1',
            'parent' : 'Super south',
            'manager' : 'Lead south 1',
            'teams' : ['DS10']
        }

        nodeSS = {
            'name' : 'Super south',
            'parent' : 'SM',
            'manager' : 'Super south',
            'teams' : ''
        }
        

        self.nodes.append(nodeLS1)
        self.nodes.append(nodeSS)

        #update DS group to add new DS10 team
        for group in self.groups:
            if group.get('name', '') == 'group_ds1':
                group['teams'].append(team3.get('name', ''))
        
        #commission scheme for supervisor and manager
        tier30 = {
            'type' : 'v',
            'tier_start' : 1,
            'tier_end' : 0,
            'amount' : 0,
            'percent' : 5,
            'trigger' : 'c'    
        }

        self.dict_tiers.update({'tier30' : tier30})

        scheme_manager = {
            'name' : 'managers',
            'points' : 5,
            'product' : self.prod_lp,
            'aggregation' : 'c',
            'tiers' : ['tier30']
        }

        self.dict_schemes.update({'scheme_manager' : scheme_manager}) 

        group_manager = {
            'name': 'group_manager',
            'schemes': ['scheme_manager'],
            'teams': ['manager'],
        }

        self.groups.append(group_manager)

        team_manager = {
            'name' : 'manager',
            'members' : ['Super south', 'Manager', 'Super north', 'Super central',]
        }

        self.teams.append(team_manager)

        tier35 = {
            'type' : 'v',
            'tier_start' : 100000,
            'tier_end' : 0,
            'amount' : 0,
            'percent' : 2,
            'trigger' : 's'    
        }

        self.dict_tiers.update({'tier35' : tier35})

        scheme_ins = {
            'name' : 'insurance',
            'points' : 2,
            'product' : self.prod_ins,
            'aggregation' : 'c',
            'tiers' : ['tier35']
        }

        self.dict_schemes.update({'scheme_insurance' : scheme_ins})

        group_ins = {
            'name': 'group_insurance',
            'schemes': ['scheme_insurance'],
            'teams': ['DS10'],
        }

        self.groups.append(group_ins)

        saleline30 = {
            'product_id' : self.prod_lp,
            'qty' : 1,
            'price_total' : 0,
            'salesman_id' : 'DSA11'
        }

        saleline31 = {
            'product_id' : self.prod_ins,
            'qty' : 0,
            'price_total' : 10000000,
            'salesman_id' : 'DSA12'
        }

        self.salelines.append(saleline30)
        self.salelines.append(saleline31)

        self.results.update({'DSA11' : 700000})
        self.results.update({'Super central' : 270000})
        self.results.update({'Super north' : 0})
        self.results.update({'Super south' : 35000})
        self.results.update({'Lead south 1' : 500000})
        self.results.update({'Manager' : 305000})
        self.results.update({'DSA12' : 20000})
        self.results.update({'DSA2' : 0})
