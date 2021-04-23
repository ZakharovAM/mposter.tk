from main import MainObject
from flask import Response
from pprint import pprint as p
from flask import render_template as RT
from flask import Flask, request,session,current_app,g
app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def test():
    items, res, user, password, src, dst = None, list(), None, None, None, None
    if request.method == 'POST':
        if request.get_json():
            items = dict(request.get_json());
            user = items.pop('login')
            password = items.pop('password')
            src = items.pop('src')
            dst = items.pop('dst')
            p(f'''items: {items} 
                  user: {user} 
                  password: {password} 
                  src: {src} 
                  dst: {dst}''')
        p(items)
        p(type(items))
        for item, pasw in items.items():
            task = MainObject(src, dst, [item, pasw])
            if task.state:
                res.append((item, "True"))
                task.prep()
                task.cp()
                task.logout()
            else:
                res.append((item, "False"))

        p(f"ANSWER:{res}")
        return Response(f'{res}', status=200, mimetype='application/json')

    if request.method == 'GET':
        return RT('page.html')

@app.errorhandler(404)
def page_not_found(e):
    return RT('404.html') , 404

@app.errorhandler(500)
def internal_server_erros(e):
    return RT('500.html'), 500
