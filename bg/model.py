# -----------------------------------------------------------------------------
# Copyright (c) 2016, Nicolas P. Rougier
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import os
import json
import numpy as np
from .dana import *

class Model(object):

    def __init__(self, filename="default-model.json"):
        self.filename = filename
        with open(filename) as f:
            self.parameters = json.load(f)
        self.trace = None
        self.setup()


    def setup(self):
        _ = self.parameters

        clamp = Clamp(min=_["clamp"]["Vmin"],
                      max=_["clamp"]["Vmax"])
        sigmoid = Sigmoid(Vmin = _["sigmoid"]["Vmin"],
                          Vmax = _["sigmoid"]["Vmax"],
                          Vh   = _["sigmoid"]["Vh"],
                          Vc   = _["sigmoid"]["Vc"])

        def weights(shape):
            Wmin = _["weight"]["min"]
            Wmax = _["weight"]["max"]
            noise= _["weight"]["noise"]
            W = np.random.normal((Wmax+Wmin)/2, scale=noise, size=shape)
            return np.clip(W, Wmin, Wmax)

        self._structures = {
            "CTX" : { "cog" : Group( 4, activation=clamp),
                      "mot" : Group( 4, activation=clamp),
                      "ass" : Group(16, activation=clamp) },
            "STR" : { "cog" : Group( 4, activation=sigmoid),
                      "mot" : Group( 4, activation=sigmoid),
                      "ass" : Group(16, activation=sigmoid) },
            "STN" : { "cog" : Group( 4, activation=clamp),
                      "mot" : Group( 4, activation=clamp) },
            "GPi" : { "cog" : Group( 4, activation=clamp),
                      "mot" : Group( 4, activation=clamp) },
            "THL" : { "cog" : Group( 4, activation=clamp),
                      "mot" : Group( 4, activation=clamp) },
        }
        for name, structure in self._structures.items():
            for group in structure.values():
                group.tau  = _[name]["tau"]
                group.rest = _[name]["rest"]
                group.noise = _[name]["noise"]
        self._structures["value"] = np.zeros(4) # FIXME: verify that.

        CTX = self["CTX"]
        STR = self["STR"]
        STN = self["STN"]
        GPi = self["GPi"]
        THL = self["THL"]
        self["value"][...] = _["RL"]["init"]

        self._groups = (CTX["cog"], CTX["mot"], CTX["ass"],
                        STR["cog"], STR["mot"], STR["ass"],
                        STN["cog"], STN["mot"],
                        GPi["cog"], GPi["mot"],
                        THL["cog"], THL["mot"] )

        W1 = (2 * np.eye(4) - np.ones((4, 4))).ravel()
        W2 = (2 * np.eye(16) - np.ones((16, 16))).ravel()

        self._links = {
            "CTX:cog -> STR:cog" :
                OneToOne(CTX["cog"]["U"], STR["cog"]["Isyn"], weights(4), 0.0),
            "CTX:cog -> STR:ass" :
                CogToAss(CTX["cog"]["U"], STR["ass"]["Isyn"], weights(4), 0.0),
            "CTX:cog -> STN:cog" :
                OneToOne(CTX["cog"]["U"], STN["cog"]["Isyn"], np.ones(4), 0.0),
            "CTX:cog -> THL:cog" :
                OneToOne(CTX["cog"]["U"], THL["cog"]["Isyn"], np.ones(4), 0.0),

            "CTX:mot -> STR:mot" :
                OneToOne(CTX["mot"]["U"], STR["mot"]["Isyn"], weights(4), 0.0),
            "CTX:mot -> STR:ass" :
                MotToAss(CTX["mot"]["U"], STR["ass"]["Isyn"], weights(4), 0.0),
            "CTX:mot -> STN:mot" :
                OneToOne(CTX["mot"]["U"], STN["mot"]["Isyn"], np.ones(4), 0.0),
            "CTX:mot -> THL:mot" :
                OneToOne(CTX["mot"]["U"], THL["mot"]["Isyn"], np.ones(4), 0.0),

            "CTX:ass -> STR:ass" :
                OneToOne(CTX["ass"]["U"], STR["ass"]["Isyn"], weights(16), 0.0),

            "STR:cog -> GPi:cog" :
                OneToOne(STR["cog"]["U"], GPi["cog"]["Isyn"], np.ones(4), 0.0),
            "STR:mot -> GPi:mot" :
                OneToOne(STR["mot"]["U"], GPi["mot"]["Isyn"], np.ones(4), 0.0),
            "STR:ass -> GPi:cog" :
                AssToCog(STR["ass"]["U"], GPi["cog"]["Isyn"], np.ones(4), 0.0),
            "STR:ass -> GPi:mot" :
                AssToMot(STR["ass"]["U"], GPi["mot"]["Isyn"], np.ones(4), 0.0),

            "STN:cog -> GPi:cog" :
                OneToAll(STN["cog"]["U"], GPi["cog"]["Isyn"], np.ones(4), 0.0),
            "STN:mot -> GPi:mot" :
                OneToAll(STN["mot"]["U"], GPi["mot"]["Isyn"], np.ones(4), 0.0),

            "GPi:cog -> THL:cog" :
                OneToOne(GPi["cog"]["U"], THL["cog"]["Isyn"], np.ones(4), 0.0),
            "GPi:mot -> THL:mot" :
                OneToOne(GPi["mot"]["U"], THL["mot"]["Isyn"], np.ones(4), 0.0),

            "THL:cog -> CTX:cog" :
                OneToOne(THL["cog"]["U"], CTX["cog"]["Isyn"], np.ones(4), 0.0),
            "THL:mot -> CTX:mot" :
                OneToOne(THL["mot"]["U"], CTX["mot"]["Isyn"], np.ones(4), 0.0),

            "CTX:mot -> CTX:mot":
                AllToAll(CTX["mot"]["U"], CTX["mot"]["Isyn"], W1, 0.0),
            "CTX:cog -> CTX:cog":
                AllToAll(CTX["cog"]["U"], CTX["cog"]["Isyn"], W1, 0.0),
            "CTX:ass -> CTX:ass":
                AllToAll(CTX["ass"]["U"], CTX["ass"]["Isyn"], W2, 0.0),
            "CTX:ass -> CTX:cog":
                AssToCog(CTX["ass"]["U"], CTX["cog"]["Isyn"], np.ones(4), 0.0),
            "CTX:ass -> CTX:mot":
                AssToMot(CTX["ass"]["U"], CTX["mot"]["Isyn"], np.ones(4), 0.0),
            "CTX:cog -> CTX:ass":
                CogToAss(CTX["cog"]["U"], CTX["ass"]["Isyn"], weights(4), 0.0),
            "CTX:mot -> CTX:ass":
                MotToAss(CTX["mot"]["U"], CTX["ass"]["Isyn"], weights(4), 0.0)
        }
        for key, link in self._links.items():
            if key in _["gain"].keys():
                link.gain = _["gain"][key]

        if self.trace is not None:
            self.trace.initialize_model(self)



    def __getitem__(self, key):
        try:
            return self._structures[key]
        except KeyError:
            return self._links[key]


    def flush(self):
        for group in self._groups:
            group.flush()

    def iterate(self, dt):
        if self.trace is not None:
            self.trace.dt_update(dt)

        # Flush all connections
        for link in self._links.values():
            link.flush()

        # Propagate activities
        for link in self._links.values():
            link.propagate()
            if self.trace is not None:
                self.trace.link_update(link)

        # Evaluate activity
        for group in self._groups:
            group.evaluate(dt)
            if self.trace is not None:
                self.trace.group_update(group)


    def process(self, task, trial, stop=True, debug=False, model=None):
        if self.trace is not None:
            self.trace.new_trial(trial)

        _ = self.parameters

        # Flush all activities
        self.flush()

        dt = _["time"]["dt"]
        settling = _["time"]["settling"]
        duration = _["time"]["duration"]

        # Settling phase (500ms)
        for i in range(int(settling/dt)):
            self.iterate(dt)

        # Trial setup
        V     = _["input"]["potential"]
        noise = _["input"]["noise"]
        self["CTX"]["cog"]["Iext"] = V * trial["cog"] * np.random.normal(1, noise, 4)
        self["CTX"]["mot"]["Iext"] = V * trial["mot"] * np.random.normal(1, noise, 4)
        self["CTX"]["ass"]["Iext"] = V * trial["ass"].ravel() * np.random.normal(1, noise, 16)

        # Trial process (max 2500ms)
        decision = False

        for i in range(int(duration/dt)):
            # Compute activities
            self.iterate(dt)

            # Test if a motor decision has been made
            if stop and self["CTX"]["mot"].delta > _["threshold"]:
                decision = True
                break

        # Response time
        RT = i * dt

        if decision is False:
            # print("  No decision")
            reward, cue, best = task.process(trial, -1, RT, debug=debug, model=model)
        else:
            choice = np.argmax(self["CTX"]["mot"]["U"])
            # actual_cue = np.argmax(self["CTX"]["cog"]["U"])
            reward, cue, best = task.process(trial, choice, RT, debug=debug, model=model)
            # print("  Motor decision: %d, Chosen cue: %d, Actual cue: %d" % (choice,cue, actual_cue))

            # Constants
            Wmin = _["weight"]["min"]
            Wmax = _["weight"]["max"]

            # Reinforcement learning
            alpha_critic = _["RL"]["alpha"]
            error = reward - self["value"][cue]
            self["value"][cue] += alpha_critic * error

            LTP   = _["RL"]["LTP"] # long-term potentiation
            LTD   = _["RL"]["LTD"] # long-term depression
            alpha_actor = LTP if error > 0 else LTD
            dw = alpha_actor * error * self["STR"]["cog"]["U"][cue]
            W = self["CTX:cog -> STR:cog"].weights
            W[cue] += dw * (Wmax - W[cue]) * (W[cue] - Wmin)
            W[cue] = np.clip(W[cue], Wmin, Wmax)

            # Hebbian learning
            # This is the chosen cue by the model (may be different from the actual cue)
            cue = np.argmax(self["CTX"]["cog"]["U"])

            LTP   = _["Hebbian"]["LTP"]
            dw = LTP * self["CTX"]["cog"]["U"][cue] * sum(self["CTX"]["ass"]["U"].reshape(4,4)[cue])
            W = self["CTX:cog -> CTX:ass"].weights
            W[cue] += dw * (Wmax - W[cue]) * (W[cue] - Wmin)
            W[cue] = np.clip(W[cue], Wmin, Wmax)
