import {loading} from './components/loading/loading.js';

export {VueLoad};


class VueLoad {

	constructor(data, core) {
    	
        // Parent div
        var div = document.createElement('div');
        div.setAttribute('id', 'app');
        document.body.appendChild(div);

        // Main load div
        var div = document.createElement('loading');
        document.getElementById('app').appendChild(div);

        data.manager = this;
        this.core = core

        this.app = new Vue({
            el: '#app',
            data: data,
            components: {
                loading
            }
        })

  	}

    set_ready(hero_index) {
        this.core.send_message({
            combat_id: this.core.combat_id,
            command: {
                set_ready: {
                    hero_id: hero_index
                }
            }
        })
    }

}
