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
		r.say("Hello. Thank you for calling The Real Estate Survey. The Real Estate Survey attempts to quantify the effect of the real estate market on today's arts ecosystem by specifically looking at the percentage of income that is absorbed by the real estate market from both individuals and organizations in the arts.", language="en-IN")
		r.pause(length=1)
		with r.gather(action="/q01", finishOnKey='#') as g:
			g.say("Almost every art worker that answered our earlier survey, lives with housing stress. We want to know about you. Do you spend more than 30% of your income on rent? Press 1 for YES and 2 for NO followed by the pound key.", language="en-IN")
		return str(r)

	@cherrypy.expose
	def q01(self, *args, **kwargs):
		r = twilio.twiml.Response()
		if not 'Digits' in kwargs:
			r.say("Ooops there is a problem")
			return str(r)
		d = kwargs['Digits']
		if d=="1": # YES
			r.say("We're sorry to hear that.", language="en-IN")
			r.say("You have housing stress too.", language="en-AU")
			r.pause(length=1)
			r.say("I don't see the problem. House prices were too low before.")
			r.say("Who are you?", language="en-AU")
			r.say("When property values go up, everyone wins. This city is more livable than ever.")
			with r.gather(action="/q02", finishOnKey='#') as g:
				g.say("OK, let's just move on. How many hours do you think that you have to work to pay your rent? You can enter the number followed by the pound key.", language="en-IN")
		elif d=="2":
			r.say("That's great for you. You do not have housing stress.", language="en-IN")
			r.pause(length=1)
			r.say("Are you sure that you are an art worker? Please press ", language="en-AU")
			r.say("Everyone is an artist. This is a city of innovation and creativity.")
			r.say("Who are you?", language="en-AU")
			r.say("I'm just someone who thinks we can have it all. Art, coffee, high property values. We just need to work together")			
			with r.gather(action="/q03", finishOnKey='#') as g:
				g.say("OK, let's just move on. Do you consider yourself an art worker, press 1 for YES and 2 for NO.", language="en-IN")
		else:			
			with r.gather(action="/q01", finishOnKey='#') as g:
				 g.say("Press 1 if you spend more than 30% of your income on rent and press 2 if you do not, followed by the pound key", voice="en-IN")		
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
