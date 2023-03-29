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
s = []
pi = []
# for mesh in kf2.getMeshes():
#     a = [
#         mesh.node.object_to_parent_transform[0] + [0.0],
#         mesh.node.object_to_parent_transform[1] + [0.0],
#         mesh.node.object_to_parent_transform[2] + [0.0],
#         mesh.node.object_to_parent_transform[3] + [1.0]
#     ]
#     a[3][0] = a[3][0] * 100.0
#     a[3][1] = a[3][1] * 100.0
#     a[3][2] = a[3][2] * 100.0
#
#     node = {
#         "name": mesh.node.name,
#         "transform": a,
#         "parent": mesh.node.parent_name
#     }
#
#     smoothing = {
#         "smoothing": mesh.smoothing.smoothing_groups
#     }
#
#     polygons_indx = {
#         "polygon_idx": mesh.polygons.polygons_indices
#     }
#
#     print("smoothing_groups num %s" % len(mesh.smoothing.smoothing_groups))
#     print("geometry.vertices num %s" % len(mesh.geometry.vertices))
#     print("geometry.vertices_per_primitive num %s (%i)" % (len(mesh.geometry.vertices_per_primitive), mesh.geometry.vertices_per_primitive[0]))
#     print("polygons.polygons_indices num %s" % len(mesh.polygons.polygons_indices))
#     print("polygons.polygons_per_primitive num %s (%i)" % (len(mesh.polygons.polygons_per_primitive), mesh.polygons.polygons_per_primitive[0]))
#
#
#     q.append(node)
#     s.append(smoothing)
#     pi.append(polygons_indx)

l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
print(l)
l[1:] = l[len(l):0:-1]
print(l)

f = open(MAX_OUT, "w")
f.write(json.dumps({'nodes': q, 'smoothing': s, 'polygon_indices': pi}, indent = 4))
f.close()
