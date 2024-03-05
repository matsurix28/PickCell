from kivy import platform
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

currentActivity = None
CLS_Activity = None
CLS_Intent = None
ImagesMedia = None

REQUEST_GALLERY = 1
MediaStore_Images_Media_DATA = '_data'

class FileSelect(BoxLayout):
    def select_path(self, filepath):
        if filepath != '':
            self.image1.source = filepath
            self.image1.reload()

    def open_file_dialog(self, *args):
        if platform == 'android':
            from android import activity
            intent = CLS_Intent(CLS_Intent.ACTION_PICK, ImagesMedia.EXTERNAL_CONTENT_URI)
            currentActivity.startActivityForResult(intent, REQUEST_GALLERY)
            activity.bind(on_activity_result=self.on_activity_result)

    def on_activity_result(self, request_code, result_code, intent):
        try:
            if request_code == REQUEST_GALLERY:
                if result_code == CLS_Activity.RESULT_CANCELED:
                    Clock.schedule_once(lambda dt: self.select_path(''), 0)
                    return
                if result_code != CLS_Activity.RESULT_OK:
                    raise NotImplementedError('Unknown result_code "{}"'.format(result_code))
                selectedImage = intent.getData()
                filePathColumn = [MediaStore_Images_Media_DATA]
                cursor = currentActivity.getContentResolver().query(selectedImage, filePathColumn, None, None, None)
                cursor.moveToFirst()
                columnIndex = cursor.getColumnIndex(filePathColumn[0])
                selectedPicturePath = cursor.getString(columnIndex)
                Clock.schedule_once(lambda dt: self.select_path(selectedPicturePath), 0)
                cursor.close()
        finally:
            from android import activity
            activity.unbind(on_activity_result=self.on_activity_result)

class MyApp(App):
    def build(self):
        if platform == 'android':
            Window.bind(on_keyboard=self.key_input)
            from jnius import autoclass, cast
            global currentActivity
            global CLS_Activity
            global CLS_Intent
            global ImagesMedia

            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
            CLS_Activity = autoclass('android.app.Activity')
            CLS_Intent = autoclass('android.content.Intent')
            ImagesMedia = autoclass('android.provider.MediaStore$Images$Media')

            from android.permissions import Permission, request_permissions
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.MANAGE_DOCUMENTS])

        return FileSelect()
    
    def key_input(self, window, key, scancode, codepoint, modifier):
        if key == 27:
            return True
        else:
            return False

if __name__ == '__main__':
    MyApp().run()