#!/usr/bin/python
from requests import session
from bs4 import BeautifulSoup

eclass_login = 'https://apps.gwinnett.k12.ga.us/pkmslogin.form'
dashboard    = 'https://apps.gwinnett.k12.ga.us/dca/student/dashboard'
course_home  = 'https://instruction.gwinnett.k12.ga.us/d2l/lp/ouHome/defaultHome.d2l'

logins = {
       ‘firstchild':{ 'login-form-type': 'pwd', 'username': ‘ECLASSID', 'password': 'learnGRADE'},
       ’secondchild':{ 'login-form-type': 'pwd', 'username': 'ECLASSID', 'password': 'learnGRADE'},
       ’thirdchid':{ 'login-form-type': 'pwd', 'username': 'ECLASSID', 'password': 'learnGRADE'}
}

def parse_dash(x):
       #print(dash_page.headers) #print(dash_page.text) #print(dash_page.content)
       soup = BeautifulSoup(x, 'html.parser')
       print soup.find(id="grades")


for kid in logins:
   print kid
   #print logins[kid]
#    with session() as c:
#        c.post(eclass_login, data=logins[kid])
#        dash_page = c.get(dashboard)
#        parse_dash(dash_page.content)
#        #with open("%s_dashboard.html" % (kid), "w") as of:
#        #    of.write(dash_page.content)
   with open("%s_dashboard.html" % (kid)) as f:
       parse_dash(f)
