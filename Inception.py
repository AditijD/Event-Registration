from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import selenium.webdriver
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import qrcode
from docxtpl import DocxTemplate
from docxtpl import InlineImage
from docx.shared import Mm
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, GappedSquareModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask, ImageColorMask
from PIL import Image
from docx2pdf import convert
from playsound import playsound
import os
import urllib.request
import requests
from bs4 import BeautifulSoup as bs
from mtcnn.mtcnn import MTCNN
from matplotlib import pyplot
import cv2
import shutil
import copy

try:
    global er
    er = 0

    def return_events(data, i):
        eventlst = data[i]['Which events are you registering for?']
        eventlst = eventlst.replace(" ", "")
        eventlst = eventlst.split(",")
        return eventlst

    def grab_events(data, s):
        eventlst = return_events(data, s)
        datacomp = copy.deepcopy(data)
        datacompn = copy.deepcopy(data)
        for i in range(0, len(data)):
            del datacompn[i]['Timestamp']
            del datacompn[i]['Registered']
            del datacompn[i]['Which events are you registering for?']
            del datacompn[i]['Upload Image [Upload on https://imgbb.com/upload and put link]']
            del datacompn[i]['Checklist']
        del datacomp[s]
        for l in range(0, len(datacomp)):
            del datacomp[l]['Registered']
            del datacomp[l]['Checklist']
            del datacomp[l]['Timestamp']
            del datacomp[l]['Which events are you registering for?']
            del datacomp[l]['Upload Image [Upload on https://imgbb.com/upload and put link]']
        if datacompn[s] in datacomp:
            lst = list()
            f = enumerate(datacomp)
            for idx, item in f:
                if item == datacompn[s]:
                    lst.append(idx)
            nlst = list()
            for idx in lst:
                if s>idx:
                    oldreg = return_events(data, idx)
                    for x in oldreg:
                        if x not in eventlst:
                            eventlst.append(x)
                str = ""
                for item in eventlst:
                    str = str+item+", "
                f = str[:-2]
            return f
        else:
            events = return_events(data, s)
            str = ""
            for item in events:
                str = str+item+", "
                f = str[:-2]
            return f

    def sort_items():
        files = os.listdir()
        pdflst = list()
        imglst = list()

        for file in files:
            if ".pdf" in file:
                pdflst.append(file)
            if ".jpg" in file:
                imglst.append(file)

        for file in pdflst:
            if os.path.isfile("./PDFs/" + file):
                t=0
                k=0
                while t==0:
                    k+=1
                    if os.path.isfile("./PDFs/" + file[:-4]+str(k)+file[-4:]):
                        continue
                    shutil.move("./"+file, "./PDFs/"+file[:-4]+str(k)+file[-4:])
                    t=1
            else:
                shutil.move("./"+file, "./PDFs/",file)


        for file in imglst:
            if os.path.isfile("./Images/" + file):
                t=0
                k=0
                while t==0:
                    k+=1
                    if os.path.isfile("./Images/" + file[:-4]+str(k)+file[-4:]):
                        continue
                    shutil.move("./"+file, "./Images/"+file[:-4]+str(k)+file[-4:])
                    t=1
            else:
                shutil.move("./"+file, "./Images/", file)

    def cropper(name):
        global er
        m = 0.25
        print("Attempting cropping.")
        pixels = pyplot.imread(name+".jpg")
        detector = MTCNN()
        result = detector.detect_faces(pixels)
        if len(result)>1:
            a = 0
            for item in result:
                _, _, w, h = item['box']
                if w*h > a:
                    a = w*h
                    finresult = [item]
        elif len(result)==0:
            print("Error, face not detected for", name)
            er = 2
            return
        else:
            finresult=result
        img = cv2.imread(name+".jpg")
        h, w, channels = img.shape
        x1, y1, width, height = finresult[0]['box']
        x2, y2 = x1 + width, y1 + height
        xm1, xm2, ym1, ym2 = scalar(m, x1, x2, y1, y2)
        xn1, xn2, yn1, yn2 = squarify(xm1, xm2, ym1, ym2)
        while xn1<0 or xn2>w or yn1<0 or yn2>h:
            m = m-0.01
            xm1, xm2, ym1, ym2 = scalar(m, x1, x2, y1, y2)
            xn1, xn2, yn1, yn2 = squarify(xm1, xm2, ym1, ym2)
        crop_img = img[yn1:yn2, xn1:xn2]
        cv2.imwrite(name+"RS.jpg", crop_img)
        print("Cropping Succesful!")

    def scalar(m, x1, x2, y1, y2):
        width = x2-x1
        xn2 = int(x2 + m*width)
        xn1 = int(x1 - m*width)
        height = y2-y1
        yn2 = int(y2 + m*height)
        yn1 = int(y1 - m*height)
        return xn1, xn2, yn1, yn2

    def squarify(xn1, xn2, yn1, yn2):
        mwidth = xn1+(xn2-xn1)/2
        mheight = yn1+(yn2-yn1)/2
        hwidth = (xn2-xn1)/2
        hheight = (yn2-yn1)/2
        if mwidth > mheight:
            yn2 = int(mheight+hwidth)
            yn1 = int(mheight-hwidth)
        if mheight > mwidth:
            xn2 = int(mwidth+hheight)
            xn1 = int(mwidth-hheight)
        return xn1, xn2, yn1, yn2

    def image_dl(name, url):
        response = requests.get(url)
        lst = list()
        soup = bs(response.content, 'html.parser')
        links = []
        for link in soup.findAll('a'):
            links.append(link.get('href'))
        for f in links:
            if f is None:
                continue
            if '.jpg' in f:
                url = f

        r = urllib.request.urlopen(url)
        with open(name + ".jpg", "wb") as f:
            f.write(r.read())

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    #image = Image.open('logo.png').resize((10, 10))
    #img_1.paste(image, (140, 140, 150, 150))
    #img_1.save("my_qrcode.png")

    chrome_options = Options()
    chrome_options.add_argument("user-data-dir=C:\\Users\\adi_d\\AppData\\Local\\Google\\Chrome\\User Data\\NewProfile")
    chrome_options.add_argument("no-sandbox")
    chrome_options.add_argument('--disable-dev-shm-usage')
    #chrome_options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    n = 0
    i = 0
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    # aditij@able-device-139019.iam.gserviceaccount.com
    creds = ServiceAccountCredentials.from_json_keyfile_name("able-device-139019-a2fb9e4ecd39.json", scope)
    client = gspread.authorize(creds)
    fail = list()
    def WhatsApp(name, college, course, events, phone, message, url, i):
        global er
        link = "https://web.whatsapp.com/send?phone={}&text&source&data&app_absent".format(phone)
        driver.get(link)
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
        code = sheet.row_values(i)[1:7]
        code[3] = events
        print(code)
        qr.add_data(code)
        img_1 = qr.make_image(image_factory=StyledPilImage, module_drawer=GappedSquareModuleDrawer(), color_mask=ImageColorMask(color_mask_path = "Invictus.png"))
        img_1.save(name+" QR.jpg")
        try:
            image_dl(name, url)
            cropper(name)
        except Exception as e:
            playsound('C:\\Users\\adi_d\\Documents\\RegDesk\\Check.mp3')
            print(name+"'s image could not be downloaded/processed because", e)
        doc = DocxTemplate("Temp.docx")
        qrimage = InlineImage(doc, image_descriptor=name+" QR.jpg", width=Mm(86), height=Mm(86))
        #event = events.replace(", ", "\n")
        if os.path.isfile(name + "RS.jpg"):
            dlimage = InlineImage(doc, image_descriptor=name+"RS.jpg", width=Mm(86), height=Mm(86))
            er = 0
            context = {
                    'name': name,
                    'kimo': dlimage,
                    'course': course,
                    'college': college,
                    #'events': event,
                    'events': events,
                    'var': qrimage
                }
        else:
            print("Image not found.")
            if er != 2:
                er = 1
            context = {
                    'name': name,
                    'college': college,
                    'course': course,
                    #'events': event,
                    'events': events,
                    'var': qrimage
                }
        doc.render(context)
        doc.save(name + ".docx")
        convert(name + ".docx")
        os.remove(name + ".docx")
        try:
            try:
                while True:
                    retry = driver.find_element_by_xpath('//div[@class="_20C5O _2Zdgs"]')
                    retry.click()
            except:
                WebDriverWait(driver, 15).until(lambda driver: driver.find_element(By.XPATH, '//div[@title = "Type a message"]'))
            filepath = str("C:\\Users\\adi_d\\Documents\\RegDesk\\" + name + ".pdf")
            WebDriverWait(driver, 60).until(lambda driver: driver.find_element(By.XPATH, '//div[@title = "Attach"]'))
            message_box = driver.find_element_by_xpath('//div[@title = "Type a message"]')
            message_box.send_keys(message)
            message_box.send_keys(Keys.ENTER)
            WebDriverWait(driver, 120).until(lambda driver: driver.find_element(By.XPATH, '//div[@title = "Attach"]'))
            time.sleep(1)
            attachment_box = driver.find_element_by_xpath('//div[@title = "Attach"]')
            attachment_box.click()
            WebDriverWait(driver, 120).until(lambda driver: driver.find_element(By.XPATH, '//input[@accept = "*"]'))
            document_box = driver.find_element_by_xpath('//input[@accept = "*"]')
            document_box.send_keys(filepath)
            WebDriverWait(driver, 120).until(lambda driver: driver.find_element(By.XPATH, '//span[@data-icon = "send"]'))
            send_button = driver.find_element_by_xpath('//span[@data-icon = "send"]')
            send_button.click()
            time.sleep(1)
            try:
                while True:
                    wait = driver.find_element_by_xpath('//span[@data-testid = "msg-time"]')
            except:
                print("WhatsApp message sent to", name)
            if er == 1:
                fail.append([name, college, course, events, phone, message])
                sheet.update_cell(i, 8, "ERROR-NOIMG")
            elif er == 2:
                fail.append([name, college, course, events, phone, message])
                sheet.update_cell(i, 8, "ERROR-NOFACE")
            else:
                sheet.update_cell(i, 8, "Checked")
        except Exception as e:
            print("Could not send message as", e, "occured.")
            fail.append([name, college, course, events, phone, message])
            sheet.update_cell(i, 8, "ERROR-CHECKWA")
            write_to_text(fail)

    def write_to_text(fail):
        playsound('C:\\Users\\adi_d\\Documents\\RegDesk\\Check.mp3')
        print("Writing fail to text.")
        f = open("Fails.txt","a")
        f.write(str(fail))
        f.close()

    sheet = client.open("Invictus Form").sheet1
    data = sheet.get_all_records()

    def phone_proper(num, i):
        num = num.replace(" ", "")
        newnum = num.strip()
        if not newnum.startswith('+91'):
            newnum = str('+91') + num
        if len(newnum) == 13:
            if newnum != num:
                print("Making appropriate changes to document for", num, "to", newnum)
                numput = "'"+newnum
                sheet.update_cell(i, 6, str(numput))
                data[i-2]['Phone Number'] = newnum
            return newnum
        else:
            return None

    def do_row(i):
        row = sheet.row_values(i)
        phone = row[5]
        phone = phone_proper(phone, i)
        name = row[1]
        nam = name.replace(" ", "")
        if nam == "":
            print("Empty name kyun daala hai bhai. Aap bauhat zyaada peete ho kya?")
            sheet.update_cell(i, 8, "ERROR-NONAME")
        events = grab_events(data, i-2)
        link = row[6]
        course = row[2]
        college = row[3]
        message = "Hi ", name, ", please find attached your pass for Invictus 2022. Please ensure that the pass mentions all the events that you have paid for. Hope you enjoy Invictus!"
        if phone == None:
            print("Wrong number provided by", name, "of", college + ".")
            fail.append([name, college, course, events, phone, message])
            sheet.update_cell(i, 8, "ERROR-CHECKNUM")
            write_to_text(fail)
        else:
            WhatsApp(name, college, course, events, phone, message, link, i)
        sort_items()

    def check_records():
        print("Attempting to check records.")
        n = len(data)
        f = sheet.col_values(8)
        if len(f) != n+1:
            for i in range(len(f)+1, n+2):
                do_row(i)
        for items in f:
            if items == "":
                idx = f.index(items)
                do_row(idx+1)
        sort_items()

    check_records()

    while True:
        sheet = client.open("Invictus Form").sheet1
        data = sheet.get_all_records()
        n = len(data)
        for items in data:
            if items['Checklist'] == "":
                check_records()
        if i == 0:
            i = n
        if n > i:
            print("New records found!")
            playsound("C:\\Users\\adi_d\\Documents\\RegDesk\\BellSmol.mp3")
            check_records()
            i=n
        else:
            print("Nothing new.")
            time.sleep(5)

except Exception as e:
    print("Exception occured: ", e, ". Quitting Selenium.")
    driver.close()
