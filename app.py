from flask import Flask
from flask import jsonify
from flask import request
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


import requests
from bs4 import BeautifulSoup

@app.route('/login', methods=["POST"])
def login_action():
    try:
        data = request.get_json(force=True)
        c = requests.Session()
        c.get("https://webkiosk.jiit.ac.in")
        params ={'x':'',
            'txtInst':'Institute',
            'InstCode':'JIIT',
            'txtuType':'Member Type',
            'UserType':'S',
            'txtCode':'Enrollment No',
            'MemberCode':data['eno'],
            'DOB':'DOB',
            'DATE1':data['dob'],
            'txtPin':'Password/Pin',
            'Password':data['password'],
            'BTNSubmit':'Submit'}
        cook=c.cookies['JSESSIONID']
        cooki=dict(JSESSIONID=cook)
        reslogin=c.post("https://webkiosk.jiit.ac.in/CommonFiles/UserActionn.jsp", data=params,cookies=cooki)
        if "Error1.jpg" in reslogin.content:
            html = BeautifulSoup(reslogin.content, 'html.parser')
            c.close()
            return jsonify(error=html.b.font.text), 500
        else:
            cgpa_resp = c.get("https://webkiosk.jiit.ac.in/StudentFiles/Exam/StudCGPAReport.jsp", cookies=cooki)
            html = BeautifulSoup(cgpa_resp.content, 'html.parser')
            rows = html.find(id = "table-1").tbody.find_all("tr")
            cgpa = []
            for row in rows:
                cols = row.find_all('td')
                temp = {"sem" : cols[0].text.strip(),"cgpa":cols[-1].text.strip(), "sgpa":cols[-2].text.strip()}
                cgpa.append(temp.copy())
            res_info = c.get("https://webkiosk.jiit.ac.in/StudentFiles/PersonalFiles/StudPersonalInfo.jsp", cookies = cooki)
            html = BeautifulSoup(res_info.content, 'html.parser')
            rows = html.find('table').find_all('tr')[10].find_all('td')
            return jsonify(cgpa = cgpa, stu_email = rows[1].text.strip(), par_email = rows[3].text.strip(), curr_sem = cgpa[-1]['sem']),200
            c.close()
    except Exception as e:
        return jsonify(error = repr(e)), 500


if __name__ == "__main__":
    app.run(debug = True)
