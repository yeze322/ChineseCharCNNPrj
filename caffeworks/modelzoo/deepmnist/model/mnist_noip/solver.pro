net: "model.net"

base_lr: 0.01
momentum: 0.9
weight_decay: 0.0005

lr_policy: "inv"
gamma: 0.0001
power: 0.75

display: 500
max_iter: 5000
snapshot: 5000
snapshot_prefix: "para"

solver_mode: GPU
