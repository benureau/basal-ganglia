from group import Group


class Network:
    
    def __init__(self, desc, history):
        self.desc    = desc
        self.history = history
        self.trial   = 0
        self.dt_idx  = 0
        self.t       = 0.0
        
        self.groups = {}
        self.create_groups()
        
        self.trial_n = len(history)
        self.dt_n    = len(history[0][1])
        
    def create_groups(self):
        for msg_type, uid, name, kind, n in self.desc:
            assert msg_type == 'group'
            self.groups[uid] = Group(name, kind, n)
            
    def step_dt(self):
        dt, updates = self.history[self.trial][1][self.dt_idx]
        self.t += dt
        self.dt_idx += 1

        for uid, us in updates:
            self.groups[uid].update(us)
                                                
    def draw(self):
        for group in self.groups.values():
            group.draw()
        