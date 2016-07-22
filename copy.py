from idaapi import Form
from struct import pack, unpack
import idc

u32 = lambda d: unpack('<I', d)[0]
u64 = lambda d: unpack('<Q', d)[0]

def to_int_array(d, QWORD = 0):
    r = []
    length = len(d)
    if QWORD:
        length -= length % 8
        for i in range(0, length, 8):
            r.append(u64(d[i: i+8]))
    else:
        length -= length % 4
        for i in range(0, length, 4):
            r.append(u32(d[i: i+4]))
    return r

def OnFormChange(fid):
    getval = f.GetControlValue
    n = getval(f.iNumberOfElement)
    size = getval(f.iElementSize)
    addr = getval(f.iStartAddress)

    if fid == f.iNumberOfElement.id:
        if ((n != 0) and (size != 0)):
            d = get_bytes(addr, n*size)
            print 'Your bytes: ', repr(d)
            print
            print 'Your bytes in DWORD array: ', to_int_array(d)
            print
            print 'Your bytes in QWORD array: ', to_int_array(d, 1)

def get_bytes(addr, n):
    return idc.GetManyBytes(addr, n)

def main():
    global f
    f = Form('''STARTITEM 0
    copy

    {FormChangeCb}
    <#address#Start address:{iStartAddress}>
    <#size#Element size:{iElementSize}>
    <#num#Number of element:{iNumberOfElement}>
    {FormChangeCb}
    ''',
{'iStartAddress': Form.NumericInput(tp=Form.FT_ADDR),
'iElementSize': Form.NumericInput(tp=Form.FT_DEC),
'iNumberOfElement': Form.NumericInput(tp=Form.FT_DEC),
'FormChangeCb': Form.FormChangeCb(OnFormChange)
})
    f.Compile()
    f.Execute()

main()
