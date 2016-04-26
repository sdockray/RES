# -*- coding: utf-8 -*-
import hashlib
import os, sys  
import re
import urlparse

import cherrypy
import twilio.twiml

# The survey
class Survey(object):
	@cherrypy.expose
	def default(self, *args, **kwargs):
		resp = twilio.twiml.Response()
		resp.say("Hello? Is it me you're looking for?")
		return str(resp)

	@cherrypy.expose
	def operator(self, *args, **kwargs):
                r = twilio.twiml.Response()
                r.say("Hello. Thank you for calling The Real Estate Survey. We'd like to ask you a few questions, this time about your work. For all answers, please press the number and then the pound key.", language="en-IN") #voice="woman")
		r.pause(length=1)
		with r.gather(action="/branch01", finishOnKey='#') as g:
			g.say("Do you consider yourself an art worker? Press 1 for Yes and 2 for No", voice="man")
                return str(r)

	@cherrypy.expose
	def branch01(self, *args, **kwargs):
		r = twilio.twiml.Response()
		if not 'Digits' in kwargs:
			r.say("Ooops there is a problem")
			return str(r)
		d = kwargs['Digits']
		if d=="1":
			r.say("Interesting. Does that mean that you make enough money from art to meet your basic needs?", voice="male")
		elif d=="2":
			r.say("OK. I'm not sure we have anything to talk about.", voice="male")
			r.say("That's not true!", voice="female")
		else:
			with r.gather(action="/branch01", finishOnKey='#') as g:
				 g.say("Press 1 if you consider yourself an arts worker and press 2 if you do not, followed by the pound key", voice="man")		
		return str(r)

# Starting things up
if __name__ == '__main__':
	try:
		cherrypy.config.update({
			'server.socket_port': 8101,
		})
		app = cherrypy.tree.mount(Survey(), '/')
		cherrypy.quickstart(app)
	except:
		print "Survey server couldn't start :("
