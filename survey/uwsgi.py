import cherrypy
from survey.server import Survey

def application(environ, start_response):
	conf = {}
	cherrypy.config.update({
		'server.socket_port': 8101
	})
	app = cherrypy.tree.mount(Survey(), '/')
	return cherrypy.tree(environ, start_response)
