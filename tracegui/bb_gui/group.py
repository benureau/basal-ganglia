import layout

class Unit:
    
    def __init__(self, xc, yc, act_fun, act_min, act_max, size=20):
        """Unit initialization
        
        xc:  x coordinate of center
        yc:  y coordinate of center
        w:   width (and height)
        """
        self.x = xc
        self.y = yc
        self.act_fun = act_fun
        self.act_min = act_min
        self.act_max = act_max
        if self.act_fun == 'Clamp':
            self.act_max = 100.0
        if self.act_fun == 'Sigmoid':
            self.act_max = 20.0

        self.size = size
        self.u = 0.0
    
    def draw(self):
        if self.u > self.act_max:
            print('max reached: {}'.format(self.u))
        stroke(0)
        fill(int(255*((self.act_max - self.u) / (self.act_max - self.act_min))))
        rect(self.x, self.y, self.size, self.size)

    def hover(self, x, y):
        """Return True if x, y is inside the unit area"""
        return (    self.x - self.size/2 <= x <= self.x + self.size/2
                and self.y - self.size/2 <= y <= self.y + self.size/2)


class Group:
    
    def __init__(self, name, domain, act_fun, act_min, act_max, n, size=40):
        self.name   = name
        self.domain = domain
        self.act_fun = act_fun
        self.act_min = act_min
        self.act_max = act_max
        self.n      = n
        self.u_size = int(size / 4 - 3.0)
        
        coo = layout.layout_abs[self.domain][self.name]
        self.center = layout.layout_posx[coo[0]], layout.layout_posx[coo[1]]
        
        # Unit creation
        pad = int(self.u_size/2+1)
        print(pad)
        self.units = []
        xc, yc = self.center
        if self.name == 'STR':
            xc += 2*pad
        if self.name == 'GPi':
            xc -= 2*pad
        x_offsets = [-3*pad, -pad, pad, 3*pad]
        y_offsets = [0] if self.n == 4 else [-3*pad, -pad, pad, 3*pad]
        for y_offset in y_offsets:
            for x_offset in x_offsets:
                unit = Unit(xc + x_offset, yc + y_offset, self.act_fun, self.act_min, self.act_max, size=self.u_size)
                self.units.append(unit)
            
    def update(self, Us):
        assert len(Us) == self.n
        for u, unit in zip(Us, self.units):
            unit.u = u
        
    def draw(self):
        # label
        strokeWeight(1.0)
        fill(0)
        textSize(16)
        text(self.name, self.center[0], self.center[1]-30)
        
        # unit
        for unit in self.units:
            unit.draw()