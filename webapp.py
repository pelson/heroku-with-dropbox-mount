import os
import subprocess
import sys

from concurrent.futures import ThreadPoolExecutor
import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class FileIndex(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ['GET']

    def get(self, path):
        """ GET method to list contents of directory or
        write index page if index.html exists."""

        for index in ['index.html', 'index.htm']:
            index = os.path.join(path, index)
            if os.path.exists(index):
                with open(index, 'rb') as f:
                    self.write(f.read())
                    self.finish()
                    return
        html = self.generate_index(path)
        self.write(html)
        self.finish()

    def generate_index(self, path):
        if path:
            files = os.listdir(path)
        else:
            files = os.listdir('.')
        files = [filename + '/'
                if os.path.isdir(os.path.join(path, filename))
                else filename
                for filename in files]
        html_template = """
        <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN"><html>
        <title>Directory listing for /{{ path }}</title>
        <body>
        <h2>Directory listing for /{{ path }}</h2>
        <hr>
        <ul>
        {% for filename in files %}
        <li><a href="{{ filename }}">{{ filename }}</a>
        {% end %}
        </ul>
        <hr>
        </body>
        </html>
        """
        t = tornado.template.Template(html_template)
        return t.generate(files=files, path=path)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r'/index/(.*)$', FileIndex),
    ])


def start_mount(mount_dir):
    dropbox_token = os.environ.get('DROPBOX_TOKEN')
    if not os.path.exists(mount_dir):
        os.mkdir(mount_dir)
    try:
        subprocess.check_call([sys.executable, 'ff4d/ff4d.py', mount_dir, '-ap', dropbox_token])
    except subprocess.CalledProcessError as err:
        print(err)
        raise


@tornado.gen.coroutine
def async(executor, function, *args, **kwargs):
    yield executor.submit(function, *args, **kwargs)


if __name__ == "__main__":
    app = make_app()
    app.listen(os.environ.get('PORT'))
    print('Get listening... on {}'.format(os.environ.get('PORT', 5000)))
    
    mount_dir = 'wibble'

    thread_pool = ThreadPoolExecutor(1)
    tornado.ioloop.IOLoop.current().spawn_callback(async, thread_pool, start_mount, mount_dir=mount_dir)

    tornado.ioloop.IOLoop.current().start()
