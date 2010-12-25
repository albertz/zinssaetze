#!/usr/bin/python

from datetime import *
from decimal import *
decimal = Decimal
import re, sys
from math import log

def userinput(text, convfn, default = None):
	cachefn = __file__ + ".cache"
	try:
		cache = eval(open(cachefn).read())
	except:
		cache = {}
	if text in cache: default = cache[text]
	while True:
		try:
			sys.stdout.write(text)
			if default:
				sys.stdout.write(" (" + default + ")")
			sys.stdout.write(": ")
			s = raw_input()
			if s == "" and default != None: s = default
			c = convfn(s)
			cache[text] = s
			open(cachefn, "w").write(repr(cache))
			return c
		except KeyboardInterrupt:
			print "Abbruch"
			quit()
		except Exception, e:
			print "Fehler bei Eingabe:", e

def strtodate(s):
	m = re.match("^([0-9]+) +([0-9]+) +([0-9]+)$", s)
	year, month, day = m.groups()
	return date(int(year), int(month), int(day))

def strtodaymonth(s):
	m = re.match("^([0-9]+) +([0-9]+)$", s)
	month, day = m.groups()
	return int(month), int(day)

def strtobool(s):
	if s.lower() in ["yes", "ja", "y", "j", "1"]: return True
	if s.lower() in ["no", "nein", "n", "0"]: return False
	raise Exception, repr(s) + " is not a boolean value"
	
def inccreaseyears(d, c = 1):
	return date(d.year + c, d.month, d.day)

def iterdaymonth(start, end, daymonth):
	currentdaymonth = date(start.year, daymonth[0], daymonth[1])
	if currentdaymonth < start: currentdaymonth = inccreaseyears(currentdaymonth)
	while currentdaymonth <= end:
		yield currentdaymonth
		currentdaymonth = inccreaseyears(currentdaymonth)

def count(iter):
	c = 0
	for i in iter: c += 1
	return c
	
def countdaymonth(start, end, daymonth):
	return count(iterdaymonth(start, end, daymonth))

start = userinput("Start", strtodate)
end = userinput("Ende", strtodate)

print "Zeitdifferenz:", end - start

kaufpreis = userinput("Kaufpreis", decimal)
endwert = userinput("Endwert", decimal)

zinstermin = userinput("Zinstermin", strtodaymonth)
ztcount = countdaymonth(start, end, zinstermin)

festerzinsatz = userinput("Fester Zinsatz?", strtobool)
if festerzinsatz:
	zinssatz = userinput("Zinssatz", decimal)
	gewinn = endwert - kaufpreis + ztcount * zinssatz * kaufpreis
else:
	zinssaetze = {}
	lastzinssatzinput = None
	for d in iterdaymonth(start, end, zinstermin):
		zinssaetze[d] = userinput("Zinsatz am " + str(d), decimal, default = lastzinssatzinput)
		lastzinssatzinput = str(zinssaetze[d])
	gewinn = endwert - kaufpreis + sum( zinssatz * kaufpreis for zinssatz in zinssaetze.itervalues() )
		
print "Gewinn:", gewinn

# kaufpreis * (1.0 + effz) ^ ztcount = gewinn + kaufpreis
# -> (gewinn + kaufpreis) / kaufpreis = (1.0 + effz) ** ztcount
# -> ((gewinn + kaufpreis) / kaufpreis) ** (1.0/ztcount) = 1.0 + effz
effz = float((gewinn + kaufpreis) / kaufpreis) ** (1.0/ztcount) - 1.0
print "Effektivzinsatz:", effz

