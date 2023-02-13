"""Welcome to Pynecone! This file outlines the steps to create a basic app."""
from pcconfig import config
import pynecone as pc
import socketio

## ++SIO
sio = socketio.Client()
authData = {
    'token': '<Token_2>'
}

@sio.event
def connect():
    print('I\'m connected!')

@sio.event
def connect_error(data):
    print('The connection failed!')

@sio.event
def disconnect():
    print('I\'m disconnected!')  
    authData["token"] = ChatState.name
    authData["username"] = ChatState.name
    sio.connect('http://localhost:5001', auth = authData)
    ChatState.connected = True

# @sio.event
# def message(data):
#     print('I received a message!')

@sio.on('message')
def on_message(data):
    ChatState.messages += [f'{data["username"]}: {data["message"]}']


## --SIO

class ChatState(pc.State):
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

    # def addMessage(self, text):
    #     self.messages += text

    def knockKnock(self):
        authData["token"] = self.name
        authData["username"] = self.name
        sio.connect('http://localhost:5001', auth = authData)
        self.connected = True
        if self.connected:
            return pc.redirect(
            "/chat"
            )

    def send(self):
        sio.emit('message', {'message': self.newMessage})
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
        pc.markdown("# Index Page!"),
        pc.link(
            "Login",
            href="/login",
            color="rgb(107,99,246)",
        )
    )

def login():
    return pc.hstack(
        pc.vstack (
            pc.markdown("## Login Page"),
            pc.input(placeholder="Your Name", on_blur=ChatState.setName),
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
app.add_page(login, route="/login")
app.add_page(chat, route="/chat")
app.compile()
