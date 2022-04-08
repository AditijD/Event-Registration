from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy_garden.zbarcam import ZBarCam
from kivymd.uix.textfield import MDTextField
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

localtime = time.asctime( time.localtime(time.time()) )
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
# aditij@able-device-139019.iam.gserviceaccount.com
creds = ServiceAccountCredentials.from_json_keyfile_dict({
  "type": "service_account",
  "project_id": "bubbly-repeater-345015",
  "private_key_id": "5576db1c9381911fff62a482366c5dfb19ddd52b",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCqNPLlPpulK1oi\n3/pkTlQtMH0Pjw7FGnpRnkAej35ELSCsZXHvUTiWEfbORGMIGVGFSjVeArE72sEW\nQYTWrQNWRdnwo7VXNs4k1hwutUVeEEMbip3fRSfJT29arr3E5cwrNFuGpLXiIdVS\nE6oI13dsVTr+ReWcDbpjEiS+ykNAeN0vY03w8zV4C6oSwegnMKCAy+xxtAlvV1ul\nbhbb16qs1LSwadourHtd0QgNdT1Bv5Tf/aK8ZxhqVm8pi4ylCTqqfeTK0hJzaajR\nM4TewqzBFiaWRD8/sQkZZbLmzzzVAMMADm8mbUTgFwKNGm+BldkLFsV8/PwtSQAF\nd7a1fXf/AgMBAAECggEAOmpevL/+kjLtRg/h82AQssuz+E2Mb6hVN8Lc1cBAwSxN\nzO0qK80P4y16K7O721E5McpUw5Wf919uKnHFIhqSDR9/G4BMIgkcufbECGHNU2m4\nZnDuGu00qPo6yQA1ACkwJ9nZ2b2Y8OnUuU0na85rXcJos1EQ6zyo7gyRkOuBJlRl\nXNpdnQmPrRedP94jv8F21nw58ucdJZSsMsolVAsaGMe+48ZmBSI1K9C5FUjW60BK\nhbWLHvG2I5g01eDeDNX55qjYo+tWarq/9PF7z/2zVuenqlcbFI0SvOM6e64Hbxjb\nZWVYnV30U2V/8KU/E7zPIiokV/zgPNXGE5jxvjIbSQKBgQDemQu3uGkyZMV73yP/\n0QiPxLP4ZqlNC6PFRDPf5MeO4gwR0ehCiJCRBWXb7e2LQVTqjiLC5RAdgywmqRNv\nheX1yyWhHOJRNr7x8RPvpcTK0MKfzgCQNRYJh6+vmKOwjL9HL9q5ucNpKRBEkjQW\nNtbjzcTH6uEzW8ZEEQVLrDdkVwKBgQDDv1YBUR2ZoQRVjbnaixQRH05VzzJpV3OI\n0a9OldwCALkJLBRpSpZVBkvOT3tDqup4uAbPJnXua2u47B6WTfpzt6pygYJCoiA/\n7h+V7yuzdf9I9Sfp41fNzb/JFAnhR0SaLqBeUaGpTU4OIhWdKomRiBUq0/z+pp0I\nRoTrsSGAmQKBgDpMQvFe7s4v7ji+/CKnkGJ21ducp4JyJfYoIp3kwQ7+zMJuAzJJ\nqfMRQtgSvD/YYHD9wMTiURIppIqLhXeTzeJNzhEgC3XRrLiYtuvwslWbzx0jSqp5\n/MeKLc0DYPuAISh3tAUoTbFg+825rMKUojsPTRY+wbQ9uPNiscxb0jYJAoGAa0uu\nxewDkJlM+eREsoE3j6ccVjbLiChyYNWnBSlpvgNNabSqv4gt3Q8lcEHq7A18lo0w\n1k1bqUNieaubnIHDvbg4Cqnoj8O0b7aDw7ikuKr+MqyGo1KFZ37XGE4OmFhrRyQ1\nrV2LgnSoS2Dtfge5/nacO6yVabREMSwOYe7m0UkCgYEArKlC2QOI5zPb7puAS5u4\nfAz5QLvT/myOgL6XAoKiEFM/EKWkqcgjluRwLs7dAm8x5mqNT4QquU6a2ltW1y2b\n06EM+SUFA4UM8fKqcgazzGGQFqkiWePhvgGHHK4BOlYYANKJq5/nz0yDYpi7Yk7S\n/pMhQyPHn/b7Q2odDbY3fFw=\n-----END PRIVATE KEY-----\n",
  "client_email": "adi-97@bubbly-repeater-345015.iam.gserviceaccount.com",
  "client_id": "116306172601376419132",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/adi-97%40bubbly-repeater-345015.iam.gserviceaccount.com"
}
, scope)
client = gspread.authorize(creds)

global SportName
global NameName
screen_helper = """
ScreenManager:
    transition: NoTransition
    MenuScreen:
    ConfigScreen:
    QRScreen:
<MenuScreen>:
    name: 'menu'
    MDRectangleFlatButton:
        text: 'Config'
        pos_hint: {'center_x':0.5,'center_y':0.6}
        on_press: root.manager.current = 'Config'
    MDRectangleFlatButton:
        text: 'QR'
        pos_hint: {'center_x':0.5,'center_y':0.5}
        on_press: root.manager.current = 'QR'

<ConfigScreen>:
    name: 'Config'
    MDTextField:
        hint_text: "Enter the name of the sport."
        helper_text: "Once all rows are filled, click the back button to save."
        helper_text_mode: "on_focus"
        id: Sport
        text: ''
        pos_hint: {'center_x':0.5,'center_y':0.4}
    MDTextField:
        hint_text: "Please enter your first name."
        helper_text: "Greetings from Aditij! Hope you're enjoying volunteering for Invictus."
        helper_text_mode: "on_focus"
        id: Name
        text: ''
        pos_hint: {'center_x':0.5,'center_y':0.6}
    MDRectangleFlatButton:
        text: 'Back'
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press:
            root.manager.current = 'menu'
            root.set_text()


<QRScreen>:
    name: 'QR'
    BoxLayout:
        orientation: "vertical"
        ZBarCam:
            id:grcodecam
        MDRectangleFlatButton:
            id: fname
            size_hint: None, None
            size: root.width, 50
            text: ' '.join([str(symbol.data) for symbol in grcodecam.symbols])
            on_press:
                root.PressbtnQR(self, ' '.join([str(symbol.data) for symbol in grcodecam.symbols]))
        MDRectangleFlatButton:
            id: Index
            size_hint: None, None
            size: root.width, 50
            text: "Go Back"
            on_press: root.manager.current = 'menu'
"""


class MenuScreen(Screen):
    pass


class ConfigScreen(Screen):
    global SportName
    global NameName
    def set_text(self):
        global SportName
        global NameName
        print(self.ids)
        index = self.ids.Sport
        SportName = index.text.title()
        index = self.ids.Name
        NameName = index.text.title()
    pass


class QRScreen(Screen):
    global SportName
    global NameName
    def PressbtnQR(self, instances, values):
        global SportName
        global NameName
        print(str(values))
        s = values[1:].split("'")
        for f in s:
            if f == ', ':
                s.remove(f)
            if f == '"[' or f == ']"':
                s.remove(f)
        print(s)
        try:
            sheet = client.open(SportName).sheet1
            data = sheet.get_all_records()
            for i in data:
                del i["Checklist"]
                del i["Registered"]
                del i["Timestamp"]
                i["Phone Number"] = str("+" + str(i["Phone Number"]))
            nlst = list()
            for a in data:
                alst = list()
                for f in a.values():
                    alst.append(f)
                nlst.append(alst)
            if s in nlst:
                Index = self.ids.Index
                Index.text = "The participant is registered on Google."
                index = nlst.index(s)
                print(index)
                message = str("QR code was scanned by " + NameName + " on" + localtime[3:-5])
                sheet.update_cell(index+2, 5, message)
            else:
                del s[3]
                newlst = list()
                for i in data:
                    newlst.append(i["Which events are you registering for?"])
                    del i["Which events are you registering for?"]
                    nlst = list()
                    for a in data:
                        alst = list()
                        for f in a.values():
                            alst.append(f)
                        nlst.append(alst)
                    if s in nlst:
                        idx = nlst.index(s)
                        l = newlst[idx]
                        print(l)
                        Index = self.ids.Index
                        Index.text = l
                        return
                Index = self.ids.Index
                Index.text = "The participant is NOT registered on Google."
        except Exception as e:
            Index = self.ids.Index
            Index.text = "Please check your config file."

    pass


# Create the screen manager
sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(ConfigScreen(name='Config'))
sm.add_widget(QRScreen(name='QR'))


class DemoApp(MDApp):
    global SportName
    global NameName
    def build(self):
        global SportName
        screen = Builder.load_string(screen_helper)
        return screen

if __name__ == '__main__':
    DemoApp().run()
