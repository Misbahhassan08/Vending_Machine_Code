__all__ = [
'VERTEX2F',
'VERTEX2II',
'BITMAP_SOURCE',
'CLEAR_COLOR_RGB',
'TAG',
'COLOR_RGB',
'BITMAP_HANDLE',
'CELL',
'BITMAP_LAYOUT',
'BITMAP_SIZE',
'ALPHA_FUNC',
'STENCIL_FUNC',
'BLEND_FUNC',
'STENCIL_OP',
'POINT_SIZE',
'LINE_WIDTH',
'CLEAR_COLOR_A',
'COLOR_A',
'CLEAR_STENCIL',
'CLEAR_TAG',
'STENCIL_MASK',
'TAG_MASK',
'BITMAP_TRANSFORM_A',
'BITMAP_TRANSFORM_B',
'BITMAP_TRANSFORM_C',
'BITMAP_TRANSFORM_D',
'BITMAP_TRANSFORM_E',
'BITMAP_TRANSFORM_F',
'SCISSOR_XY',
'SCISSOR_SIZE',
'CALL',
'JUMP',
'BEGIN',
'COLOR_MASK',
'CLEAR',
'END',
'SAVE_CONTEXT',
'RESTORE_CONTEXT',
'RETURN',
'MACRO',
'DISPLAY'
]
#Display List Macro's
def VERTEX2F(x,y):
    value = ((0x01<<30)|(((x)&0x7FFF)<<15)|(((y)&0x7FFF)<<0))
    #PrintResponse("VERTEX2F: " + hex(value) + " " + str(value))
    return value 
def VERTEX2II(x,y,handle,cell):
	value = ((0x02<<30)|(((x)&0x1FF)<<21)|(((y)&0x1FF)<<12)|(((handle)&0x1F)<<7)|(((cell)&0x7F)<<0))
	#PrintResponse("VERTEX2II: " + hex(value) + " " + str(value))
	return value 
def BITMAP_SOURCE(addr):
	value = ((0x01<<24)|(((addr)&0xFFFFF)<<0))
	#PrintResponse("BITMAP_SOURCE: " + hex(value) + " " + str(value))
	return value 
def CLEAR_COLOR_RGB(red,green,blue):
	value = ((0x02<<24)|(((red)&0xFF)<<16)|(((green)&0xFF)<<8)|(((blue)&0xFF)<<0)) 
	#PrintResponse("CLEAR_COLOR_RGB: " + hex(value) + " " + str(value))
	return value
def TAG(s):
	value = ((0x03<<24)|(((s)&0xFF)<<0))
	#PrintResponse("VERTEX2II: " + hex(value) + " " + str(value))
	return value
def COLOR_RGB(red,green,blue):
    value = ((0x04<<24)|(((red)&0xFF)<<16)|(((green)&0xFF)<<8)|(((blue)&0xFF)<<0))
    #PrintResponse("COLOR_RGB: " + hex(value) + " " + str(value))
    return value
def BITMAP_HANDLE(handle):
    value = ((0x05<<24)|(((handle)&0x1F)<<0))
    #PrintResponse("VERTEX2II: " + hex(value) + " " + str(value))
    return value 
def CELL(cell): 
    value = ((0x06<<24)|(((cell)&0x7F)<<0))
    #PrintResponse("CELL: " + hex(value) + " " + str(value))
    return value 
def BITMAP_LAYOUT(format,linestride,height): 
    value = ((0x07<<24)|(((format)&0x1F)<<19)|(((linestride)&0x3FF)<<9)|(((height)&0x1FF)<<0))
    #PrintResponse("BITMAP_LAYOUT: " + hex(value) + " " + str(value))
    return value 
def BITMAP_SIZE(filter,wrapx,wrapy,width,height): 
    value = ((0x08<<24)|(((filter)&0x01)<<20)|(((wrapx)&0x01)<<19)|(((wrapy)&0x01)<<18)|(((width)&0x1FF)<<9)|(((height)&0x1FF)<<0))
    #PrintResponse("BITMAP_SIZE: " + hex(value) + " " + str(value))
    return value 
def ALPHA_FUNC(func,ref): 
    value = ((0x09<<24)|(((func)&0x07)<<8)|(((ref)&0xFF)<<0))
    #PrintResponse("ALPHA_FUNC: " + hex(value) + " " + str(value))
    return value 
def STENCIL_FUNC(func,ref,mask): 
    value = ((0x0A<<24)|(((func)&0x07)<<16)|(((ref)&0xFF)<<8)|(((mask)&0xFF)<<0))
    #PrintResponse("STENCIL_FUNC: " + hex(value) + " " + str(value))
    return value 
def BLEND_FUNC(src,dst): 
    value = ((0x0B<<24)|(((src)&0x07)<<3)|(((dst)&0x07)<<0))
    #PrintResponse("BLEND_FUNC: " + hex(value) + " " + str(value))
    return value 
def STENCIL_OP(sfail,spass): 
    value = ((0x0C<<24)|(((sfail)&0x07)<<3)|(((spass)&0x07)<<0))
    #PrintResponse("STENCIL_OP: " + hex(value) + " " + str(value))
    return value 
def POINT_SIZE(size):
    value = ((0x0D<<24)|(((size)&0x1FFF)<<0))
    #PrintResponse("POINT_SIZE: " + hex(value) + " " + str(value))
    return value 
def LINE_WIDTH(width): 
    value = ((0x0E<<24)|(((width)&0xFFFF)<<0))
    #PrintResponse("LINE_WIDTH: " + hex(value) + " " + str(value))
    return value 
def CLEAR_COLOR_A(alpha): 
    value = ((0x0F<<24)|(((alpha)&0xFF)<<0))
    #PrintResponse("CLEAR_COLOR_A: " + hex(value) + " " + str(value))
    return value 
def COLOR_A(alpha): 
    value = ((0x10<<24)|(((alpha)&0xFF)<<0))
    #PrintResponse("COLOR_A: " + hex(value) + " " + str(value))
    return value 
def CLEAR_STENCIL(s): 
    value = ((0x11<<24)|(((s)&0xFF)<<0))
    #PrintResponse("CLEAR_STENCIL: " + hex(value) + " " + str(value))
    return value 
def CLEAR_TAG(s): 
    value = ((0x12<<24)|(((s)&0xFF)<<0))
    #PrintResponse("CLEAR_TAG: " + hex(value) + " " + str(value))
    return value 
def STENCIL_MASK(mask): 
    value = ((0x13<<24)|(((mask)&0xFF)<<0))
    #PrintResponse("STENCIL_MASK: " + hex(value) + " " + str(value))
    return value 
def TAG_MASK(mask): 
    value = ((0x14<<24)|(((mask)&0x01)<<0))
    #PrintResponse("TAG_MASK: " + hex(value) + " " + str(value))
    return value 
def BITMAP_TRANSFORM_A(a): 
    value = ((0x15<<24)|(((a)&0x1FFFF)<<0))
    #PrintResponse("BITMAP_TRANSFORM_A: " + hex(value) + " " + str(value))
    return value 
def BITMAP_TRANSFORM_B(b): 
    value = ((0x16<<24)|(((b)&0x1FFFF)<<0))
    #PrintResponse("BITMAP_TRANSFORM_B: " + hex(value) + " " + str(value))
    return value 
def BITMAP_TRANSFORM_C(c): 
    value = ((0x17<<24)|(((c)&0xFFFFFF)<<0))
    #PrintResponse("BITMAP_TRANSFORM_C: " + hex(value) + " " + str(value))
    return value 
def BITMAP_TRANSFORM_D(d): 
    value = ((0x18<<24)|(((d)&0x1FFFF)<<0))
    #PrintResponse("BITMAP_TRANSFORM_D: " + hex(value) + " " + str(value))
    return value 
def BITMAP_TRANSFORM_E(e): 
    value = ((0x19<<24)|(((e)&0x1FFFF)<<0))
    #PrintResponse("BITMAP_TRANSFORM_E: " + hex(value) + " " + str(value))
    return value 
def BITMAP_TRANSFORM_F(f):
    value = ((0x1A<<24)|(((f)&0xFFFFFF)<<0))
    #PrintResponse("BITMAP_TRANSFORM_F: " + hex(value) + " " + str(value))
    return value 
def SCISSOR_XY(x,y):
    value = ((0x1B<<24)|(((x)&0x1FF)<<9)|(((y)&0x1FF)<<0))
    #PrintResponse("SCISSOR_XY: " + hex(value) + " " + str(value))
    return value 
def SCISSOR_SIZE(width,height):
    value = ((0x1C<<24)|(((width)&0x3FF)<<12)|(((height)&0x3FF)<<0))
    #PrintResponse("SCISSOR_SIZE: " + hex(value) + " " + str(value))
    return value
def CALL(dest):
    value = ((0x1D<<24)|(((dest)&0xFFFF)<<0))
    #PrintResponse("CALL: " + hex(value) + " " + str(value))
    return value 
def JUMP(dest):
    value = ((0x1E<<24)|(((dest)&0xFFFF)<<0))
    #PrintResponse("JUMP: " + hex(value) + " " + str(value))
    return value 
def BEGIN(prim):
	value = ((0x1F<<24)|(((prim)&0x0F)<<0))
	#PrintResponse("BEGIN: " + hex(value) + " " + str(value))
	return value
def COLOR_MASK(r,g,b,a):
    value = ((0x20<<24)|(((r)&0x01)<<3)|(((g)&0x01)<<2)|(((b)&0x01)<<1)|(((a)&0x01)<<0))
    #PrintResponse("COLOR_MASK: " + hex(value) + " " + str(value))
    return value
def CLEAR(c,s,t):
	value = (((0x26<<24)|(((c)&0x01)<<2)|(((s)&0x01)<<1)|(((t)&0x01)<<0)))
	#PrintResponse("CLEAR: " + hex(value) + " " + str(value))
	return value
def END():
    value = (0x21<<24)
    #PrintResponse("END: " + hex(value) + " " + str(value))
    return value
def SAVE_CONTEXT():
    value = ((0x22<<24))
    #PrintResponse("SAVE_CONTEXT: " + hex(value) + " " + str(value))
    return value 
def RESTORE_CONTEXT():
    value = ((0x23<<24))
    #PrintResponse("RESTORE_CONTEXT: " + hex(value) + " " + str(value))
    return value 
def RETURN():
    value = ((0x24<<24))
    #PrintResponse("RETURN: " + hex(value) + " " + str(value))
    return value 
def MACRO(m):
    value = ((0x25<<24)|(((m)&0x01)<<0))
    #PrintResponse("MACRO: " + hex(value) + " " + str(value))
    return value 
def DISPLAY():
	value = 00 << 24
	#PrintResponse("DISPLAY: " + hex(value) + " " + str(value))
	return value