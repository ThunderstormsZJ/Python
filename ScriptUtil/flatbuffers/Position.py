# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flatbuffers

import flatbuffers

class Position(object):
    __slots__ = ['_tab']

    # Position
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Position
    def X(self): return self._tab.Get(flatbuffers.number_types.Float32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(0))
    # Position
    def Y(self): return self._tab.Get(flatbuffers.number_types.Float32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(4))

def CreatePosition(builder, x, y):
    builder.Prep(4, 8)
    builder.PrependFloat32(y)
    builder.PrependFloat32(x)
    return builder.Offset()
