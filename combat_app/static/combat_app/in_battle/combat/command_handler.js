export {CommandHandler};

import {MainHandler} from './handlers/handler.js'


class CommandHandler {

	constructor(wsCore) {
    	this.core = wsCore;
    	this.interface = null;
  	}    

  	load_battle(id) {
  		this.core.send_message({
  			combat_id: id,
  			system: {
  				list: ['load']
  			}
  		})
  	}

  	reciever(event) {
  		console.log('|=========================INCOME=========================|')
  		console.log(event);
  		console.log('|========================= END ==========================|')
  		this.handler = new MainHandler(event, this.core);
  	}

}