import consul

consulCilent = consul.Consul(host='139.162.2.128', port=8301)

consulCilent.kv.get('dd')

consulCilent.kv.put('test1', 'test2')
consulCilent.kv.put('test1/test2', 'test3')

rules = """
    key "" {
        policy = "read"
    }
    key "private/" {
        policy = "deny"
    }
"""

consulCilent.acl.create(rules=rules)

