from flask.helpers import url_for
from .models import PutForm,separator
from . import connection
from flask import _app_ctx_stack,render_template,redirect,url_for,request,jsonify
import json 

@connection.route('/put/',methods=["GET","POST"])
def put():
    put_form=PutForm()
    if request.method == 'POST':
        mass_flow=put_form.mass_flow.data
        humidity=put_form.humidity.data
        if hasattr(_app_ctx_stack,'db'):
            db=_app_ctx_stack.db
            newdata={'mass_flow':mass_flow,
                     'humidity': humidity,
                        }
            ret=db.put_data_flow_mass(**newdata)
            if ret:
                _app_ctx_stack.data_available=True
        else:
            raise Exception("Db not find")
        return redirect(url_for('connection.put'))
    return render_template('put.html',put_form=put_form)

@connection.route('/get_all/')
def get_all():
    if hasattr(_app_ctx_stack,'db'):
        db=_app_ctx_stack.db
        data=db.get_all_data_flow_mass()
        context={'data':data,
                 'separator':separator
                }
    else:
        raise Exception('DB not find')
    return render_template('get_all.html',**context)
@connection.route('/data_available/')
def data_available():
    if not hasattr(_app_ctx_stack,'data_available'):
        _app_ctx_stack.data_available=False
    if _app_ctx_stack.data_available:
        _app_ctx_stack.data_available=False
        return redirect(url_for('connection.get_last_data'))
    return "None"
@connection.route('/get_last/')
def get_last_data():
    if hasattr(_app_ctx_stack,'db'):
        db=_app_ctx_stack.db
        data=db.get_last_data_flow_mass()
        context={'data':data,
                 'separator':separator
                }
    else:
        raise Exception('DB not find')
    return render_template('get_last.html',**context)

@connection.route('/clear_all/<key>')
def clear_all(key):
    if key=='cc':
        if hasattr(_app_ctx_stack,'db'):
            db=_app_ctx_stack.db
            db.clear_var()
        return 'Done'
    else:
        return 'error: invalid key'