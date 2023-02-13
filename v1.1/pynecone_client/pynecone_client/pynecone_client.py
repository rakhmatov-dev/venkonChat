"""Welcome to Pynecone! This file outlines the steps to create a basic app."""
from pcconfig import config
import pynecone as pc
import socketio

# ## ++SIO
# sio = socketio.Client()
# authData = {
#     'token': '<Token>'
# }

# @sio.event
# def connect():
#     print('I\'m connected!')

# @sio.event
# def connect_error(data):
#     print('The connection failed!')

# @sio.event
# def disconnect():
#     print('I\'m disconnected!')  
#     authData["token"] = ChatState.name
#     authData["username"] = ChatState.name
#     sio.connect('http://localhost:5001', auth = authData, namespaces=[f"/{ChatState.name}"])
#     ChatState.connected = True

# # @sio.event
# # def message(data):
# #     print('I received a message!')

# @sio.on('message')
# def on_message(data):
#     ChatState.messages += [f'{data["username"]}: {data["message"]}']


# ## --SIO

class SocketIOClient(pc.Base):
    sio: socketio.Client = socketio.Client()
    # def __init__(self, reconnection=True, reconnection_attempts=0,
    #              reconnection_delay=1, reconnection_delay_max=5,
    #              randomization_factor=0.5, logger=False, serializer='default',
    #              json=None, handle_sigint=True, **kwargs):
        
    #     socketio.Client.__init__(self, reconnection, reconnection_attempts,
    #                             reconnection_delay, reconnection_delay_max,
    #                             randomization_factor, logger, serializer,
    #                             json, handle_sigint)


class ChatState(pc.State):

    ## ++SIO
    _mySocketClient: socketio.Client = socketio.Client()
    authData: dict = {
        'token': '<Token>'
    }

    @_mySocketClient.event
    def connect():
        print('I\'m connected!')

    @_mySocketClient.event
    def connect_error(data):
        print('The connection failed!')

    @_mySocketClient.event
    def disconnect():
        print('I\'m disconnected!')  
        ChatState.authData["token"] = ChatState.name
        ChatState.authData["username"] = ChatState.name
        ChatState._mySocketClient.connect('http://localhost:5001', auth = ChatState.authData)
        ChatState.connected = True

    @_mySocketClient.on('message')
    def on_message(data):
        ChatState.messages += [f'{data["username"]}: {data["message"]}']

    ## --SIO

    login: str = ''
    password: str = ''
    name: str = ''

    connected: bool = False

    messages: list = []
    newMessage: str = ""

    def setLogin(self, text):
        self.login = text

    def setPassword(self, text):
        self.password = text

    def setName(self, text):
        self.name = text

    def setNewMessage(self, text):
        self.newMessage = text

    def knockKnock(self):
        self.authData["token"] = self.name
        self.authData["username"] = self.name
        self._mySocketClient.connect('http://localhost:5001', auth = self.authData)
        self.connected = True
        if self.connected:
            return pc.redirect(
            "/chat"
            )

    def send(self):
        self._mySocketClient.emit('message', {'message': self.newMessage})
        self.messages += [f"{self.name}: {self.newMessage}"]
        self.newMessage = ""


def renderMessage(message):
    """Render a message in the messages list."""
    return pc.list_item(
        pc.hstack(
            pc.box(message, width="100%")
        )
    )


def index():
    return pc.hstack(
        pc.vstack (
            pc.markdown("## Login Page"),
            pc.input(placeholder=ChatState.name, on_blur=ChatState.setName),
            pc.button("Knock Knock!", on_click=ChatState.knockKnock)
        )
    )

def chat():
    return pc.hstack(
        pc.vstack (
            pc.avatar(name=ChatState.name, size="md"),
            pc.list(
                pc.foreach(ChatState.messages, lambda message: renderMessage(message)),
            ),
            pc.input(placeholder="Type your message...", on_blur=ChatState.setNewMessage),
            pc.button("Send", on_click=ChatState.send)
        )
    )

# Add state and page to the app.
app = pc.App(state=ChatState)
app.add_page(index)
app.add_page(chat, route="/chat")
app.compile()
