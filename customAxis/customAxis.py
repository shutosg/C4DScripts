import c4d
from c4d import gui
#Welcome to the world of Python


def main():
    if op == None:
        gui.MessageDialog("Select object!")
        return
    pyTag = op.MakeTag(c4d.Tpython)
    pyTag.SetName("CustomAxis")
    rootGroup = c4d.GetCustomDataTypeDefault(c4d.DTYPE_GROUP)
    rootGroup[c4d.DESC_NAME] = "CustomAxis"
    rootGroup[c4d.DESC_SHORT_NAME] = "CustomAxis"
    rootGroup[c4d.DESC_TITLEBAR] = 1
    rootGroup[c4d.DESC_PARENTGROUP] = c4d.DescID()
    descId = pyTag.AddUserData(rootGroup)
    secondGroup = c4d.GetCustomDataTypeDefault(c4d.DTYPE_GROUP)
    secondGroup[c4d.DESC_NAME] = "Axis Position"
    secondGroup[c4d.DESC_SHORT_NAME] = "Axis Position"
    secondGroup[c4d.DESC_TITLEBAR] = 1
    secondGroup[c4d.DESC_PARENTGROUP] = descId
    secondGroup[c4d.DESC_COLUMNS] = 3
    descId = pyTag.AddUserData(secondGroup)
    label = [
    "X   |   Left", "Center", "Right", \
    "Y   |   Bottom", "Center", "Top", \
    "Z   |   Front", "Center", "Back"
    ]
    default = [0, 1, 0, 1, 0, 0, 0, 1, 0]
    
    for i in range(9):
        bc = c4d.GetCustomDataTypeDefault(c4d.DTYPE_BOOL)
        bc[c4d.DESC_NAME] = label[i]
        bc[c4d.DESC_SHORT_NAME] = label[i]
        bc[c4d.DESC_PARENTGROUP] = descId
        bc[c4d.DESC_DEFAULT] = default[i]
        bc
        bc[c4d.DESC_ANIMATE] = c4d.DESC_ANIMATE_OFF
        descId2 = pyTag.AddUserData(bc)
        pyTag[descId2] = default[i]
    
    
    ##### TPYTHON_CODE is from ##### 
    # https://twitter.com/gupon/status/724619989366378497
    #####
    
    pyTag[c4d.TPYTHON_CODE] = 'import c4d\n#Welcome to the world of Python\n\nprev_stats = 0b010010010\ninited = False\nparent = c4d.BaseObject(c4d.Ocube)\n\ndef main():\n\tglobal prevSize\n\tglobal prev_stats\n\tglobal inited\n\tglobal parent\n\t\n\tinited = parent == op.GetObject()\n\t\n\tif not inited:\n\t\tparent = op.GetObject()\n\t\tprevSize = parent.GetRad()\n\t\top.Message(c4d.MSG_UPDATE)\n\t\tinited = True\n\t\n\t# get axis data\n\tIDUD = c4d.ID_USERDATA\n\taxisID = [[(IDUD, 3), (IDUD, 4), (IDUD, 5)], #axisX \\ \n\t\t\t [(IDUD, 6), (IDUD, 7), (IDUD, 8)], #axisY \\ \n\t\t\t [(IDUD, 9), (IDUD, 10), (IDUD, 11)]] #axisZ \\\n\t\n\t#check & update status\n\tbool2Bin = lambda a, b: (a<<1) + int(b)\n\tval = lambda v: op[v]\n\tstats =   (reduce(bool2Bin, map(val, axisID[0])) << 0) \\\n\t\t\t+ (reduce(bool2Bin, map(val, axisID[1])) << 3) \\\n\t\t\t+ (reduce(bool2Bin, map(val, axisID[2])) << 6)\n\t \n\tfor i in xrange(3):\n\t\tcurrent = (stats & (0b111 << i * 3)) >> (i * 3)\n\t\tprev = (prev_stats & (0b111 << i * 3)) >> (i * 3)\n\t\t\n\t\tif current != prev:\n\t\t\told = current & prev\n\t\t\t\n\t\t\tif current == 0:\n\t\t\t\tstats = stats | (prev << (i * 3))\n\t\t\t\t\n\t\t\telif old > 0:\n\t\t\t\tfor j in xrange(3):\n\t\t\t\t\tif old & (0b1 << j):\n\t\t\t\t\t\tstats = stats ^ (0b1 << (i * 3 + j))\n\t\n\t# apply status to UI\n\tvec = c4d.Vector(0)\n\tfor i in xrange(3):\n\t\tfor j in xrange(3):\n\t\t\tv = bool(stats & (0b1 << (i * 3 + j)))\n\t\t\top[axisID[i][2-j]] = v\n\t\t\t\n\t\t\t#set vector for position offset\n\t\t\tif v: vec[i] = 1-j\n\t\n\t# get size and offset by diff\n\tsize = parent.GetRad()\n\tdSize = size - prevSize\n\tdPos = c4d.Vector(dSize.x * vec.x, dSize.y * vec.y, dSize.z * vec.z)\n\tparent.SetRelPos(parent.GetRelPos() - dPos)\n\t\n\t# store status and size\n\tprev_stats = stats\n\tprevSize = size'


if __name__=='__main__':
    main()
    c4d.EventAdd()