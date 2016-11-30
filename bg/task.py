# -----------------------------------------------------------------------------
# Copyright (c) 2016, Nicolas P. Rougier, Meropi Topalidou
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
"""
Generic bandit task using at most 4 cues at 4 different positions.

A task is made of n trials.
A trial is fully described by 4 arrays:

cog:   4 items, indicate which cues are present (A,B,C,D)
mot:   4 items, indicate where cues are present (1,2,3,4)
ass: 4x4 items, indicate the position of cues (A1, A2,..., D3, D4)
rew:   4 items, indicate the reward probability associated with each
                cue for this specific trial

Example
-------

A is in position 3, reward probablity is a
C is in position 2, reward probablity is c
B is not present, D is not present

cue :  [1, 0, 1, 0]
pos :  [0, 1, 1, 0]
rwd :  [a, b, c, d]
ass : [[0, 0, 0, 0],
       [0, 0, 0, 0],
       [0, 0, 1, 0],
       [1, 0, 0, 0]]

Usage
-----

task = Task(n=120)

for trial in task:
    choice = ...
    RT = ...
    reward, best = task.process(trial, choice, RT)
"""
import numpy as np


class Task(object):
    """ A two-armed bandit task """

    record_dtype = np.dtype([("choice", float, 1),
                             ("cue",    float, 1),
                             ("best",   float, 1),
                             ("valid",  float, 1),
                             ("RT",     float, 1),
                             ("reward", float, 1),
                             # These values must be collected from the model
                             ("value",  float, 4),
                             ("CTX:cog -> CTX:ass", float, 4),
                             ("CTX:cog -> STR:cog", float, 4)])

    trial_dtype = np.dtype([("mot", float,  4),
                            ("cog", float,  4),
                            ("ass", float, (4,4)),
                            ("rwd", float,  4),
                            ("rnd", float,  1)])

    def __init__(self, parameters):
        self.parameters = parameters
        self.session    = self.parameters["session"]

    def length(self):
        """Return the total number of trials summed across all blocks"""
        return sum(self.parameters[blockname]['n_trial']
                   for blockname in self.session)

    def block(self, blockname):
        """Create the datastructure and trials for a given block"""
        block = self.parameters[blockname]

        # Build corresponding arrays
        self.cursor  = 0 # current trial # FIXME: brittle, non-dry coding
        self.trials  = np.zeros(block['n_trial'], dtype=self.trial_dtype)
        self.records = np.zeros(block['n_trial'], dtype=self.record_dtype)

        # We draw all reward random probabilities at once (faster)
        self.trials['rnd'] = np.random.uniform(0, 1, block['n_trial'])

        n_cues = block.get("n_cue", 2) # defaults to 2 cues
        cue_options = range(len(block["cue"]))
        pos_options = range(len(block["pos"]))

        # Getting cue and position probabilities
        P_cue = np.array(block["cue"], float)
        P_cue = P_cue / np.sum(P_cue) # normalizing
        P_pos = block["pos"]
        P_pos = P_pos / np.sum(P_pos)

        for trial in self.trials:
            # Drawing cues and positions
            cues_idx = np.random.choice(cue_options, size=n_cues, replace=False, p=P_cue)
            pos_idx  = np.random.choice(pos_options, size=n_cues, replace=False, p=P_pos)

            # Setting the trial values
            trial["cog"][cues_idx] = 1
            trial["mot"][pos_idx]  = 1
            for c, p in zip(cues_idx, pos_idx):
                trial["ass"][c, p] = 1
            trial["rwd"] = block["rwd"]

        return self.trials

    def process(self, trial, choice, RT=0.0, model=None, debug=False):
        """
        Process a (motor) choice and return the reward and whether this was the
        best choice for this trial.
        """

        # Do we have a choice at least ?
        if choice < 0:
            # No cue chosen
            cue = -1
            # Choice is not valid
            valid = False
            # Not the best move
            best = False
            # No choice, no reward
            reward = 0.0
        else:
            # Check if choice is valid
            valid = (trial["mot"][choice] == 1.0)
            # Get cue corresponding to motor choice
            cues = np.nonzero(trial["ass"][:,choice])[0]
            assert(len(cues) == 1)
            cue = cues[0]
            # Get whether this is the best choice
            present_rwd = trial["cog"]*trial["rwd"]
            best = max(present_rwd) == present_rwd[cue]
            # Get actual reward
            reward = trial["rnd"] < trial["rwd"][cue]

        # Record everything
        self.records[self.cursor]["choice"] = choice
        self.records[self.cursor]["cue"]    = cue
        self.records[self.cursor]["best"]   = best
        self.records[self.cursor]["valid"]  = valid
        self.records[self.cursor]["RT"]     = RT
        self.records[self.cursor]["reward"] = reward
        if model is not None:
            self.records[self.cursor]["value"] = model["value"]
            self.records[self.cursor]["CTX:cog -> CTX:ass"] = model["CTX:cog -> CTX:ass"].weights
            self.records[self.cursor]["CTX:cog -> STR:cog"] = model["CTX:cog -> STR:cog"].weights


        if debug:
            if best: s = " (+)"
            else:    s = " (-)"
            print("Trial %d%s" % ((self.cursor+1), s))
            P = self.records[:self.cursor+1]["best"]
            print("  Mean performance: %.3f" % np.array(P).mean())
            R = self.records[:self.cursor+1]["reward"]
            print("  Mean reward:      %.3f" % np.array(R).mean())

        self.cursor += 1
        return reward, cue, best


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    task = Task()

    for trial in task:
        # Best choice
        best_cue = np.argmax(trial["cog"]*trial["rwd"])
        choice = np.argmax(trial["ass"][best_cue])
        # Random choice
        # n = len(trial["mot"]) - 1 - np.random.randint(0,trial["mot"].sum()-1)
        # choice = np.argsort(trial["mot"])[n]
        # Process choice
        reward, cue, best = task.process(trial, choice, debug=True)
