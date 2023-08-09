import os
from ftplib import FTP
from time import time
import six
import json
from chameleon import PageTemplate


BIGTABLE_ZPT = """\
<table xmlns="http://www.w3.org/1999/xhtml"
xmlns:tal="http://xml.zope.org/namespaces/tal">
<tr tal:repeat="row python: options['table']">
<td tal:repeat="c python: row.values()">
<span tal:define="d python: c + 1"
tal:attributes="class python: 'column-' + %s(d)"
tal:content="python: d" />
</td>
</tr>
</table>""" % six.text_type.__name__

ftp = FTP("localhost")
ftp.login(user='ftpuser', passwd='ftpuser')
ftp.cwd('files')

def main(args):
    num_of_rows = int(args['num_of_rows'])
    num_of_cols = int(args['num_of_cols'])


    start = time()
    tmpl = PageTemplate(BIGTABLE_ZPT)

    data = {}
    for i in range(num_of_cols):
        data[str(i)] = i

    table = [data for x in range(num_of_rows)]
    options = {'table': table}

    data = tmpl.render(options=options)
    latency = time() - start
    with open('sample.html', 'w+') as html_file:
        html_file.write(data)
        ftp.storbinary('STOR ' + 'sample.html', html_file)
        html_file.close()

    os.remove('sample.html')

    return {'latency': latency}


'''
sample_payload
{'num-of-rows':'10','num-of-cols':'10'}
To Run:
python -i chameleon-test.py
main({'num_of_rows':'10','num_of_cols':'10','output_path':'../output'})
'''