#!/usr/bin/python
import tornado.ioloop
import tornado.web

from wtforms.fields import IntegerField
from wtforms.validators import Required
from wtforms_tornado import Form

class SumForm(Form):

    a = IntegerField(validators=[Required()])
    b = IntegerField(validators=[Required()])

class SumHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

    def post(self):
        form = SumForm(self.request.arguments)
        if form.validate():
            self.write(str(form.data['a'] + form.data['b']))
        else:
            self.set_status(400)
            self.write("" % form.errors)

application = tornado.web.Application([
    (r"/", SumHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()