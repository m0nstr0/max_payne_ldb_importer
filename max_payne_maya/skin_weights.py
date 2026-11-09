"""Map source bone IDs to Maya's dense influenceObjects() ordering."""


def dense_weights(vertex, source_to_physical, influence_count):
    if len(vertex.vertex_bone_indices) != len(vertex.vertex_weights):
        raise ValueError("Mismatched vertex bone/weight arrays")
    result = [0.0] * influence_count
    for bone, weight in zip(vertex.vertex_bone_indices, vertex.vertex_weights):
        if bone not in source_to_physical:
            raise ValueError("Skin bone %d is missing from the selected skeleton" % bone)
        index = source_to_physical[bone]
        if not 0 <= index < influence_count:
            raise ValueError("Skin influence index outside cluster")
        result[index] += weight
    return result
