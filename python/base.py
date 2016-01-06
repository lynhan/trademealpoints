# base.py 
# contains handler
# twizzley 

import webapp2
import jinja2
import random
from trademealpoints import template_dir

# init jinja 
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


# render page with jinja
class Handler(webapp2.RequestHandler):
    def __init__(self, request=None, response=None):
        """init handler"""
        super(Handler, self).__init__(request, response)
        self.jinja = jinja_env

    def write(self, *a, **kw):
        """write string to response stream"""
        self.response.out.write(*a, **kw)

    def render_str(self, template_name, **params):
        """render jinja2 template and return as string"""
        template = jinja_env.get_template(template_name)
        return template.render(params)

    def render(self, template, **kw):
        """render jinja2 template using dictionary or keyword arguments"""
        self.write(self.render_str(template, **kw))

    def redirect_to(self, route_name, *args, **kwargs):
        """redirect to a URI that corresponds to route_name."""
        self.redirect(self.uri_for(route_name, *args, **kwargs))
