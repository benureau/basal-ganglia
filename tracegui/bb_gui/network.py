from group import Group


class Network:
    """Network class: holds the Group and Link objects, manages time."""
    
    def __init__(self, desc, history):
        self.desc    = desc
        self.history = history
        self.trial   = 0
        self.k       = 0    # number of dt iteration (reset at trial start)
        self.t       = 0.0  # time elapsed (reset at trial start)
        
        self.groups   = {}
        self.groupmap = {}
        self.links    = {}
        self.create_network()
        
        self.trial_n = len(history)
        self.dt_n    = len(history[0][1])
        
    def create_network(self):
        """Read the description and create the network's object"""
        # first groups
        for msg in self.desc:
            if msg[0] == 'group':
                msg_type, uid, name, kind, n = msg
                grp = Group(name, kind, n)
                self.groups[uid] = grp
                self.groupmap[name] = grp

        # then, links, that need group to already exist.
        for msg in self.desc:
            if msg[0] == 'link':
                msg_type, uid, pre, post, kind, n = msg
                self.links[uid] = Link(kind, pre, post, n, self.groupmap) 
                    
    def step_dt(self):
        t, updates = self.history[self.trial][1][self.k]
        self.t = t
        self.k += 1

        for uid, us in updates:
            if uid in self.groups:
                self.groups[uid].update(us)
                                                
    def draw(self):
        for group in self.groups.values():
            group.draw()
        for link in self.links.values():
            link.draw()
        