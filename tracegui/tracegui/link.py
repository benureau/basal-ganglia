class DrawnLink:
    """Handle the drawing routines for links"""

    def __init__(self, pre, post, cp=None):
        """
        :param pre, post:  pre and post units
        :param cp:         control points.
                           If None or empty, draw a straight line.
                           Else, it needs to contain a pair number of
                           coordinates, that define controls points
                           of the bezier curve. The first and last
                           coo define the tangents relative to the pre
                           and post position. The other pairs define
                           the tangents of additional control point,
                           placed as the average coordinate of the pair.
        """
        self.pre  = pre
        self.post = post
        if cp is None or len(cp) == 0:
            self._cp = None
        else:
            # transform cp coos into bezier() function quaternions
            assert len(cp) % 2 == 0
            cp = [list(p) for p in cp]
            for p in cp[:-1]:
                p[0] += pre.x
                p[1] += pre.y
            cp[-1][0] += post.x
            cp[-1][1] += post.y
            coos = [((pre.x, pre.y), cp[0])]
            for i in range(len(cp)//2 - 1):
                ax, ay = cp[2*i + 1]
                bx, by = cp[2*i + 2]
                middle = (ax + bx) / 2, (ay + by) / 2
                coos.append(((ax, bx), middle))
                coos.append((middle, (ay, by)))
            coos.append((cp[-1], (post.x, post.y)))
            self._cp = []
            for j in range(len(coos)//2):
                self._cp.append(coos[2*j] + coos[2*j + 1])

    def draw(self):
        noFill()
        if self._cp is None:
            line(self.pre.x, self.pre.y, self.post.x, self.post.y)
        else:
            for a, b, c, d in self._cp:
                bezier(a[0], a[1], b[0], b[1], c[0], c[1], d[0], d[1])



class AtomicLink:
    """A single unit-to-unit connection"""

    def __init__(self, pre, post, cp=None):
        self.pre  = pre
        self.post = post
        self.w    = 0.0
        self.drawer = DrawnLink(pre, post, cp=cp)

    def draw(self):
        a = int(100.0*(1-self.w))
        stroke(a, a, a, 128)
        strokeWeight(2.0)
        self.drawer.draw()


class Link:

    def __init__(self, kind, pre, post, n, groupmap, cp=None):
        self.kind = kind
        self.pre_name  = pre
        self.post_name = post
        self.pre_grp   = groupmap[pre]
        self.post_grp  = groupmap[post]
        self.n         = n
        self.cp        = cp

        self.create_atomics()
#        self.weights = [0.0 for _ in range(n)]

    def create_atomics(self):
        self.atomics = []
        if self.kind == 'OneToOne':
            assert self.pre_grp == self.post_grp
            for i in range(self.pre_grp.n):
                self.atomics.append(AtomicLink(self.pre_grp,  k,
                                               self.post_grp, k, cp=self.cp))

    def update(self, weights):
        assert len(weights) == self.n
        if self.kind in ('OneToOne'):
            for w, atomic in zip(weights, self.atomics):
                atomic.w = w

    def draw(self):
        for atomic in self.atomics:
            atomic.draw()
