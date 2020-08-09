export {MainHandler};



class MainHandler {

	constructor (request, core) {
		this.core = core;
		this._action_handler(request.action);
		this._command_handler(request.command);
		this._system_handler(request.system);
	}

	_action_handler (request) {
		if (request == null) {return;}
		
	}

	_command_handler (request) {
		if (request == null) {return;}
		var handle = new CommandHandler(request, this.core);
	}

	_system_handler (request) {
		if (request == null) {return;}
		var handle = new SystemHandler(request, this.core);
	}

}

class CommandHandler {
	
	constructor (request, core) {
		this.core = core;
		this._set_ready_handler(request.set_ready);
	}
	
	_set_ready_handler (request) {
		this.core.interface.vue.app.heroes[request.hero_id].ready = request.ready;
	}

}

class SystemHandler {
	
	constructor (request, core) {
		this.core = core;
		this._list_handler(request.list);
		this._attr_handler(request.attr);
	}
	
	_list_handler (request) {
		request.forEach((item, i) => {
		    if (item.message == 'load') {
		    	this._load_handler(item.data);
		    }
		});
	}

	_attr_handler (request) {

	}

	_load_handler(request) {
		this.core.interface.battle_load(request);
	}

}