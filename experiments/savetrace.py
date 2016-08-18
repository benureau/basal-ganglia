import pickle


class TracedGroup:

    def __init__(self, name, kind, group):
        self.name = name
        self.kind = kind
        self.group = group

    def update(self):
        return [float(u) for u in self.group.U]


class TracedLink:

    def __init__(self, name, link):
        pre, post = name.split(' -> ')
        self.pre, self.post = pre.split(':'), post.split(':')
        self.kind = type(link).__name__
        self.link = link

    def update(self):
        return [float(w) for w in self.link.weights]


class Trace:
    """Records the whole history of the network"""

    def __init__(self, filename):
        self.filename = filename
        self.trial_count = 0
        self.res = 5    # only keep one in every res dt iteration
        self.k   = 0    # number of dt iteration (reset at trial start)
        self.t   = 0.0  # time elapsed (reset at trial start)

    def initialize_model(self, model):
        self.model = model

        self.groups = {}
        for str_name, structure in model._structures.items():
            if str_name != 'value':
                for str_kind, group in structure.items():
                    self.groups[id(group)] = TracedGroup(str_name, str_kind, group)

        self.links = {}
        for link_name, link in model._links.items():
            self.links[id(link)] = TracedLink(link_name, link)

        self.history = []

    def description(self):
        desc = []
        for uid, group in self.groups.items():
            desc.append(('group', uid, group.name, group.kind, len(group.group.U)))
        return desc

    def new_trial(self, trial):
        self.history.append((self.trial_count, []))
        self.trial_count += 1
        self.k, self.t = 0, 0.0

    def dt_update(self, dt):
        if self.k % self.res == 0:
            self.history[-1][1].append((float(self.t), []))
        self.k += 1
        self.t += dt

    def group_update(self, group):
        if self.k % self.res == 0 and id(group) in self.groups:
            self.history[-1][1][-1][1].append((id(group), self.groups[id(group)].update()))

    def link_update(self, link):
        if self.k % self.res == 0 and id(link) in self.links:
            self.history[-1][1][-1][1].append((id(link), self.links[id(link)].update()))

    def save(self):
        content = (self.description(), self.history)
        with open(self.filename, 'wb') as fd:
            pickle.dump(content, fd, protocol=2) # python 2 compatibility
