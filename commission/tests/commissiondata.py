
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
    agent_id1 = 689
    agent_id2 = 668
    prod_lp = 42
    prod_lm = 43
    prod_ins = 44
    arr_hierarchy = [
            ['Manager', ''],
            ['Super Central', 'Manager'],
            ['Super South', 'Manager'],
            ['Lead Central 1', 'Super Central'],
            ['Lead South 1', 'Super South']
        ]
    

    def __init__(self):
        self.agents = [self.agent_id1, self.agent_id2]

        group_agent = {
            'name' : 'group_agent',
            'schemes' : ['scheme_loan', 'scheme_ins'],
            'teams' : ['Lead Central 1', 'Lead South 1']
        }
        group_super = {
            'name' : 'group_super',
            'schemes' : ['scheme_5'],
            'teams' : ['Super Central', 'Super South']
        }
        group_manager = {
            'name' : 'group_manager',
            'schemes' : ['scheme_3'],
            'teams' : ['Manager']
        }

        self.groups = [group_agent, group_super, group_manager]

        scheme_loan = {
            'name' : 'scheme_loan',
            'points' : 5,
            'product' : self.prod_lp,
            'aggregation' : 'c',
            'tiers' : ['tier1', 'tier2', 'tier3']
        }

        scheme_ins = {
            'name' : 'scheme_ins',
            'points' : 2,
            'product' : self.prod_ins,
            'aggregation' : 'c',
            'tiers' : ['tier4']
        }

        scheme_5 = {
            'name' : 'scheme_5',
            'points' : 5,
            'product' : self.prod_lp,
            'aggregation' : 'c',
            'tiers' : ['tier10']
        }

        scheme_3 = {
            'name' : 'scheme_3',
            'points' : 5,
            'product' : self.prod_lp,
            'aggregation' : 'c',
            'tiers' : ['tier11']
        }

        self.schemes = [scheme_loan, scheme_ins, scheme_3, scheme_5]

        tier1 = {
            'type' : 'q',
            'tier_start' : 0,
            'tier_end' : 3,
            'amount' : 200000,
            'percent' : 0,
            'trigger' : 's'
        }

        tier2 = {
            'type' : 'q',
            'tier_start' : 4,
            'tier_end' : 6,
            'amount' : 300000,
            'percent' : 0,
            'trigger' : 's'
        }
        tier3 = {
            'type' : 'q',
            'tier_start' : 7,
            'tier_end' : 0,
            'amount' : 400000,
            'percent' : 0,
            'trigger' : 's'
        }
        tier4 = {
            'type' : 'v',
            'tier_start' : 0,
            'tier_end' : 0,
            'amount' : 0,
            'percent' : 5,
            'trigger' : 's'
        }
        tier10 = {
            'type' : 'v',
            'tier_start' : 0,
            'tier_end' : 3,
            'amount' : 0,
            'percent' : 5,
            'trigger' : 'c'
        }

        tier11 = {
            'type' : 'v',
            'tier_start' : 0,
            'tier_end' : 3,
            'amount' : 0,
            'percent' : 3,
            'trigger' : 'c'
        }

        self.dict_tiers = {
            'tier1' : tier1,
            'tier2' : tier2,
            'tier3' : tier3,
            'tier4' : tier4,
            'tier10': tier10,
            'tier11' : tier11
        }


        # leads name is key for agents assigne to team
        self.team_members = {
            'Lead Central 1' : self.agents
        }

        saleline1 = {
            'product_id' : self.prod_lp,
            'qty' : 5,
            'price_total' : 0,
            'salesman_id' : self.agent_id1
        }
        saleline2 = {
            'product_id' : self.prod_ins,
            'qty' : 1,
            'price_total' : 4000000,
            'salesman_id' : self.agent_id2
        }

        self.salelines = [saleline2, saleline1]

        self.results = {
            self.agent_id1 : 1500000,
            self.agent_id2 : 200000
        }

class TestCase2(TestCase1):
    def __init__(self):
        super().__init__()

        group_lead = {
            'name': 'group_lead',
            'schemes': ['scheme_20'],
            'teams': ['Lead Central 1'],
        }

        #reconfigure manager groups
        for group in self.groups:
            if group.get('name') == 'group_super':
                group.update({'schemes' : ['scheme_20']})
            if group.get('name') == 'group_manager':
                group.update({'schemes' : ['scheme_20']})
            
        self.groups.append(group_lead)

        scheme_20 = {
            'name' : 'scheme_20',
            'points' : 5,
            'product' : self.prod_lp,
            'aggregation' : 'c',
            'tiers' : ['tier21', 'tier22']
        }

        self.schemes.append(scheme_20)

        tier21 = {
            'type' : 'v',
            'tier_start' : 0,
            'tier_end' : 2000000,
            'amount' : 0,
            'percent' : 5,
            'trigger' : 'c'
        }

        tier22 = {
            'type' : 'v',
            'tier_start' : 2000001,
            'tier_end' : 0,
            'amount' : 0,
            'percent' : 4,
            'trigger' : 'c'
        }
        
        self.dict_tiers.update({'tier21' : tier21})
        self.dict_tiers.update({'tier22' : tier22})

        self.results.update({'Manager' : 75000})
        self.results.update({'Lead Central 1' : 75000})
        