export {Interface};
import {VueLoad} from './vue/core.js';


class Interface {

	constructor (core) {
		this.core = core;
	}

	battle_load(event) {
		if (event.status == 'load') {
			this._battle_in_load(event);
		} else if (event.status == 'prepare') {
			this._battle_prepare(event);
		} else if (event.status == 'inbattle') {
			this._battle_in_battle(event);
		}
	}

    _create_pixi_instance() {
        var w = window.innerWidth*0.9;
        var h = w*9/16;

        let app = new PIXI.Application(
            {
                width: w, 
                height: h,
                antialias: true,
                transparent: false,
                resolution: 1 
            }
        );
        document.body.appendChild(app.view);

        app.renderer.autoResize = true;

        window.onresize = function(event) {
            w = window.innerWidth*0.9;
            h = w*9/16; 
            app.renderer.resize(w, h);
        };
    }

	_battle_in_load(event) {
        this.vue = new VueLoad(event, this.core);
	}

    _battle_prepare(event) {
        
    }

    _battle_in_battle(event) {
        
    }

}