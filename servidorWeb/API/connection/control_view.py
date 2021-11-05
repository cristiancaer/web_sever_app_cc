from flask.helpers import url_for
from .models import PutFlowForm,separator,PutHumidityForm
from . import connection
from flask import _app_ctx_stack,render_template,redirect,url_for,request,jsonify,session
import json 
@connection.route('/put_humidity/',methods=['GET','POST'])
def put_humidity():
    put_form=PutHumidityForm()
    if hasattr(_app_ctx_stack,'db'):
        db=_app_ctx_stack.db
    if request.method=='POST':
        db.put_data_humidity(put_form.humidity.data)
        return redirect(url_for('connection.get_humidity'))
    return render_template('put_humidity.html',put_form=put_form)
@connection.route('/get_humidity/')
def get_humidity():
    if hasattr(_app_ctx_stack,'db'):
        db=_app_ctx_stack.db
        humidity=db.get_humidity()
    else:
        humidity=None
    return humidity
@connection.route('/put_flow/',methods=["GET","POST"])
def put_flow():
    put_form=PutFlowForm()
    if request.method == 'POST':
        mass_flow=put_form.mass_flow.data
        if hasattr(_app_ctx_stack,'db'):
            db=_app_ctx_stack.db
            newdata={'mass_flow':mass_flow,
                        }
            ret=db.put_data_flow_mass(**newdata)
        else:
            raise Exception("Db not find")
        return redirect(url_for('connection.put_flow'))
    return render_template('put_flow.html',put_form=put_form)

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
@connection.route('/data_flow_available/')
def data_flow_available():
    if hasattr(_app_ctx_stack,'db'):
        db=_app_ctx_stack.db
        new_len_data_flow=db.len_data_flow()
        data_available=not session.get('data_flow_available')==new_len_data_flow
    if data_available:
        session['data_flow_available']=new_len_data_flow
        return redirect(url_for('connection.get_last_data_flow'))
    return "None"
@connection.route('/get_last_flow/')
def get_last_data_flow():
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