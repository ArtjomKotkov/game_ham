export {Core};

class Core {

	constructor(ws_url) {
    	this.ws_url = ws_url;
  	}

  	connect() {
  		this.ws = new WebSocket(this.ws_url);
  	}

  	_send_message(msg) {
  		this.ws.send(JSON.stringify(msg));
  	}

  	load_battle() {
  		this._send_message({
  			'command': 'load_battle'
  		})
  	}

  	reciever(message) {
  		console.log(message.data);
  	}

}