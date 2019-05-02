import c4d
import time
#Welcome to the world of Python


def main():
    obj = c4d.BaseObject(c4d.Onull)
    obj.SetName("Music")
    doc.InsertObject(obj)
    doc.SetSelection(obj)

    tr = c4d.CTrack(obj,c4d.DescID(c4d.DescLevel(c4d.CTsound, c4d.CTsound, 0)))
    obj.InsertTrackSorted(tr)

    pyTag = obj.MakeTag(c4d.Tpython)
    pyTag.SetName("Music")

    rootGroup = c4d.GetCustomDataTypeDefault(c4d.DTYPE_GROUP)
    rootGroup[c4d.DESC_NAME] = "Sound Properties"
    rootGroup[c4d.DESC_SHORT_NAME] = "Sound"
    rootGroup[c4d.DESC_TITLEBAR] = 1
    rootGroup[c4d.DESC_GUIOPEN] = 1
    rootGroup[c4d.DESC_PARENTGROUP] = c4d.DescID()
    descId = obj.AddUserData(rootGroup)

    secondGroup = c4d.GetCustomDataTypeDefault(c4d.DTYPE_GROUP)
    secondGroup[c4d.DESC_NAME] = "Basic Properties"
    secondGroup[c4d.DESC_SHORT_NAME] = "Basic"
    secondGroup[c4d.DESC_TITLEBAR] = 1
    secondGroup[c4d.DESC_GUIOPEN] = 1
    secondGroup[c4d.DESC_PARENTGROUP] = descId
    descId = obj.AddUserData(secondGroup)

    label = ["Use Sound", "Start Time", "Sound"]
    default = [1, c4d.BaseTime(), ""]
    typ = [c4d.DTYPE_BOOL, c4d.DTYPE_TIME, c4d.DTYPE_FILENAME]

    for i in range(3):
        bc = c4d.GetCustomDataTypeDefault(typ[i])
        bc[c4d.DESC_NAME] = label[i]
        bc[c4d.DESC_SHORT_NAME] = label[i]
        bc[c4d.DESC_PARENTGROUP] = descId
        bc[c4d.DESC_DEFAULT] = default[i]
        bc[c4d.DESC_ANIMATE] = c4d.DESC_ANIMATE_OFF
        descId2 = obj.AddUserData(bc)
        obj[descId2] = default[i]

    pyTag[c4d.TPYTHON_CODE] = 'import c4d\n#Welcome to the world of Python\n\n\ndef main():\n    obj = op.GetObject()\n    tr = obj.GetCTracks()[0]\n    tr[c4d.CID_SOUND_ONOFF] = obj[(c4d.ID_USERDATA, 3)]\n    tr[c4d.CID_SOUND_START] = obj[(c4d.ID_USERDATA, 4)]\n    tr[c4d.CID_SOUND_NAME] = obj[(c4d.ID_USERDATA, 5)]\n'

if __name__=='__main__':
    main()
    c4d.EventAdd()
