import eventlet
import socketio

# create a Socket.IO server
sio = socketio.Server()

# wrap with a WSGI application
app = socketio.WSGIApp(sio)

@sio.on('my custom event')
def another_event(sid, data):
    pass

@sio.event
def connect(sid, environ, auth):
    """User authentication and mapping between user entities and SID"""
    print(auth)
    print('connect ', sid)
    with sio.session(sid) as session:
        session['username'] = auth['username']


@sio.on('message')
def newMessage(sid, data):
    session = sio.get_session(sid)
    print('+++NEW MESSAGE+++')
    print(f'sid: {sid}')
    print(f'username: {session["username"]}')
    print(f'data: {data}')
    print('---NEW MESSAGE---')
    sio.emit('message', {'username': session["username"],'message': data['message']}, skip_sid=sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5001)), app)
