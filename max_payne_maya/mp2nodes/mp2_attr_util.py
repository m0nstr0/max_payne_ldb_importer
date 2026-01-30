import maya.api.OpenMaya as OpenMaya


def create_attr_numeric(cls, cls_attr, name, type, default, attr_hidden=False, attr_keyable=False, attr_writable=True, attr_storable=True):
    attr = OpenMaya.MFnNumericAttribute()
    setattr(cls, cls_attr, attr.create(name, name, type))
    attr.default = default
    attr.hidden = attr_hidden
    attr.keyable = attr_keyable
    attr.writable = attr_writable
    attr.storable = attr_storable
    cls.addAttribute(getattr(cls, cls_attr))


def create_attr_typed(cls, cls_attr, name, type, default, attr_hidden=False, attr_keyable=False, attr_writable=True, attr_storable=True):
    attr = OpenMaya.MFnTypedAttribute()
    setattr(cls, cls_attr, attr.create(name, name, type))
    attr.default = default
    attr.hidden = attr_hidden
    attr.keyable = attr_keyable
    attr.writable = attr_writable
    attr.storable = attr_storable
    cls.addAttribute(getattr(cls, cls_attr))


def create_attr_string(cls, cls_attr, name, default='', attr_hidden=False, attr_keyable=False, attr_writable=True, attr_storable=True):
    attr_value = OpenMaya.MFnStringData().create(default)
    create_attr_typed(cls, cls_attr, name, OpenMaya.MFnData.kString, attr_value, attr_hidden, attr_keyable, attr_writable, attr_storable)

def create_attr_enum(cls, cls_attr, name, values, default=0, attr_hidden=False, attr_keyable=False, attr_writable=True, attr_storable=True):
    attr = OpenMaya.MFnEnumAttribute()
    setattr(cls, cls_attr, attr.create(name, name, default))
    attr.hidden = attr_hidden
    attr.keyable = attr_keyable
    attr.writable = attr_writable
    attr.storable = attr_storable

    for i in range(len(values)):
        attr.addField(values[i], i)

    cls.addAttribute(getattr(cls, cls_attr))

def create_color_attr(cls, cls_attr, name, default=(1.0, 1.0, 1.0), attr_hidden=False, attr_keyable=False, attr_writable=True, attr_storable=True, attr_readable=True):
    attr = OpenMaya.MFnNumericAttribute()
    setattr(cls, cls_attr, attr.createColor(name, name))
    attr.default = default
    attr.hidden = attr_hidden
    attr.keyable = attr_keyable
    attr.writable = attr_writable
    attr.storable = attr_storable
    attr.readable = attr_readable
    attr.usedAsColor = True
    cls.addAttribute(getattr(cls, cls_attr))