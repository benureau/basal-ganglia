
class AtomicLink:
    """A single unit-to-unit connection"""

    def __init__(self, pre, post):
        self.pre  = pre
        self.post = post
        self.w    = 0.0
        
    def draw(self):
        fill(int(100*(self.u-0.25)/0.5))
        line(self.pre.x, self.pre.y, self.post.x, self.post.y


class Link:
    
    def __init__(self, kind, pre, post, n, self.groupmap,):
        self.kind = kind
        self.pre_name  = pre
        self.post_name = post
        self.pre_grp   = groupmap[pre]
        self.post_grp  = groupmap[post]
        self.n      = n

        self.create_atomics()
#        self.weights = [0.0 for _ in range(n)]

    def create_atomics(self):
        self.atomics = []
        if self.kind == 'OneToOne':
            for pre_u, post_u in zip(self.pre_grp.units, self.post_grp.units):
                self.atomics.append(AtomicLink(pre_u, post_u))
                
    def update(self, weights):
        assert len(weights) == self.n
        if self.kind in ('OneToOne'):
            for w, atomic in zip(weights, self.atomics):
                atomic.w = w
        
    def draw(self):
        return
        # for atomic in self.atomics:
        #     atomic.draw()     
        