from pprint import pformat
from cgi import parse_qsl, escape

def application(environ, start_response):
    output = ['<p>WSGI!</p>']

    output.append('Post:')
    output.append('<form method="post">')
    output.append('<input type="text" name = "test">')
    output.append('<input type="submit" value="Send">')
    output.append('</form>')

    d = parse_qsl(environ['QUERY_STRING'])
    if environ['REQUEST_METHOD'] == 'POST':
        output.append('<h1>Post  data:</h1>')
        output.append(pformat(environ['wsgi.input'].read()))

    if environ['REQUEST_METHOD'] == 'GET':
        if environ['QUERY_STRING'] != '':
            output.append('<h1>Get data:</h1>')
            for ch in d:
                output.append(' = '.join(ch))
                output.append('<br>')

    output_len = sum(len(line) for line in output)
    start_response('200 OK', [('Content-type', 'text/html'),
                              ('Content-Length', str(output_len))])
    return output
