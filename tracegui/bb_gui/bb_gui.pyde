import pickle

import network
import layout


net = None

def load_data(filename):
    """Load data"""
    with open(filename, 'r') as f:
        data = pickle.load(f)
    return data


def setup():
    """Setup the network"""
    global net
    size(800, 800)
    print(width)
    frameRate(30)
    textAlign(CENTER)
    rectMode(CENTER)

    layout.generate_pos(125, 125)

    filename = "/Users/fabien/research/renc/projects/basal/basal-ganglia/experiments/data/guthrie-symmetry.trace"
    desc, history = load_data(filename)
    net = network.Network(desc, history)
    net.step_dt()

def draw():
    """Draw the network and advance time"""
    background(255)
    net.draw()
    if frameCount % 1 == 0:
        if net.k < net.dt_n:
            net.step_dt()
            #print(net.t)
