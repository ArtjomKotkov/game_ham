export {Core};

import {CommandHandler} from './command_handler.js'
import {Interface} from './interface/main.js'


class Core {

	constructor(ws_url, combat_id) {
      this.combat_id = combat_id;
    	this.ws_url = ws_url + this.combat_id;
  	}    

    connect(onOpen, handler) {
        this.ws = new WebSocket(this.ws_url);

        this.command = new CommandHandler(this);

        this.interface = new Interface(this);

        this.ws.onerror = (event) => {
            console.log(event);
        }

        this.ws.onopen = (event) => {
            this.command.load_battle(this.combat_id);
        }

        this.ws.onmessage = (event) => {
            this.command.reciever(JSON.parse(event.data));
        }
    }

  	send_message(msg) {
      console.log('|========================= OUTCOME =========================|')
      console.log(msg);
      console.log('|=========================== END ===========================|')
  		this.ws.send(JSON.stringify(msg));
  	}

}