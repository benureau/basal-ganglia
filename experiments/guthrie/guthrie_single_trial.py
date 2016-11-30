# -----------------------------------------------------------------------------
# Copyright (c) 2016, Nicolas P. Rougier
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt

from bg.task import Task
from bg.model import Model
import bg


seed = np.random.randint(0,1000)
np.random.seed(seed)

model_filename = "guthrie_model.json"
task_filename  = "guthrie_task.json"
model = Model(bg.utils.load_json('.', model_filename))
task = Task(bg.utils.load_json('.', task_filename))

print("-"*30)
print("Seed:     %d" % seed)
print("Model:    %s" % model_filename)
print("Task:     %s" % task_filename)
print("-"*30)


trial = task.block('block 1')[0]
model.process(task, trial, stop=False, debug=False)

cog = model["CTX"]["cog"].history[:3000]
mot = model["CTX"]["mot"].history[:3000]


fig = plt.figure(figsize=(12,5))
plt.subplots_adjust(bottom=0.15)

duration = 3.0
timesteps = np.linspace(0, duration, 3000)

fig.patch.set_facecolor('.9')
ax = plt.subplot(1,1,1)

plt.plot(timesteps, cog[:,0], c='r', label="Cognitive Cortex")
plt.plot(timesteps, cog[:,1], c='r')
plt.plot(timesteps, cog[:,2], c='r')
plt.plot(timesteps, cog[:,3], c='r')
plt.plot(timesteps, mot[:,0], c='b', label="Motor Cortex")
plt.plot(timesteps, mot[:,1], c='b')
plt.plot(timesteps, mot[:,2], c='b')
plt.plot(timesteps, mot[:,3], c='b')

plt.title("Single trial")
plt.xlabel("Time (seconds)")
plt.ylabel("Activity (Hz)")
plt.legend(frameon=False, loc='upper left')
plt.xlim(0.0,duration)
plt.ylim(-10.0,60.0)
plt.xticks([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0],
           ['0.0','0.5\n(Trial start)','1.0','1.5', '2.0','2.5','3.0'])
plt.savefig("data/single-trial-guthrie.pdf")
plt.show()
