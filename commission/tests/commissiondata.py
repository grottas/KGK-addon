
class CommissionData():
    prod_id1 = 1
    prod_id2 = 2
    agent_id1 = 688
    agent_id2 = 668
    team_id1 = 220
    team_id2 = 221
    lead_super_id1 = 215
    manager_team_id1 = 211
    
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