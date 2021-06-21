const user_id = 1;
// const token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI0MjAwMzc3LCJqdGkiOiIwNTBhMDljMWNiZDk0NWJjOWVjYWI2MGE0NjE5MWRkYiIsInVzZXJfaWQiOjIsInVzZXJuYW1lIjoiZGl2YW5vdiJ9.167OnFdS2kVQvp-io3gYsJKqq26q8Ps_VjXkaNIUCMc';
const task_id = 1;

const WS = new WebSocket('ws://localhost:8000/ws/notify/'+user_id+'/');
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
    WS.send(JSON.stringify(createMsg('stop.task')));
}

function startTask() {
    WS.send(JSON.stringify(createMsg('star.task')));
}

function closeTask() {
    WS.send(JSON.stringify(createMsg('close.task')));
}

WS.onmessage = message => {
    data = JSON.stringify(message);
    console.log(data);
}