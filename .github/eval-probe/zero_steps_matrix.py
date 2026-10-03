"""Evaluator-only probe: pinned behaviour of set_timesteps step counts. Contains no fix."""
import sys

import diffusers
import torch
from diffusers import DDPMParallelScheduler, DDPMScheduler

print("python", sys.version.split()[0], "| torch", torch.__version__, "cuda", torch.version.cuda)
print("diffusers from", diffusers.__file__)
assert torch.__version__ == "2.7.1+cpu" and torch.version.cuda is None
for cls in (DDPMScheduler, DDPMParallelScheduler):
    for spacing in ("leading", "linspace", "trailing"):
        cells = []
        for n in (0, -1, 1, 2, 50, 1000, 1001, None):
            scheduler = cls(num_train_timesteps=1000, timestep_spacing=spacing)
            try:
                scheduler.set_timesteps(n)
                ts = scheduler.timesteps.tolist()
                cells.append(f"n={n}: ok len={len(ts)} head={ts[:3]}")
            except Exception as exc:  # noqa: BLE001 - recording observed behaviour
                cells.append(f"n={n}: {type(exc).__name__}: {str(exc)[:60]}")
        print(f"{cls.__name__} {spacing}:\n  " + "\n  ".join(cells))
print("default spacing:", DDPMScheduler().config.timestep_spacing, DDPMParallelScheduler().config.timestep_spacing)
