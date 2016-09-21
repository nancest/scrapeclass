#!/usr/bin/python
import os,imp
import re,optparse
from requests import session
from bs4 import BeautifulSoup

courseHome = 'https://instruction.gwinnett.k12.ga.us/d2l/lp/ouHome/defaultHome.d2l'
eclassBase = 'https://apps.gwinnett.k12.ga.us/'

#{{{ command line config options and arguments
usage = "%prog [-c file] [-s] [-f]"
parser = optparse.OptionParser(usage)
parser.add_option("-c", "--conffile",
                dest="conffile",
                type="string",
                action="store",
                metavar="CONFIG",
                help="points to config file instead of using ~/.scrapeclass_config.py")
parser.add_option("-f", "--file",
                dest="cachedfile",
                type="string",
                action="store",
                metavar="CACHEDFILE",
                help="reads previously created html file with -s instead of making a web call")
parser.add_option("-s", "--save",
                dest="save",
                action="store_true",
                default=False,
                help="saves the dashboard to an html file")
(options, args) = parser.parse_args()
#}}}

#{{{ parseDash
def parseDash(x):
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
#}}}

#{{{ parseClass
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
#}}}
  
#{{{refreshGrades
def refreshGrades(k):
  eclassDashboard = eclassBase + 'dca/student/dashboard'
  eclassLogin     = eclassBase + 'pkmslogin.form'
  eclassUrl       = eclassBase + 'dca/student/'
  with session() as c:
    c.post(eclassLogin,data=config.logins[k])
    dashPage = c.get(eclassDashboard)
    with open("%s_dashboard.html" % (kid), "w") as of:
      of.write(dashPage.content)
    d = parseDash(dashPage.content)
    for e in d:
      f = c.get(eclassUrl + d[e]['link'])
      with open("%s_%s.html" % (k,e), "w") as of:
        of.write(f.content)
#}}}

if options.conffile:
  config = imp.load_source('config',options.conffile)
else:
  config = imp.load_source('config',os.path.expanduser('~/.scrapeclass_config.py'))

for kid in sorted(config.logins):
  print kid
  refreshGrades(kid)
  with open("%s_dashboard.html" % (kid)) as f:
    classDict = parseDash(str(f.readlines()))
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

# vim:set ts=2 sw=2 expandtab:
