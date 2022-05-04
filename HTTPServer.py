from netTools import *
import threading
import PyPDF2
import re
import mqttpublish as mqtt
import time
import random

r = 0
k = 0

def processRequest(s, addr):
    request = getMessage(s)
    directory = "resources/"
    print(request)
    if request[:3] == "GET" or request[:4] == "POST":
        if request[:3] == "GET":
            request = request[3:]
            link_pat = re.compile(" \S*")
            resource = link_pat.match(request)
            resource = resource.group()[1:]
        else:
            request = request[4:]
            link_pat = re.compile(" \S*")
            resource = link_pat.match(request)
            resource = resource.group()[1:]

        if "Greeting.ss235" in resource:
            response = "HTTP/1.0 200 OK\n"
            response += "Content-Type: text/html\n"
            response += "\n"
            try:
                fname_pat = re.compile('fname=[a-zA-Z]*')
                fname = fname_pat.search(request)
                inFile = open(directory + "Greeting.ss235.html", "w")
                inFile.write("""
                <HTML>
                <HEAD>
                <TITLE>Greeting</TITLE>
                </HEAD>
                <BODY>
                <p id="greeting">Hello, """ + fname.group()[6:] + """ </p>
                </BODY>
                </HTML>""")
                inFile.close()
                inFile = open(directory + "Greeting.ss235.html", "r")
                response += inFile.read()
                s.send(response.encode("ascii"))
            except:
                response = "HTTP/1.0 404 Not Found"
                s.send(response.encode("ascii"))

        elif "ThankYou" in resource:
            response = "HTTP/1.0 200 OK\n"
            response += "Content-Type: text/html\n"
            response += "\n"
            # try:
            fav_plant_pat = re.compile('fav_plant=[a-zA-Z]*')
            fav_plant = fav_plant_pat.search(request)
            if "Kumquat" in fav_plant.group():
                global k
                k += 1
            else:
                global r
                r += 1
            inFile = open(directory + "ThankYou.html", "w")
            inFile.write("""
            <HTML>
            <HEAD>
            <TITLE>Greeting</TITLE>
            </HEAD>
            <BODY>
            <p>Thank you for voting!</p>
            <p id="preference">You chose """ + fav_plant.group()[10:] + """ </p>
            <p>Vote Totals:\nKumquats = """ + str(k) + """\nRutabagas = """ + str(r) + """
            </BODY>
            </HTML>""")
            inFile.close()
            inFile = open(directory + "ThankYou.html", "r")
            response += inFile.read()
            s.send(response.encode("ascii"))
            # except:
            #     response = "HTTP/1.0 404 Not Found"
            #     s.send(response.encode("ascii"))
        elif resource[-4:].lower() == "html":
            if "LED-off" in resource:
                mqtt.publish("State=off")
            if "LED-on" in resource:
                mqtt.publish("State=on")
            response = "HTTP/1.0 200 OK\n"
            response += "Content-Type: text/html\n"
            response += "\n"
            try:
                inFile = open(directory + resource, "r")
                response += inFile.read()
                s.send(response.encode("ascii"))
            except:
                response = "HTTP/1.0 404 Not Found"
                s.send(response.encode("ascii"))

        elif resource[-3:].lower() == "js":
            if "LED-submit-off" in resource:
                mqtt.publish("State=off")
            if "LED-submit-on" in resource:
                mqtt.publish("State=on")
            response = "HTTP/1.0 200 OK\n"
            response += "Content-Type: text/javascript\n"
            response += "\n"
            try:
                inFile = open(directory + resource, "r")
                response += inFile.read()
                s.send(response.encode("ascii"))
            except:
                response = "HTTP/1.0 404 Not Found"
                s.send(response.encode("ascii"))

        elif resource[-3:].lower() == "jpg":
            response = "HTTP/1.0 200 OK\n"
            try:
                inFile = open(directory + resource, "rb")
            except:
                response += "Content-Type: image/jpeg\n"
                response += "\n"
                response += "HTTP/1.0 404 Not Found"
                s.send(response.encode("ascii"))
            else:
                response += "Content-Type: image/jpeg\n"
                response += "\n"
                s.send(response.encode("ascii"))
                s.send(inFile.read())

        elif resource[-3:].lower() == "png":
            response = "HTTP/1.0 200 OK\n"
            try:
                inFile = open(directory + resource, "rb")
            except:
                response += "Content-Type: image/png\n"
                response += "\n"
                response += "HTTP/1.0 404 Not Found"
                s.send(response.encode("ascii"))
            else:
                response += "Content-Type: image/png\n"
                response += "\n"
                s.send(response.encode("ascii"))
                s.send(inFile.read())

        elif resource[-3:].lower() == "gif":
            response = "HTTP/1.0 200 OK\n"
            try:
                inFile = open(directory + resource, "rb")
            except:
                response += "Content-Type: image/gif\n"
                response += "\n"
                response += "HTTP/1.0 404 Not Found"
                s.send(response.encode("ascii"))
            else:
                response += "Content-Type: image/gif\n"
                response += "\n"
                s.send(response.encode("ascii"))
                s.send(inFile.read())

        elif resource[-3:].lower() == "bmp":
            response = "HTTP/1.0 200 OK\n"
            try:
                inFile = open(directory + resource, "rb")
            except:
                response += "Content-Type: image/bmp\n"
                response += "\n"
                response += "HTTP/1.0 404 Not Found"
                s.send(response.encode("ascii"))
            else:
                response += "Content-Type: image/bmp\n"
                response += "\n"
                s.send(response.encode("ascii"))
                s.send(inFile.read())

        elif resource.lower() == "favicon.ico":
            response = "HTTP/1.0 200 OK\n"
            try:
                inFile = open(directory + resource, "rb")
            except:
                response += "Content-Type: image/favicon\n"
                response += "\n"
                response += "HTTP/1.0 404 Not Found"
                s.send(response.encode("ascii"))
            else:
                response += "Content-Type: image/favicon\n"
                response += "\n"
                s.send(response.encode("ascii"))
                s.send(inFile.read())

        elif resource[-3:].lower() == "pdf":
            response = "HTTP/1.0 200 OK\n"
            try:
                inFile = open(directory + resource, "rb")
                pdf_reader = PyPDF2.PdfFileReader(inFile)
                for i in range(pdf_reader.numPages):
                    current_page = pdf_reader.getPage(i)
                    response += current_page.extractText()
                s.send(response.encode("ascii"))
            except:
                response += "Content-Type: image/pdf\n"
                response += "\n"
                response += "HTTP/1.0 404 Not Found"
                s.send(response.encode("ascii"))
            else:
                response += "Content-Type: image/pdf\n"
                response += "\n"
                s.send(response.encode("ascii"))
                s.send(inFile.read())

        else:
            response = "HTTP/1.0 403 Forbidden\n\nResources not recogonized"
            s.send(response.encode("ascii"))

    else:
        response = "HTTP/1.0 501 Not Implemented\n"
        response += "\n"
        response += "I'm sorry Dave, I can't do that\n"
        response += "\n"

        s.send(response.encode("ascii"))


    s.close()


def HTTPServer():
    serversocket = socket()

    host = getIPAddress()
    print("Listening on: ", host, ":2008")
    serversocket.bind((host, 2008))

    serversocket.listen()

    while True:
        print("Waiting for connection....")
        clientsocket, addr = serversocket.accept()
        print("Connnection from", addr)

        threading.Thread(target=processRequest, args=(clientsocket, addr)).start()

    serversocket.close()


HTTPServer()
