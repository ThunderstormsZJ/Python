# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flatbuffers

import flatbuffers

class BlendFunc(object):
    __slots__ = ['_tab']

    # BlendFunc
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # BlendFunc
    def Src(self): return self._tab.Get(flatbuffers.number_types.Int32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(0))
    # BlendFunc
    def Dst(self): return self._tab.Get(flatbuffers.number_types.Int32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(4))

def CreateBlendFunc(builder, src, dst):
    builder.Prep(4, 8)
    builder.PrependInt32(dst)
    builder.PrependInt32(src)
    return builder.Offset()
