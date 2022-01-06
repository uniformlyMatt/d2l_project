def get_data(row,  key, application_data):
    
    data = application_data[key][row]
    
    data = str(data)
    
    if data =="nan":
        return ""
    else:
        return data

def write_html(row, application_data, year, foldername, write=False):
    
    f = open('template.html', 'r')

    HTML = f.read()
    
    FN = get_data(row, "Person First Name", application_data)
    LN = get_data(row, "Person Last Name", application_data)
    APc = get_data(row, "Acad Prog Code", application_data)
    APlc = get_data(row, "Academic Plan 1 Code", application_data)
    SID =  get_data(row, "Student ID", application_data)
    Q1 = get_data(row, "Are you applying to a combined program?\xa0(Example: MBA/JD) If yes, specify which program.\xa0", application_data)
    Q2 = get_data(row, " Are you looking for\xa0advanced credit? If yes, please list the courses you wish to receive credit for.\xa0 ", application_data)
    RA = get_data(row, "research areas", application_data)
    St = get_data(row, "Statement", application_data)
    GPA = get_data(row, "GPA etc.", application_data)
    Aw = get_data(row, "Awards", application_data)
    Fs = get_data(row, "Financial support", application_data)
    Pub = get_data(row, "Publications", application_data)
    Jobs = get_data(row, "Jobs", application_data)
    Other = get_data(row, "Other", application_data)
    
    Gender = get_data(row, "Gender", application_data)
    Country = get_data(row, "Country", application_data)
    Residence = get_data(row, "Residency", application_data)
    
    Bday = application_data["Birth Date"][row]
    birthday = str(Bday.year) + "-" + str(Bday.month) + "-" + str(Bday.day)
    
    
    HTML = HTML.replace("FirstName", FN)
    HTML = HTML.replace("LastName", LN)
    HTML = HTML.replace("StudentNumber", SID)
    HTML = HTML.replace("AcadProgram", APc)
    HTML = HTML.replace("AcademicPlan", APlc)
    HTML =HTML.replace("Question1", Q1)
    HTML =HTML.replace("Question2", Q2)
    HTML =HTML.replace("RAparagraph", RA)
    HTML =HTML.replace("STparagraph", St)
    HTML =HTML.replace("GPAparagraph", GPA)
    HTML =HTML.replace("AWparagraph", Aw)
    HTML =HTML.replace("FSparagraph", Fs)
    HTML =HTML.replace("JEparagraph", Jobs)
    HTML =HTML.replace("PUBparagraph", Pub)
    HTML =HTML.replace("OTparagraph", Other)
    HTML =HTML.replace("theGender", Gender)
    HTML =HTML.replace("Bday", birthday)
    HTML =HTML.replace("theCountry", Country)
    HTML =HTML.replace("theRes", Residence)
    
    if write:
        fname =  year + LN + FN + str(SID) + ".html"
        with open(foldername + "/" + fname, 'w') as f:
            f.write(HTML)
        f.close()
        
        return FN, LN, SID, APc, APlc, fname
        
    else:
        print(HTML)
        

