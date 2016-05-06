# -*- coding: utf-8 -*-
import hashlib
import os, sys  
import re
import urlparse

import cherrypy
import twilio.twiml

# The script
part0 = [
	("f1", "Hello. Thank you for calling The Real Estate Survey. The Real Estate Survey attempts to quantify the effect of the real estate market on today's arts ecosystem by specifically looking at the percentage of income that is absorbed by the real estate market from both individuals and organizations in the arts."),
	(1,),
	("f1", "Almost every art worker that answered our earlier survey, lives with housing stress. We want to know about you. Do you spend more than 30% of your income on rent? Press 1 for YES and 2 for NO followed by the pound key.", "/q01")
]

part0_again = [
	("f1", "Press 1 if you spend more than 30% of your income on housing and 2 if you do not, followed by the pound key.", "/q01")
]

part1a = [
	("f2", "We're sorry to hear that."),
	(1,),
	("f1", "You have housing stress too."),
	(1,),
	("m", "I don't see the problem. House prices were too low before."), 
	(1,),
	("f1", "Who are you?"),
	("m", "When property values go up, everyone wins. This city is more livable than ever."),
	(1,),
	("f1", "Do you know who this is?"),
	(1,),
	("f2", "I have no idea. I have never seen him before."),
	(2,),
	("f1", "Look, let's just move on. Caller: you have housing stress. Have you ever felt gastrointestinal discomfort when you think of paying your rent..."),
	(1,),
	("f2", "But do you think it is possible to separate housing stress from other forms of stress? Finding a job, bringing up children, medical problems, caring for ageing parents, that ache in your tooth."),
	(1,),
	("f1", "Yes, it is all connected, isn't it? Caller, have you experienced sleep disturbances or changes in sleeping habits in the past 6 months? Press 1 for yes and 2 for no, followed by the pound key.", "/q02")
]

part1b = [
	("f2", "That's great for you. You do not have housing stress."),
	(1,),
	("f1", "Are you sure that you are an art worker? Please press "),
	(1,),
	("m", "Everyone is an artist. This is a city of creativity and innovation."), 
	(1,),
	("f1", "Who are you?"),
	("m", "I'm just someone who thinks we can have it all. Art, coffee, high property values. We just need to work together."),
	(1,),
	("f1", "Do you know who this is?"),
	(1,),
	("f2", "I have no idea. I have never seen him before."),
	(2,),
	("f1", "Look, let's just move on. Caller: you do not have housing stress, but that doesn't mean you are care free."),
	(1,),
	("f2", "It isn't possible to separate housing stress from other forms of stress. Finding a job, bringing up children, medical problems, caring for ageing parents, that ache in your tooth."),
	(1,),
	("f1", "Yes, it is all connected, isn't it? Caller, have you experienced sleep disturbances or changes in sleeping habits in the past 6 months? Press 1 for yes and 2 for no, followed by the pound key.", "/q02")
]

part1_again = [
	("f1", "If you have you experienced sleep disturbances or changes in sleeping habits in the past 6 months please Press 1, otherwise press 2, followed by the pound key.", "/q02")
]

part2 = [
	("f1", "Have you experienced regular muscle tension, muscle aches, fatigue or headache over the past 6 months? Press 1 for Yes and 2 for No, followed by the pound key.", "/q03")
]

part2_again = [
	("f1", "If you have you experienced regular muscle tension, muscle aches, fatigue or headache over the past 6 months please press 1, and otherwise press 2.", "/q03")
]

part3 = [
	("f1", "Have you had gastrointestinal problems over the past 6 months? Press 1 for Yes and 2 for No.", "/q04")
]

part4 = [
	("m", "You should really be recommending exercise to the callers. Perhaps a visit to their doctor where they might get a prescription."),
	(1,),
	("f2", "We feel stress individually, but it is a collective problem."),
	(1,),
	("f1", "If your stress makes you feel alone, press 1. If it makes you feel solidarity with other people experiencing similar symptoms, press 2.", "/q05")
]

part4_again = [
	("f1", "Does your stress makes you feel alone? Then press 1. If not, if it makes you feel solidarity with other people experiencing similar symptoms, press 2.", "/q05")
]

part5 = [
	("f1", "The feeling of loneliness keeps us apart."),
	(1,),
	("f2", "Yes, loneliness is another symptom of stress. The idea of the collective has been put under so much stress that is has broken into pieces. We think of ourselves as individuals."),
	(1,),
	("f1", "We imagine that our trouble is ours alone. We think we are at fault."),
	(1,),
	("m", "What's going on here? I think you are all getting carried away. If you are having trouble paying your rent then you could just ask for some more hours, or get a second job, or a better paying job."),
	(1,),
	("f1", "Some people are working more hours than ever and still struggling."),
	(2,),
	("f2", "The size of the average loan taken out by a first-time buyer in New South Wales has swelled by more than 43% in the past four years (and 20% in the past year alone). Wages in the same period increased only 10%."),
	(1,),
	("m", "If your wages aren't what you want them to be, maybe it's time to go back to school. Learn a new skill."),
	(1,),
	("f1", "People have been learning new skills. They have been going into debt. There is only so far that people can stretch."),
	(1,),
	("m", "Research shows that multitasking is highly beneficial for anyone's creativity and promotes business growth, no matter if they are an artist, designer or entrepreneur."),
	(2,),
	("f1", "Caller, do you have a clear and consistent boundary between your place of work and your place of non-work? Press 1 for YES and 2 for NO followed by the pound key.", "/q06")
]

part5_again = [
	("f1", "Do you have a clear and consistent boundary between your place of work and your place of non-work? Press 1 for YES and 2 for NO.", "/q06")
]

part6 = [
	("f1", "And do you have a clear and consistent division between your time of work and your time of non-work? Press 1 for YES and 2 for NO.", "/q07")
]

part6_again = [
	("f1", "Press 1 if you have a clear and consistent division between your time of work and your time of non-work. Press 2 if you do not.", "/q07")
]

part7 = [
	("f2", "Most of us are so used to being stressed, we often don't know we are stressed until we are at the breaking point."),
	(1,),
	("m", "You can't feel stress. You are a robot."),
	(1,),
	("f1", "But stress is already a concept that is applied to inanimate materials. Stress tests allow machines, software, bridges, and airplanes to be operated at their limits."),
	(2,),
	("m", "Caller, you can do anything if you want to. The only limits are in your mind."),
	(1,),
	("f2", "Why don't we ask about the caller's limits rather than telling them?"),
	(1,),
	("f1", "But how can someone know their own limits?"),
	(1,),
	("m", "I know no limits."),
	(2,),
	("f1", "Of course you don't. You were born on the finish line."),
	(2,),
	("f2", "Caller, we apologize for the interruptions. Perhaps this question can't be quantified so I will just ask if you believe that there is a breaking point where the rent becomes too high and it causes individuals and communities irreparable harm?"),
	(1,),
	("f1", "Do we even need to ask? Isn't the answer obvious."),
	(1,),
	("m", "Of course you do. Caller, press 1 if you believe that a healthy economy and a great real estate market go hand in hand raising all boats. Press 2 if you are a skeptic or a communist or something like these ladies.", "/q08")
]

part7_again = [
	("m", "Press 1 if you believe that a healthy economy and a great real estate market go hand in hand raising all boats. Press 2 if you do not, followed by the pound key", "/q08")
]

part8a = [
	("m", "That's right. The caller and I are just everyday people who think we can have it all. Art, coffee, high property values. We just need to work together."),
	(1,),
	("f1", "You would never work with anyone. You prefer gated communities, private police forces, and putting your money offshore."),
	(1,),
	("m", "What I mean is that we shouldn't be fighting. That attitude is the problem."),
	(1,),
	("f1", "The problem is with capitalism and private property."),
	(1,),
	("m", "Oh not this again. Haven't we been down this road before? Press 1 if we have been down this road before and press 2 if it is something new.", "/q09"),
]

part8b = [
	("m", "Caller, I am not sure you pressed the correct button."),
	(2,),
	("f1", "The problem is not with the caller. The problem is with capitalism and private property."),
	(1,),
	("m", "Oh not this again. Haven't we been down this road before? Press 1 if we have been down this road before and press 2 if it is something new.", "/q09"),
]

part8_again = [
	("m", "Press 1 if we have been down this road before or press 2 if it is something new.", "/q09"),
]

part9a = [
	("f1", "Have we really been here before?"),
	(2,),
	("f2", "There are fewer and fewer factories here."),
	(1,),
	("f1", "Jobs are disappearing. Work is being automated."),
	(1,),
	("f2", "Just look at us."),
	(1,),
	("f1", "More people compete for fewer opportunities."),
	(1,),
	("f2", "And all the profit flows into investments - like real estate."),
	(1,),
	("f1", "Which is then rented back to you for a huge chunk of the wages you do receive."),
	(1,),
	("m", "Look, what you need to do is get in the game. If you save up a bit, work hard, buy some property, then it will be a great investment. Just trust us. We create the jobs. We sell you the houses. We loan you money. If you just follow the rules, and don't get sick, you can get ahead."),
	(2,),
	("f1", "If you want to get ahead press 1, if you can't stand the imperative to get ahead press 2.", "/q10"),
]

part9b = [
	("f1", "I agree, there is something new happening."),
	(2,),
	("f2", "There are fewer and fewer factories here."),
	(1,),
	("f1", "Jobs are disappearing. Work is being automated."),
	(1,),
	("f2", "Just look at us."),
	(1,),
	("f1", "More people compete for fewer opportunities."),
	(1,),
	("f2", "And all the profit flows into investments - like real estate."),
	(1,),
	("f1", "Which is then rented back to you for a huge chunk of the wages you do receive."),
	(1,),
	("m", "Look, what you need to do is get in the game. If you save up a bit, work hard, buy some property, then it will be a great investment. Just trust us. We create the jobs. We sell you the houses. We loan you money. If you just follow the rules, and don't get sick, you can get ahead."),
	(2,),
	("f1", "If you want to get ahead press 1, if you can't stand the imperative to get ahead press 2.", "/q10"),
]

part9_again = [
	("f1", "If you want to get ahead press 1, if you can't stand the imperative to get ahead press 2 followed by the pound key.", "/q10"),
]


part10a = [
	("m", "That's my boy."),
	(1,),
	("f1", "We know nothing about the gender of the caller."),
	(3,),
	("m", "Whatever. Look, if there is no incentive, then nothing will happen. There will be no medicine, no great works of art."),
	(2,),
	("f2", "There are other incentives besides profit."),
	(1,),
	("m", "But none are as efficient. And the disincentive of poverty and imprisonment should really be enough to get the caller to hang up now and start innovating."),
	(1,),
	("f1", "Innovation is just finding new ways to steal more from the poor."),
	(1,),
	("m", "Innovation is the body's response to stress. Stress is not bad. Stress is good. Stress makes you stronger."),
	(1,),
	("f2", "Housing stress does not make anyone stronger except those applying the stress."),
	(1,),
	("f1", "If you agree that housing stress makes people stronger press 1. If you feel that the metaphor of stress might not work across the full range of its implications, press 2.", "/q11")
]

part10b = [
	("f2", "There are other incentives besides profit."),
	(1,),
	("m", "But none are as efficient. And the disincentive of poverty and imprisonment should really be enough to get the caller to hang up now and start innovating."),
	(1,),
	("f1", "Innovation is just finding new ways to steal more from the poor."),
	(1,),
	("m", "Innovation is the body's response to stress. Stress is not bad. Stress is good. Stress makes you stronger."),
	(1,),
	("f2", "Housing stress does not make anyone stronger except those applying the stress."),
	(1,),
	("f1", "If you agree that housing stress makes people stronger press 1. If you feel that the metaphor of stress might not work across the full range of its implications, press 2.", "/q11")
]

part10_again = [	
	("f1", "Does housing stress makes people stronger? If you think it does, press 1. If not, press 2.", "/q11")
]

part11 = [
	("f1", "Stress as a metaphor has its limits."),
	(1,),
	("f2", "For one, it implies that you can just get over it by making yourself stronger."),
	(2,),
	("f1", "But perhaps we should take it seriously for a moment. If there is housing stress, then it also means that there is a breaking point."),
	(3,),
	("f2", "A moment of failure."),
	(1,),
	("f1", "Broken people. "),
	(2,),
	("f2", "Yes. But that is only if you think of stress as an individual symptom and not a collective problem."),
	(2,),
	("f1", "So what you are saying is broken"),
	("f2", "Yes, is housing itself. Real estate. Property."),
	(2,),
	("m", "Caller, you know better than this. Ignore these"),
	("f2", "Be quiet."), 
	(1,),
	("f1", "Is there some way out? Sharing our homes?"),
	("f2", "A rent strike?"),
	("f1", "Occupying vacant buildings?"),
	("f2", "Paying rent to the traditional owners of the land?"),
	("f1", "Is real estate the only way?"),
	(2,),
	("m", "I'm sorry. Your call has been disconnected.")
]

# Three characters
def f1(o, text):
	o.say(text , language="en-AU")

def f2(o, text):
	o.say(text , language="en-IN")

def m(o, text):
	o.say(text)

# Pause some length
def pause(o, duration):
	o.pause(length=duration)

# Convenience function for saying something
def say(o, c, text):
	if c=='f1':
		f1(o, text)
	elif c=='f2':
		f2(o, text)
	else:
		m(o, text)

# Loops through a list of tuples which define a script
def say_script(o, script):
	for line in script:
		if len(line)==1:
			pause(o, line[0])
		elif len(line)==2:
			say(o, line[0], line[1])
		elif len(line)==3:
			with o.gather(action=line[2], finishOnKey='#') as g:
				say(g, line[0], line[1])


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
		say_script(r, part0)
		return str(r)

	@cherrypy.expose
	def q01(self, *args, **kwargs):
		r = twilio.twiml.Response()
		if not 'Digits' in kwargs:
			r.say("Ooops there is a problem")
			return str(r)
		d = kwargs['Digits']
		if d=="1": # YES
			say_script(r, part1a)
		elif d=="2":
			say_script(r, part1b)
		else:			
			say_script(r, part0_again)
		return str(r)

	@cherrypy.expose
	def q02(self, *args, **kwargs):
		r = twilio.twiml.Response()
		if not 'Digits' in kwargs:
			r.say("Ooops there is a problem")
			return str(r)
		d = kwargs['Digits']
		if d=="1": # YES
			say_script(r, part2)
		elif d=="2":
			say_script(r, part2)
		else:			
			say_script(r, part1_again)
		return str(r)


	@cherrypy.expose
	def q03(self, *args, **kwargs):
		r = twilio.twiml.Response()
		if not 'Digits' in kwargs:
			r.say("Ooops there is a problem")
			return str(r)
		d = kwargs['Digits']
		if d=="1": # YES
			say_script(r, part3)
		elif d=="2":
			say_script(r, part3)
		else:			
			say_script(r, part2_again)
		return str(r)

	@cherrypy.expose
	def q04(self, *args, **kwargs):
		r = twilio.twiml.Response()
		if not 'Digits' in kwargs:
			r.say("Ooops there is a problem")
			return str(r)
		d = kwargs['Digits']
		if d=="1": # YES
			say_script(r, part4)
		elif d=="2":
			say_script(r, part4)
		else:			
			say_script(r, part3)
		return str(r)


	@cherrypy.expose
	def q05(self, *args, **kwargs):
		r = twilio.twiml.Response()
		if not 'Digits' in kwargs:
			r.say("Ooops there is a problem")
			return str(r)
		d = kwargs['Digits']
		if d=="1": # YES
			say_script(r, part5)
		elif d=="2":
			say_script(r, part5)
		else:			
			say_script(r, part4_again)
		return str(r)

	@cherrypy.expose
	def q06(self, *args, **kwargs):
		r = twilio.twiml.Response()
		if not 'Digits' in kwargs:
			r.say("Ooops there is a problem")
			return str(r)
		d = kwargs['Digits']
		if d=="1": # YES
			say_script(r, part6)
		elif d=="2":
			say_script(r, part6)
		else:			
			say_script(r, part5_again)
		return str(r)

	@cherrypy.expose
	def q07(self, *args, **kwargs):
		r = twilio.twiml.Response()
		if not 'Digits' in kwargs:
			r.say("Ooops there is a problem")
			return str(r)
		d = kwargs['Digits']
		if d=="1": # YES
			say_script(r, part7)
		elif d=="2":
			say_script(r, part7)
		else:			
			say_script(r, part6_again)
		return str(r)

	@cherrypy.expose
	def q08(self, *args, **kwargs):
		r = twilio.twiml.Response()
		if not 'Digits' in kwargs:
			r.say("Ooops there is a problem")
			return str(r)
		d = kwargs['Digits']
		if d=="1": # YES
			say_script(r, part8a)
		elif d=="2":
			say_script(r, part8b)
		else:			
			say_script(r, part7_again)
		return str(r)

	@cherrypy.expose
	def q09(self, *args, **kwargs):
		r = twilio.twiml.Response()
		if not 'Digits' in kwargs:
			r.say("Ooops there is a problem")
			return str(r)
		d = kwargs['Digits']
		if d=="1": # YES
			say_script(r, part9a)
		elif d=="2":
			say_script(r, part9b)
		else:			
			say_script(r, part8_again)
		return str(r)

	@cherrypy.expose
	def q10(self, *args, **kwargs):
		r = twilio.twiml.Response()
		if not 'Digits' in kwargs:
			r.say("Ooops there is a problem")
			return str(r)
		d = kwargs['Digits']
		if d=="1": # YES
			say_script(r, part10a)
		elif d=="2":
			say_script(r, part10b)
		else:			
			say_script(r, part9_again)
		return str(r)

	@cherrypy.expose
	def q10(self, *args, **kwargs):
		r = twilio.twiml.Response()
		if not 'Digits' in kwargs:
			r.say("Ooops there is a problem")
			return str(r)
		d = kwargs['Digits']
		if d=="1": # YES
			say_script(r, part11)
		elif d=="2":
			say_script(r, part11)
		else:			
			say_script(r, part10_again)
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
