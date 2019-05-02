import os
import c4d
from c4d import gui, documents, bitmaps

WINDOW_TITLE = 'Easy Visibility Switcher'

BUTTON_GROUP = 300

# ボタンIDの下位4bit
VISIBILITY_ID_VISIBLE   = 0b0000
VISIBILITY_ID_INVISIBLE = 0b0001
VISIBILITY_ID_DEFAULT   = 0b0010

# ボタンIDの上位4bit
BUTTON_FLAG_EDITOR = 1 << 4
BUTTON_FLAG_RENDER = 1 << 5

BORDER_SPACE = 5

path, file = os.path.split(__file__)

class EasyVisiblitySwitcher(gui.GeDialog):
    # カスタムボタン作成
    def _addImageButton(self, button_id, file_name):
        bc = c4d.BaseContainer()
        bmp = bitmaps.BaseBitmap()
        bmp.InitWith(os.path.join(path, "res", file_name))
        hoge = self.AddCustomGui(button_id, c4d.CUSTOMGUI_BITMAPBUTTON, "", c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 16, 16, bc)
        hoge.SetImage(bmp, True)
        
    # ボタン作成
    def _addButtonGroup(self, label, buttonFlag):
        self.AddStaticText(0, c4d.BFH_LEFT | c4d.BFV_SCALEFIT, 0, 0, label, c4d.BORDER_NONE)
        self.GroupBorderSpace(BORDER_SPACE, 0, BORDER_SPACE, 0)
        self._addImageButton(VISIBILITY_ID_DEFAULT   | buttonFlag, 'default.png')
        self._addImageButton(VISIBILITY_ID_VISIBLE   | buttonFlag, 'visible.png')
        self._addImageButton(VISIBILITY_ID_INVISIBLE | buttonFlag, 'invisible.png')

    def CreateLayout(self):
        self.SetTitle(WINDOW_TITLE)
        # ボタン追加
        self.GroupBegin(BUTTON_GROUP, c4d.BFH_SCALEFIT, 12)
        self.GroupBorderNoTitle(c4d.BORDER_NONE)
        self._addButtonGroup(' Both',   BUTTON_FLAG_EDITOR | BUTTON_FLAG_RENDER)
        self._addButtonGroup(' Editor', BUTTON_FLAG_EDITOR)
        self._addButtonGroup(' Render', BUTTON_FLAG_RENDER)
        self.GroupEnd()
        return True

    def Command(self, id, msg):
        is_changed = False
        for obj in doc.GetSelection():
            visibility_id = id & 0b1111
            # ボタンID の エディタフラグ が立っている かつ 現在の値と異なる
            if id & BUTTON_FLAG_EDITOR and obj[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] != visibility_id:
                # はじめての変更なら StartUndo
                if not is_changed:
                    doc.StartUndo()
                    is_changed = True
                doc.AddUndo(c4d.UNDOTYPE_CHANGE_NOCHILDREN, obj)
                obj[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = visibility_id
            # ボタンID の レンダーフラグ が立っている かつ 現在の値と異なる
            if id & BUTTON_FLAG_RENDER and obj[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] != visibility_id:
                # はじめての変更なら StartUndo
                if not is_changed:
                    doc.StartUndo()
                    is_changed = True
                doc.AddUndo(c4d.UNDOTYPE_CHANGE_NOCHILDREN, obj)
                obj[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = visibility_id
        if is_changed:
            doc.EndUndo()
        c4d.EventAdd(c4d.MSG_UPDATE)
        return True

if __name__ == '__main__':
    dlg = EasyVisiblitySwitcher()
    dlg.Open(c4d.DLG_TYPE_ASYNC)
    c4d.EventAdd()
