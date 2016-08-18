import pickle


class TracedGroup:

    def __init__(self, name, kind, group):
        self.name = name
        self.kind = kind
        self.group = group
        self.history = []

    def update(self):
        return [float(u) for u in self.group.U]


class Trace:
    """Records the whole history of the network"""

    def __init__(self, filename):
        self.filename = filename
        self.trial_count = 0

    def initialize_model(self, model):
        self.model = model

        self.groups = {}
        for str_name, structure in model._structures.items():
            if str_name != 'value':
                for str_kind, group in structure.items():
                    self.groups[id(group)] = TracedGroup(str_name, str_kind, group)

        self.history = []

    def description(self):
        desc = []
        for uid, group in self.groups.items():
            desc.append(('group', uid, group.name, group.kind, len(group.group.U)))
        return desc

    def new_trial(self, trial):
        self.history.append((self.trial_count, []))
        self.trial_count += 1

    def dt_update(self, dt):
        self.history[-1][1].append((float(dt), []))

    def group_update(self, group):
        if id(group) in self.groups:
            self.history[-1][1][-1][1].append((id(group), self.groups[id(group)].update()))

    def link_update(self, link):
        pass

    def save(self):
        content = (self.description(), self.history)
        with open(self.filename, 'wb') as fd:
            pickle.dump(content, fd, protocol=2) # python 2 compatibility
