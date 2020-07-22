export {ws};

var path = window.location.pathname.split('/');

var ws = new WebSocket(`ws://127.0.0.1:8000/ws/combat/${path[path.length-1]}`);

