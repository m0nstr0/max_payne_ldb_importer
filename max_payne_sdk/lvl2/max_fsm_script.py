import struct

from max_payne_sdk.lvl2.max_chunk import MaxChunk
from max_payne_sdk.lvl2.max_pack import packString, packInt, packBool, packFloat, packUInt


class MaxFSMTimer:
    def __init__(self):
        self.name = ''
        self.length = 0.0
        self.is_real_time = False

    def getBytes(self):
        data = [packBool(self.is_real_time), packFloat(self.length)]
        max_chunk = MaxChunk(0, 1)
        return [packString(self.name)] + max_chunk.getBytes(data)


class MaxFMSCustomState:
    def __init__(self):
        self.name = ''

    def getBytes(self):
        return []


class MaxFSMCustomEvent:
    def __init__(self):
        self.name = ''

    def getBytes(self):
        return []

class MaxFSMMessage:
    def __init__(self):
        self.message = ''
        self.function_name = ''
        self.target_node_name = ''
        self.parameters = []
        self.is_target_node_global = False
        self.target_node_id = 0

    def getBytes(self):

        data = [packString(self.message),
                packString(self.function_name),
                packString(self.target_node_name),
                struct.pack('<c', b'\x1C'),
                packInt(len(self.parameters))]

        for i in self.parameters:
            data.append(packString(i))

        data = data + [packBool(self.is_target_node_global),
                       packUInt(self.target_node_id),
                       struct.pack('<c', b'\x1C'),
                       packInt(len(self.parameters))]

        for i in self.parameters:
            data.append(packUInt(0))

        max_chunk = MaxChunk(0, 1)
        return max_chunk.getBytes(data)

class MaxFSMStateSpecificMessage:
    def __init__(self):
        self.state_name = ''
        self.messages = []

    def getBytes(self):
        data = [packString(self.state_name),
                struct.pack('<c', b'\x1C'),
                packInt(len(self.messages))]

        for i in self.messages:
            data = data + i.getBytes()

        return data

class MaxFSMEvent:
    def __init__(self, name):
        self.name = name
        self.always_before_messages = []
        self.state_specific = []
        self.always_after_messages = []

    def getBytes(self):
        data = [packString(self.name),
                struct.pack('<c', b'\x1C'),
                packInt(len(self.always_before_messages))]

        for i in self.always_before_messages:
            data = data + i.getBytes()

        data = data + [struct.pack('<c', b'\x1F'), packInt(len(self.state_specific))]
        for i in self.state_specific:
            data = data + i.getBytes()


        data = data + [struct.pack('<c', b'\x1C'), packInt(len(self.always_after_messages))]
        for i in self.always_after_messages:
            data = data + i.getBytes()

        return data

class MaxFSMScript:
    def __init__(self):
        self.timers = []
        self.custom_states = []
        self.default_custom_state_name = ''
        self.custom_events = []
        self.events = []
        self.can_add_states = True
        self.can_add_events = True

    def getBytes(self):
        data = []

        data = data + [struct.pack('<c', b'\x1D'), packInt(len(self.custom_states))]
        for i in self.custom_states:
            data.append(packString(i.name))
        data.append(packString(self.default_custom_state_name))

        data = data + [struct.pack('<c', b'\x1D'), packInt(len(self.custom_events))]
        for i in self.custom_events:
            data.append(packString(i.name))

        data = data + [struct.pack('<c', b'\x1F'), packInt(len(self.events))]
        for i in self.events:
            data = data + i.getBytes()

        data.append(packBool(self.can_add_states))
        data.append(packBool(self.can_add_events))

        data = data + [struct.pack('<c', b'\x1F'), packInt(len(self.timers))]
        for i in self.timers:
            data = data + i.getBytes()

        max_chunk = MaxChunk(0, 1)
        return [packUInt(max_chunk.getSize(data))] + max_chunk.getBytes(data)