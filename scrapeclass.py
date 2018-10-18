#!/usr/bin/python
import sys; sys.dont_write_bytecode = True
import os,imp
import re,optparse
from requests import session
from bs4 import BeautifulSoup

# i don't think this variable is needed any longer
#courseHome = 'https://instruction.gwinnett.k12.ga.us/d2l/lp/ouHome/defaultHome.d2l'
#
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
        tempDict[classId] = {'name' : d.span.text, 
                             'cGrade' : d.span.next_sibling.next_sibling.string, 
                             'link' : str(e)}
  return tempDict
#}}}

#{{{ parseClass
def parseClass(x):
  gradeList = []
  soup = BeautifulSoup(x, 'html.parser')

  # the row with the task type/weight is a sibling of the grade table
  # i'm pulling all the rows from the body
  gradeTable = soup.find("tbody").find_all("tr", recursive=False)

  # if the rows are not paired, exit
  if len(gradeTable) % 2 != 0:
    print "The number of tasks rows do no match the number of grade tables!!"
    exit()

  # i'm going to parse 2 rows at a time per loop and break on the
  # even rows
  rowcntr = 1
  for element in gradeTable:
    if rowcntr % 2 != 0:

      tr1List = []
      for tr1 in element.find_all("td"): 
        tr1List.append(tr1.get_text())

      tr2List = []
      for tr2 in element.find_next_sibling().find("table").find_all("tr"):
        tempList = []
        tds = tr2.find_all("td")
        for td in tds:
          tempList.append(td.get_text())
        tr2List.append(tempList)
      tr1List.append(tr2List)
      gradeList.append(tr1List)
    else:
      True

    rowcntr += 1

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
       print
       print "%10s %-58s %10s" % (indivClass,
                                 classDict[indivClass]['name'],
                                 classDict[indivClass]['cGrade']
                                )
       print "  =============================================================================="
       with open("%s_%s.html" % (kid,indivClass)) as g:
         grades = parseClass(str(g.readlines()))
         for (task,weight,gradeList) in grades:
           print "    -------------------------------------------------------------------------   "
           print '    %-60s%7s' % (task,weight)
           print "    -------------------------------------------------------------------------   "
           for (subj,date,grade,avg) in gradeList:
             print '     %-39s %8s %15s %7s' % (subj,date,grade,avg)
  print

# vim:set ts=2 sw=2 expandtab:
