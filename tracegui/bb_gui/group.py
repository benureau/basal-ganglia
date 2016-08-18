import layout

class Group:
    
    def __init__(self, name, domain, n, width=40):
        self.name   = name
        self.domain = domain
        self.n      = n
        
        coo = layout.layout_abs[self.domain][self.name]
        self.center = layout.layout_posx[coo[0]], layout.layout_posx[coo[1]]
        
        self.us = [0.0 for _ in range(n)]
    
    def update(self, Us):
        assert len(Us) == self.n
        self.us = Us
        
    def draw(self):
        xc, yc = self.center
        # label
        fill(0)
        textSize(16)
        text(self.name, xc, yc-30)
        
        # units        
        x_offsets = [-15, -5, 5, 15]
        y_offsets = [0] if self.n == 4 else [-15, -5, 5, 15]
        u_iter = iter(self.us)
        for y_offset in y_offsets:
            for x_offset in x_offsets:
                u = next(u_iter)
                stroke(100)
                fill(int(100*u))
                rect(xc + x_offset, yc + y_offset, 8, 8)