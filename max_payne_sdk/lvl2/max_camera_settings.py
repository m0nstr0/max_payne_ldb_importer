from max_payne_sdk.lvl2.max_pack import packDouble, packVector3


class MaxCameraSettings:
    def __init__(self):
        self.pos_x = 0.0
        self.pos_y = 8.0
        self.pos_z = -8.0
        self.rotation = [0.7853982, 0.0, 0.0]
        self.speed = 1.0

    def getBytes(self):
        data = [packDouble(self.pos_x),
                packDouble(self.pos_y),
                packDouble(self.pos_z),
                packVector3(self.rotation),
                packDouble(self.speed)]
        return data
