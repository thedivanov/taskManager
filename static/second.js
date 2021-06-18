const user_id = 1;
const token = '123';
const task_id = 1;

const WS = new WebSocket('ws://localhost:8000/ws/notify/'+task_id+'/');
const url = 'http://127.0.0.1:8000'

WS.onclose = () => {
    console.log('closed');
}

WS.onerror = error => {
    console.log('some error: ', error);
}

function createMsg(type) {
    const msg = {
        'type':type,
        'task_id':task_id,
        'user_id':user_id,
    }

    return msg;
}

function stopTask() {
    WS.send(JSON.stringify(createMsg('stop_task')));
}

function startTask() {
    WS.send(JSON.stringify(createMsg('star_task')));
}

function closeTask() {
    WS.send(JSON.stringify(createMsg('close_task')));
}

WS.onmessage = message => {
    data = JSON.stringify(message);
    console.log(data);
}