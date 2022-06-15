"""
    Creation date: 2021-06-11 14:33:20
    Tampa, FL

    @author: Manuel Machado
    @version: 0.0.1

    Description: The purpose of this program is to display a simple "Hello World" message from a web server
                 using python's web microservice Flask.

"""

from flask import Flask

application = Flask(__name__)


@application.route('/api/helloworld', methods=['GET'])
def helloWorld():
    return '<html> ' \
           '<head>' \
           '<title>Simple Hello World API</title>' \
           '</head>' \
           '<body>' \
           '<h1>API Programming with Flask</h1> ' \
           '<p>Hello, World</p>' \
           '</body>' \
           '</html>'


if __name__ == '__main__':
    application.run(port=8088, host='localhost', debug=True)
