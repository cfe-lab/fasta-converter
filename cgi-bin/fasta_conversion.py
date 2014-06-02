#!/opt/local/Library/Frameworks/Python.framework/Versions/2.7/bin/python
import cgi, sys, re

form = cgi.FieldStorage()
forminput = form.getvalue("textinput")
runfasta = form.getvalue("runfasta")
dlfasta = form.getvalue("dlfasta")
runcsv = form.getvalue("runcsv")
dlcsv = form.getvalue("dlcsv")
delim = form.getvalue("delim")
splitfastaheader = form.getvalue("splitfastaheader")
stripwhitespace = form.getvalue("stripwhitespace")

def toFasta(lines, delim="_"):
	lines = [[(delim).join(x.rstrip().split('\t')[:-1]), x.rstrip().split('\t')[-1]] for x in lines.split('\n')]
	return lines

def toCsv(lines):
	result = re.findall('(>.+[\\n\\r\\n])([VLIMFWPSCYNQDEKRH\\*\\-ACTGRYKMSWBHDVN\\:\\n\\r\\n]+)', lines, re.IGNORECASE)
	result = [y.translate(None, '\n\r\n').upper() for x in result for y in x]
	return result

if (runfasta is not None):
	print "Content-Type: text/html"
	print
	print """<!DOCTYPE html><html>
	<head>
	<link rel="stylesheet" href="../css/style.css">
	</head>
	<body><div class="container textoverflow">"""
	result = toFasta(forminput,delim)
	for item in result:
		if (stripwhitespace):
			print ">{}<br>".format(item[0].translate(None, ' '))
		else:
			print ">{}<br>".format(item[0])
		print "{}<br>".format(item[1])
	print """</div></body>
	</html>"""
elif (dlfasta is not None):
	print "Content-Disposition: attachment; filename=\"converted.fa\""
	print "Content-Type:application/octet-stream; name=\"converted.fa\""
	print
	result = toFasta(forminput,delim)
	for item in result:
		if (stripwhitespace):
			print ">{}".format(item[0].translate(None, ' '))
		else:
			print ">{}".format(item[0])
		print "{}".format(item[1])
elif (runcsv is not None):
	print "Content-Type: text/html"
	print
	print """<!DOCTYPE html><html>
	<head>
	<link rel="stylesheet" href="../css/style.css">
	</head>
	<body><div class="container textoverflow"><table>"""
	result = toCsv(forminput)
	header = True
	for item in result:
		if (header is True):
			if (stripwhitespace):
				item = item.translate(None, ' ')
			if (splitfastaheader):
				for i in item[1:].split(delim):
					print "<td>{}</td>".format(i)
			else:
				print "<tr><td>{}</td>".format(item[1:])
			header = False
		else:
			print "<td>{}</td></tr>".format(item)
			header = True
	print "</table></div></body></html>"
elif (dlcsv is not None):
	print "Content-Disposition: attachment; filename=\"converted.csv\""
	print "Content-Type:application/octet-stream; name=\"converted.csv\""
	print
	result = toCsv(forminput)
	isheader = True
	for item in result:
		if (isheader is True):
			if (stripwhitespace):
				item = item.translate(None, ' ')
			header = ''
			if (splitfastaheader):
				header = (',').join(item[1:].split(delim))
			else:
				header = item[1:]
			isheader = False
		else:
			print "{},{}".format(header,item)
			isheader = True
