
class Link:
    
    def __init__(self, kind, pre, post, n, self.groupmap,):
        self.kind = kind
        self.pre_name  = pre
        self.post_name = post
        self.pre_grp   = groupmap[pre]
        self.post_grp  = groupmap[post]
        self.n      = n
                
        self.weights = [0.0 for _ in range(n)]
    
    def update(self, weights):
        assert len(weights) == self.n
        self.weights = weights
        
    def draw(self):
        return
        # if self.kind == 'OneToOne':
        