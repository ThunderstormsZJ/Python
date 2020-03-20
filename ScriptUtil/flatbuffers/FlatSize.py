# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flatbuffers

import flatbuffers

class FlatSize(object):
    __slots__ = ['_tab']

    # FlatSize
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # FlatSize
    def Width(self): return self._tab.Get(flatbuffers.number_types.Float32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(0))
    # FlatSize
    def Height(self): return self._tab.Get(flatbuffers.number_types.Float32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(4))

def CreateFlatSize(builder, width, height):
    builder.Prep(4, 8)
    builder.PrependFloat32(height)
    builder.PrependFloat32(width)
    return builder.Offset()
