import max_payne_sdk.max_kf2 as max_kf2
import sys
import json

if len(sys.argv) != 3:
    print("Specify input and output")
    exit()

MAX_IN = sys.argv[1]
MAX_OUT = sys.argv[2]

print("Reading KF2 file {}".format(MAX_IN))
kf2 = max_kf2.MaxKF2Reader().parse(MAX_IN)

q = []
for mesh in kf2.getMeshes():
    a = [
        mesh.node.object_to_parent_transform[0] + [0.0],
        mesh.node.object_to_parent_transform[1] + [0.0],
        mesh.node.object_to_parent_transform[2] + [0.0],
        mesh.node.object_to_parent_transform[3] + [1.0]
    ]
    a[3][0] = a[3][0] * 100.0
    a[3][1] = a[3][1] * 100.0
    a[3][2] = a[3][2] * 100.0

    node = {
        "name": mesh.node.name,
        "transform": a,
        "parent": mesh.node.parent_name
    }
    q.append(node)

f = open(MAX_OUT, "w")
f.write(json.dumps({'nodes': q}, indent = 4))
f.close()
