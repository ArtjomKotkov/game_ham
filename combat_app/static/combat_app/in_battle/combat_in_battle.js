import {Core} from './combat/core.js';

// Get id of battle from url path.
var path = window.location.pathname.split('/');

// Connect and handle ws.
var core = new Core(`ws://127.0.0.1:8000/ws/combat/`, path[path.length-1]);
core.connect()


