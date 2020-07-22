import {Core} from './combat/core.js'

var path = window.location.pathname.split('/');

var core = new Core(`ws://127.0.0.1:8000/ws/combat/${path[path.length-1]}`)
core.connect()

core.ws.onmessage = function (event) {
  	core.reciever(event);
}

core.ws.onopen = function (event) {
	core.load_battle()
}