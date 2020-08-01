#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import os
import time
import cgi
import threading
import random

html = '<html>{}<head><title>Uno Game</title></head><body link="red" vlink="red" alink="red"><font face="Courier">{}</font></body></html>'
redirect='<meta http-equiv="refresh" content="2;http://194.87.103.226:100/${}">'
dictcolors={'R':'red','G':'green','B':'blue','Y':'yellow'}

base=[]
player=[[],[],[]]
table=[]
currentcolor="red"

def GenerateBase():
	for i in range(0,10):
		base.append(str(i)+'R')
		base.append(str(i)+'Y')
		base.append(str(i)+'G')
		base.append(str(i)+'B')
	for i in ['+','-','&']:
		base.append(i+'R')
		base.append(i+'G')
		base.append(i+'B')
		base.append(i+'Y')
	for i in range(0,4):
		base.append('??')
		base.append('?4')
	for i in range(0,8):
		player[0].append(base.pop(random.randint(0,len(base)-1)))
		player[1].append(base.pop(random.randint(0,len(base)-1)))
		player[2].append(base.pop(random.randint(0,len(base)-1)))
	table.append(base.pop(random.randint(0,len(base)-1)))

def GeneratePage(index):
	global currentcolor
	st='Player {}\r\n'.format(index)

	index_=0
	st+='<p>'
	while index_<3:
		if int(index)==index_:
			st+='<p>'
			for i in player[int(index)]:
				st+='\t<a href="{}">{}</a>'.format('/@'+index+i,i)
		else:
			st+='<p>[Player {}: {} cards]'.format(index_,len(player[index_]))
		
		index_+=1
	print(currentcolor)

	if not (table[0]=='??' or table[0]=='?4'):
		print('123')
		currentcolor=dictcolors[table[0][1]]
	st+='<p><font color="{}"><b>Table: </b></a></font>'.format(currentcolor)
	for i in range(0,len(table)):
		if i==0:
			st+=' <b>'+table[i]+'</b>'
		else:
			st+=' <i>'+table[i]+'</i>'

	st+='<p><a href="/={}">Base: {} cards</a>'.format(index,len(base))
	if table[0]=='??' or table[0]=='?4':
		st+='<br>Choose color: <a href="/!{0}R">Red </a><a href="/!{0}Y">Yellow </a><a href="/!{0}G">Green </a><a href="/!{0}B">Blue </a>'.format(index)
	return st

class ServerHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		print(self.path[0:2])
		if self.path[0:2] == "/$":
			global currentcolor
			playername=int(self.path[2])
			st=GeneratePage(str(playername))

			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.send_header('Connection', 'closed')
			self.end_headers()

			self.wfile.write(html.format(redirect.format(str(playername)),st).encode('utf-8'))

		elif self.path[0:2] == "/=":
			playername=int(self.path[2])
			player[playername].append(base.pop(random.randint(0,len(base)-1)))

			st=GeneratePage(str(playername))

			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.send_header('Connection', 'closed')
			self.end_headers()

			self.wfile.write(html.format(redirect.format(str(playername)),st).encode('utf-8'))

		elif self.path[0:2] == "/!":
			playername=int(self.path[2])
			cur=self.path[3]
			currentcolor=dictcolors[cur]
			print(currentcolor)
			st=GeneratePage(str(playername))

			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.send_header('Connection', 'closed')
			self.end_headers()

			self.wfile.write(html.format(redirect.format(str(playername)),st).encode('utf-8'))

		elif self.path[0:2] == "/@":
			playername=int(self.path[2])
			card=self.path[3:]
			print(playername)
			print(card)
			print(player[playername])
			pos=player[playername].index(card)
			table.insert(0,player[playername].pop(pos))

			st=GeneratePage(str(playername))

			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.send_header('Connection', 'closed')
			self.end_headers()

			self.wfile.write(html.format(redirect.format(str(playername)),st).encode('utf-8'))
		else:
			self.send_error(404, "Page Not Found {}".format(self.path))
		print('#'+self.path+'#Answered')
		#print(self.headers)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	"""
	"""


def server_thread(port):
	server_address = ('194.87.103.226', port)
	httpd = ThreadedHTTPServer(server_address, ServerHandler)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()

if __name__ == '__main__':
	port = 100
	GenerateBase()
	print(base)
	print(player)

	print("Starting server at port %d" % port)
	server_thread(port)
