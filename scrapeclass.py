#!/usr/bin/python
from requests import session
from bs4 import BeautifulSoup
import re

courseHome = 'https://instruction.gwinnett.k12.ga.us/d2l/lp/ouHome/defaultHome.d2l'
eclassBase = 'https://apps.gwinnett.k12.ga.us/'

def parse_dash(x):
  tempDict = {}
  soup = BeautifulSoup(x, 'html.parser')
  a = soup.find(id='grades')
  b = BeautifulSoup(str(a), 'html.parser')
  c = b.find_all("li")
  for d in c:
    if 'ungraded' not in str(d):
      e = d.a.get('href')
      f = re.search(r'.+=(\d+)&ts', str(e))
      if f:
        classId = f.group(1)
        tempDict[classId] = {'name' : d.span.get_text(), 'cGrade' : d.span.next_sibling.get_text(),
                             'link' : str(e)}
  return tempDict

def parseClass(x):
  gradeList = []
  soup = BeautifulSoup(x, 'html.parser')
  tbls = soup.find_all("table", {'class': 'tasks-inner-table'})
  for tbl in tbls:
    trs = tbl.find_all("tr")
    for tr in trs:
      tempList = []
      tds = tr.find_all("td")
      for td in tds:
        tempList.append(td.get_text())
      gradeList.append(tempList)
  return gradeList
  
def refreshGrades(k):
  eclassDashboard = eclassBase + 'dca/student/dashboard'
  eclassLogin     = eclassBase + 'pkmslogin.form'
  eclassUrl       = eclassBase + 'dca/student/'
  with session() as c:
    c.post(eclassLogin,data=logins[k])
    dash_page = c.get(eclassDashboard)
    with open("%s_dashboard.html" % (kid), "w") as of:
      of.write(dash_page.content)
    d = parse_dash(dash_page.content)
    for e in d:
      f = c.get(eclassUrl + d[e]['link'])
      with open("%s_%s.html" % (k,e), "w") as of:
        of.write(f.content)

logins = []
with open('kids', 'r') as f:
  logins = eval(f.read())

for kid in sorted(logins):
  print kid
  refreshGrades(kid)
  with open("%s_dashboard.html" % (kid)) as f:
    classDict = parse_dash(str(f.readlines()))
    for indivClass in classDict:
       print '  ' + indivClass + ' - ' + classDict[indivClass]['name'] + ' - ' + classDict[indivClass]['cGrade']
       with open("%s_%s.html" % (kid,indivClass)) as g:
         grades = parseClass(str(g.readlines()))
         for items in grades:
           print '    ',
           for i in items:
             print i,
           print 
  print
