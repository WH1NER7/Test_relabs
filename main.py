from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form name="main_info" action="" onsubmit="sendMessage(event)" >
            <input name="text" type="text" id="messageText" autocomplete="off"/>
            <input name="email" type="email" id="messageEmail" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var parsedData = JSON.parse(event.data);
                var text = parsedData.text
                var email = parsedData.email
                var number = parsedData.number
                var str_to_show = `${number} Сообщение от ${email}. Текст: ${text}`;
                var content = document.createTextNode(str_to_show)
                message.appendChild(content)
                messages.appendChild(message)
            };
            
            

            const EMAIL_REGEXP = /^(([^<>()[\].,;:\s@"]+(\.[^<>()[\].,;:\s@"]+)*)|(".+"))@(([^<>()[\].,;:\s@"]+\.)+[^<>()[\].,;:\s@"]{2,})$/iu;

            
            function onInput() {
              if (isEmailValid(input_mail.value)) {
                input_mail.style.borderColor = 'green';
              } else {
                input_mail.style.borderColor = 'red';
              }
            }
            
            
            function isEmailValid(value) {
            return EMAIL_REGEXP.test(value);
            }
            
           
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                var input_mail = document.getElementById("messageEmail")
                input_mail.addEventListener('input_mail', onInput);

                var object = {};
                var formData = new FormData(document.forms.main_info);
            
                formData.forEach(function(value, key){
                    object[key] = value;
                });
                var json = JSON.stringify(object);
                
                ws.send(json)
                input.value = ''
                input_mail.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    msg_count = 0
    while True:
        msg_count += 1
        data = await websocket.receive_json()
        text = data.get('text')
        email = data.get('email')
        response = {
            "text": text,
            "email": email,
            "number": msg_count
        }
        await websocket.send_json(response)

