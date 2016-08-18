import layout

class Unit:
    
    def __init__(self, xc, yc, u, size=8):
        """Unit initialization
        
        xc:  x coordinate of center
        yc:  y coordinate of center
        w:   width (and height)
        """
        self.x = xc
        self.y = yc
        self.size = size
        self.u = u
    
    def draw(self):
        stroke(100)
        fill(int(100*self.u))
        rect(self.x, self.y, self.size, self.size)


class Group:
    
    def __init__(self, name, domain, n, width=40):
        self.name   = name
        self.domain = domain
        self.n      = n
        
        coo = layout.layout_abs[self.domain][self.name]
        self.center = layout.layout_posx[coo[0]], layout.layout_posx[coo[1]]
        
        # Unit creation
        self.units = []
        xc, yc = self.center
        x_offsets = [-15, -5, 5, 15]
        y_offsets = [0] if self.n == 4 else [-15, -5, 5, 15]
        for y_offset in y_offsets:
            for x_offset in x_offsets:
                unit = Unit(xc + x_offset, yc + y_offset, 0.0, size=8)
                self.units.append(unit)
            
    def update(self, Us):
        assert len(Us) == self.n
        for u, unit in zip(Us, self.units):
            unit.u = u
        
    def draw(self):
        # label
        fill(0)
        textSize(16)
        text(self.name, self.center[0], self.center[1]-30)
        
        # unit
        for unit in self.units:
            unit.draw()
