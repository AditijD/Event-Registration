import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import copy
from pprint import pprint

global er
er = 0
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
# aditij@able-device-139019.iam.gserviceaccount.com
# adidhamija@veritas-345501.iam.gserviceaccount.com
creds = ServiceAccountCredentials.from_json_keyfile_name("veritas-345501-d9348c7ea235.json", scope)
client = gspread.authorize(creds)
fail = list()

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

def write_to_text(fail):
    playsound('C:\\Users\\adi_d\\Documents\\RegDesk\\Check.mp3')
    print("Writing fail to text.")
    fh = open("Fails.txt", "r")
    failold = ast.literal_eval(fh.read())
    fh.close()
    f = open("Fails.txt","w")
    fail = failold + fail
    f.write(str(fail))
    f.close()

def create_sheet(event):
    sheet = client.create(event)
    sheet.share("aditijdhamija1999@gmail.com", perm_type="user", role="owner")
    sheet = client.open(event).sheet1
    sheet.update("A1:I1", [["Timestamp", "Enter Name", "Select Course", "Enter College Name", "Which events are you registering for?", "Phone Number", "Upload Image [Upload on https://imgbb.com/upload and put link]", "Checklist", "Registered"]])

def enter_deets(row_data, event):
    try:
        sheet = client.open(event).sheet1
        sheet.update("A1:I1", [["Timestamp", "Enter Name", "Select Course", "Enter College Name", "Which events are you registering for?", "Phone Number", "Upload Image [Upload on https://imgbb.com/upload and put link]", "Checklist", "Registered"]])
    except:
        create_sheet(event)
        sheet = client.open(event).sheet1
    data = sheet.get_all_records()
    n = len(data)
    range = str("A"+str(int(n+2))+":"+"I"+str(int(n+2)))
    lst = list()
    for i in row_data.values():
        lst.append(i)
    sheet.update(range,[lst])
    newlst = list()
    for items in data:
        nlst = [items['Enter Name'], items['Select Course'], items['Enter College Name'], items['Phone Number']]
        newlst.append(nlst)
    del lst[8]
    del lst[7]
    del lst[6]
    del lst[4]
    del lst[0]
    lstf = enumerate(newlst)
    idxlst = list()
    for idx, item in lstf:
        if item == lst:
            idxlst.append(idx)
    for idx in idxlst:
        print("Removing duplicates.")
        range = str("A"+str(int(idx+2))+":"+"I"+str(int(idx+2)))
        sheet.update(range,[["-","-","-","-","-","-","-","-","-"]])
    print(event, "sheet updated with", row_data['Enter Name']+"'s entry.")
    time.sleep(2)

def return_events(data, i):
    eventlst = data[i]['Which events are you registering for?']
    eventlst = eventlst.replace(" ", "")
    eventlst = eventlst.split(",")
    return eventlst

def sheets_update():
    sheet = client.open("Invictus Form").sheet1
    data = sheet.get_all_records()
    for i in range(0, len(data)):
        eventlst = return_events(data, i)
        if data[i]['Checklist'][:5] == "ERROR" or data[i]['Checklist'] == "":
            continue
        if data[i]['Registered'] != "":
            continue
        datacomp = copy.deepcopy(data)
        datacompn = copy.deepcopy(data)
        del datacompn[i]['Timestamp']
        del datacompn[i]['Registered']
        del datacompn[i]['Which events are you registering for?']
        del datacompn[i]['Upload Image [Upload on https://imgbb.com/upload and put link]']
        del datacomp[i]
        for l in range(0, len(datacomp)):
            del datacomp[l]['Registered']
            del datacomp[l]['Timestamp']
            del datacomp[l]['Which events are you registering for?']
            del datacomp[l]['Upload Image [Upload on https://imgbb.com/upload and put link]']

        if datacompn[i] in datacomp:
            lst = list()
            f = enumerate(datacomp)
            for idx, item in f:
                if item == datacompn[i]:
                    lst.append(idx)

            nlst = list()
            for idx in lst:
                if i>idx:
                    oldreg = return_events(data, idx)
                    for s in oldreg:
                        if s not in nlst:
                            nlst.append(s)
            if len(nlst) == 0:
                for event in eventlst:
                    print(data[i]['Enter Name'], "registered for", event)
                    enter_deets(data[i], event)
                sheet.update_cell(i+2, 9, "Registered")
            else:
                print("Re-registration detected.")
                for a in nlst:
                    if a in eventlst:
                        eventlst.remove(a)
                allevents = eventlst + nlst
                if len(eventlst) != 0:
                    print("New events found.")
                    f = grab_events(data, i)
                    data[i]['Which events are you registering for?'] = f
                    for event in allevents:
                        print(data[i]['Enter Name'], "registered for", event)
                        enter_deets(data[i], event)
                    sheet.update_cell(i+2, 9, "INFO-REREG+EVENTS")
                    print("Sheet updated.")
                else:
                    print("No new events in this entry. What the fuck?")
                    sheet.update_cell(i+2, 9, "INFO-REREG")
                    sheet.update_cell(idx+3, 9, "INFO-REREG")
                    print("Sheet updated.")

        else:
            for event in eventlst:
                print(data[i]['Enter Name'], "registered for", event)
                enter_deets(data[i], event)
            sheet.update_cell(i+2, 9, "Registered")


while True:
    print("Sheet updater is running...")
    sheets_update()
    time.sleep(5)
