import max_payne_sdk.max_ldb as max_ldb
import sys
import json

if len(sys.argv) != 3:
    print("Specify input and output")
    exit()

MAX_IN = sys.argv[1]
MAX_OUT = sys.argv[2]

print("Reading LDB file {}".format(MAX_IN))
ldb = max_ldb.MaxLDBReader(MAX_IN).parse()

FSMS = []
for fsm in ldb.getFSMs().fsms:
    FSM = {
        'shared_name': fsm.shared_name,
        'properties': {
            'name': fsm.properties.name,
            'room_id': fsm.properties.room_id,
            'parent_dynamic_mesh_name': fsm.properties.parent_dynamic_mesh_name,
            'object_to_room_transform': fsm.properties.object_to_room_transform,
            'object_to_parent_transform': fsm.properties.object_to_parent_transform
        },
        'states': fsm.states.states,
        'default_state': fsm.states.default,
        'startup_before': fsm.startup_before.messages,
        'startup_after': fsm.startup_after.messages
    }
    state_switch = []
    for fsm_event in fsm.state_switch.events:
        state_specifics = []
        for state_specific in fsm_event.state_specific.messages:
            state_specifics.append({'state_name': state_specific.state_name, 'messages': state_specific.messages.messages})
        state_switch.append({
            'name': fsm_event.state_name,
            'before_messages': fsm_event.before.messages,
            'state_specific': state_specifics,
            'after_messages': fsm_event.after.messages
        })
    FSM['state_switch'] = state_switch
    string_specific = []
    for fsm_event in fsm.string_specific.events:
        state_specifics = []
        for state_specific in fsm_event.state_specific.messages:
            state_specifics.append({'state_name' : state_specific.state_name, 'messages' : state_specific.messages.messages})
        string_specific.append({
            'name': fsm_event.state_name,
            'before_messages': fsm_event.before.messages,
            'state_specific': state_specifics,
            'after_messages': fsm_event.after.messages
        })
    FSM['string_specific'] = string_specific
    entity_specific = []
    for fsm_event in fsm.entity_specific.events:
        state_specifics = []
        for state_specific in fsm_event.state_specific.messages:
            state_specifics.append({'state_name': state_specific.state_name, 'messages': state_specific.messages.messages})
        entity_specific.append({
            'name': fsm_event.state_name,
            'before_messages': fsm_event.before.messages,
            'state_specific': state_specifics,
            'after_messages': fsm_event.after.messages
        })
    FSM['entity_specific'] = entity_specific
    FSMS.append(FSM)

CHARACTERS = []
for character in ldb.getCharacters().characters:
    CHARACTER = {
        'character_name': character.character_name,
        'shared_name': character.shared_name,
        'properties': {
            'name': character.properties.name,
            'room_id': character.properties.room_id,
            'parent_dynamic_mesh_name': character.properties.parent_dynamic_mesh_name,
            'object_to_room_transform': character.properties.object_to_room_transform,
            'object_to_parent_transform': character.properties.object_to_parent_transform
        },
        'fsm' : {
            'startup_before': character.startup_before.messages,
            'on_death_before': character.on_death_before.messages,
            'on_activate_before': character.on_activate_before.messages,
            'on_special_before': character.on_special_before.messages
        }
    }
    CHARACTERS.append(CHARACTER)

TRIGGERS = []
for trigger in ldb.getTriggers().triggers:
    TRIGGER = {
        'shared_name': trigger.shared_name,
        'properties': {
            'name': trigger.properties.name,
            'room_id': trigger.properties.room_id,
            'parent_dynamic_mesh_name': trigger.properties.parent_dynamic_mesh_name,
            'object_to_room_transform': trigger.properties.object_to_room_transform,
            'object_to_parent_transform': trigger.properties.object_to_parent_transform
        },
        'radius': trigger.radius,
        'type': trigger.type
    }
    TRIGGERS.append(TRIGGER)

ITEMS = []
for item in ldb.getItems().items:
    ITEM = {
        'item_name': item.item_name,
        'shared_name': item.shared_name,
        'properties': {
            'name': item.object_properties.name,
            'room_id': item.object_properties.room_id,
            'parent_dynamic_mesh_name': item.object_properties.parent_dynamic_mesh_name,
            'object_to_room_transform': item.object_properties.object_to_room_transform,
            'object_to_parent_transform': item.object_properties.object_to_parent_transform
        }
    }
    ITEMS.append(ITEM)

WAYPOINTS = []
for waypoint in ldb.getWaypoints().waypoints:
    WAYPOINT = {
        'shared_name': waypoint.shared_name,
        'properties': {
            'name': waypoint.object_properties.name,
            'room_id': waypoint.object_properties.room_id,
            'parent_dynamic_mesh_name': waypoint.object_properties.parent_dynamic_mesh_name,
            'object_to_room_transform': waypoint.object_properties.object_to_room_transform,
            'object_to_parent_transform': waypoint.object_properties.object_to_parent_transform
        },
        'type': waypoint.type
    }
    WAYPOINTS.append(WAYPOINT)

POINTLIGHTS = []
for pointlight in ldb.getPointlights().pointlights:
    POINTLIGHT = {
        'id': pointlight.id,
        'properties': {
            'name': pointlight.object_properties.name,
            'room_id': pointlight.object_properties.room_id,
            'parent_dynamic_mesh_name': pointlight.object_properties.parent_dynamic_mesh_name,
            'object_to_room_transform': pointlight.object_properties.object_to_room_transform,
            'object_to_parent_transform': pointlight.object_properties.object_to_parent_transform
        },
        'color': {
            'r': pointlight.r,
            'g': pointlight.g,
            'b': pointlight.b,
            'a': pointlight.a,
        },
        'falloff': pointlight.falloff,
        'intensity': pointlight.intensity
    }
    POINTLIGHTS.append(POINTLIGHT)

DYNAMICMESHES = []
for dynamicmesh in ldb.getDynamicMeshes().dynamic_meshes:
    DYNAMICMESH = {
        'shared_name': dynamicmesh.shared_name,
        'properties': {
            'name': dynamicmesh.properties.name,
            'room_id': dynamicmesh.properties.room_id,
            'parent_dynamic_mesh_name': dynamicmesh.properties.parent_dynamic_mesh_name,
            'object_to_room_transform': dynamicmesh.properties.object_to_room_transform,
            'object_to_parent_transform': dynamicmesh.properties.object_to_parent_transform
        },
        'transform': dynamicmesh.transform,
        'config': {
            'dynamic_collisions': dynamicmesh.config.dynamic_collisions,
            'bullet_collisions': dynamicmesh.config.bullet_collisions,
            'light_mapped': dynamicmesh.config.light_mapped,
            'cont_update': dynamicmesh.config.cont_update,
            'pointlight_affected': dynamicmesh.config.pointlight_affected,
            'block_explosions': dynamicmesh.config.block_explosions
        },
        'animations': []
    }
    animations = []
    for animation in dynamicmesh.animations.animations:
        ANIMATION = {
            'animation_name': animation.animation_name,
            'length_in_secs': animation.length_in_secs,
            'start_transform': animation.start_transform,
            'end_transform': animation.end_transform,
            'fsm': {
                'leaving_first_frame': animation.leaving_first_frame.messages,
                'returning_first_frame': animation.returning_first_frame.messages,
                'reaching_second_frame': animation.reaching_second_frame.messages
            },
            'translation_graph': {
                'sample_rate': animation.translation_graph.sample_rate,
                'points': animation.translation_graph.points
            },
            'rotation_graph': {
                'sample_rate': animation.rotation_graph.sample_rate,
                'points': animation.rotation_graph.points
            }
        }
        DYNAMICMESH['animations'].append(ANIMATION)
    DYNAMICMESHES.append(DYNAMICMESH)

ROOMS = []
for room in ldb.getRooms().rooms:
    ROOM = {
        'id': room.id,
        'name': room.name,
        'static_meshes': room.static_meshes,
        'dynamic_lights': room.dynamic_lights,
        'exits': room.exits,
        'start_points': room.start_points,
        'fsms': room.fsms,
        'characters': room.characters,
        'triggers': room.triggers,
        'dynamic_meshes': room.dynamic_meshes,
        'level_items': room.level_items,
        'point_lights': room.point_lights,
    }
    ROOMS.append(ROOM)

f = open(MAX_OUT, "w")
f.write(json.dumps({'FSMS': FSMS, 'CHARACTERS': CHARACTERS, 'TRIGGERS': TRIGGERS, 'ITEMS': ITEMS, 'WAYPOINTS': WAYPOINTS, 'POINTLIGHTS': POINTLIGHTS, 'DYNAMICMESHES': DYNAMICMESHES, 'ROOMS': ROOMS}, indent=4))
f.close()