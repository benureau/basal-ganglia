# -----------------------------------------------------------------------------
# Copyright (c) 2016, Nicolas P. Rougier
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import io
import sys
import json
import time
import os
import argparse
import multiprocessing

import numpy as np
from tqdm import tqdm

from . import savetrace
from . import utils
from .task import Task
from .model import Model


def session(exp):
    """Default session function

    Run the task, by iterating over all trials.
    """
    exp.model.setup()
    for trial in exp.task:
        exp.model.process(task=exp.task, trial=trial, model=exp.model)
    return exp.task.records


class Experiment(object):
    def __init__(self, model, task, result, report, n_session, n_block, changes=None,
                       seed=None, rootdir=None, verbose=True, trace_file=None):
        """Initialize an experiment.

        rootdir: root directory for the `model`, `task`, `result` and `report`
                 filepath. If None, defaults to the directory of the main script.
        """
        self.verbose = verbose
        self.rootdir = rootdir
        if rootdir is None:
            from __main__ import __file__ as __mainfile__
            self.rootdir = os.path.dirname(__mainfile__)

        self.model_file  = utils.filepath(self.rootdir, model)
        self.task_file   = utils.filepath(self.rootdir, task)
        self.result_file = utils.filepath(self.rootdir, result)
        self.report_file = utils.filepath(self.rootdir, report)
        self.n_session   = n_session
        self.n_block     = n_block
        self.seed        = seed

        self.trace = None
        if trace_file is not None:
            tracepath = utils.filepath(self.rootdir, trace_file)
            if not os.path.isdir(os.path.dirname(tracepath)):
                os.makedirs(os.path.dirname(tracepath))
            self.trace = savetrace.Trace(tracepath)

        if self.seed is None:
            self.seed = np.random.randint(0, 1000)
        np.random.seed(seed)

        # Instanciating model and task
        model_params = utils.load_json(self.rootdir, model)
        task_params = utils.load_json(self.rootdir, task)
        if changes is not None:
            changes = utils.load_json(self.rootdir, changes)
            if 'model' in changes:
                model_params = utils.update_json(model_params, changes['model'])
            if 'task'  in changes:
                task_params = utils.update_json(task_params, changes['task'])

        self.model = Model(model_params)
        self.task  = Task(task_params)

        self.n_trial = len(self.task)

    def msg(self, s):
        """Print if verbose is True"""
        if self.verbose:
            print(s)

    def run(self, session, desc="", save=True, force=False):

        # Command line argument parsing for the --force switch
        parser = argparse.ArgumentParser()
        parser.add_argument("--force", action='store_true')
        args = parser.parse_known_args()[0]
        force = force or args.force

        if os.path.exists(self.result_file) and not force:
            print("Reading report (%s)" % self.report_file)
            self.read_report()

        self.msg("-"*30)
        self.msg("Seed:     {}".format(self.seed))
        self.msg("Model:    {}".format(self.model_file))
        self.msg("Task:     {}".format(self.task_file))
        self.msg("Result:   {}".format(self.result_file))
        self.msg("Report:   {}".format(self.report_file))
        n = self.n_session * self.n_block * self.n_trial
        self.msg("Sessions: {} ({} trials)".format(self.n_session, n))
        self.msg("-"*30)

        if not os.path.exists(self.result_file) or force:
            index = 0
            records = np.zeros((self.n_session, self.n_block, self.n_trial),
                               dtype=self.task.records.dtype)

            n_workers = multiprocessing.cpu_count() # depends on your hardware
            pool = multiprocessing.Pool(n_workers)
            # different seed for different sessions
            seeds = np.random.randint(0, 1000000000, size=self.n_session)
            traces = (self.trace,) + (len(seeds)-1)*(None,)
            session_args = [(self, session, seed, trace)
                            for seed, trace in zip(seeds, traces)]

            # # non-multiprocessing version (for debugging)
            # for args in session_args:
            #     result = self.session_init(args)
            #     records[index] = result
            #     index += 1
            for result in tqdm(pool.imap(self.session_init, session_args),
                               total=self.n_session, leave=True, desc=desc,
                               unit="session", disable=not self.verbose,
                               file=sys.stdout):
                records[index] = result
                index += 1
            pool.close()

            if save:
                self.msg("Saving results ({})".format(self.result_file))
                if not os.path.isdir(os.path.dirname(self.result_file)):
                    os.makedirs(os.path.dirname(self.result_file))
                np.save(self.result_file, records)
                if not os.path.isdir(os.path.dirname(self.report_file)):
                    os.makedirs(os.path.dirname(self.report_file))
                self.msg("Writing report ({})".format(self.report_file))
                self.write_report()
                self.msg("-"*30)
        else:
            self.msg("Loading previous results")
            self.msg(' -> "{}"'.format(self.result_file))
            records = np.load(self.result_file)
            self.msg("-"*30)

        return records

    def session_init(cls, args):
        """Initialize the random seed of a process and run a session."""
        experiment, session, seed, trace = args
        experiment.model.trace = trace
        np.random.seed(seed)
        results = session(experiment)
        if trace is not None:
            trace.save()
        return results

    def write_report(self):
        report = { "seed"      : self.seed,
                   "n_session" : self.n_session,
                   "n_block"   : self.n_block,
                   "n_trial"   : self.n_trial,
                   "task"      : self.task.parameters,
                   "model"     : self.model.parameters }
        with io.open(self.report_file, 'w', encoding='utf8') as fp:
            json.dump(report, fp, indent=4, ensure_ascii=False)

    def read_report(self):
        with io.open(self.report_file, 'r', encoding='utf8') as fp:
            report = json.load(fp)
        self.seed      = report["seed"]
        self.n_session = report["n_session"]
        self.n_block   = report["n_block"]
        self.n_trial   = report["n_trial"]
