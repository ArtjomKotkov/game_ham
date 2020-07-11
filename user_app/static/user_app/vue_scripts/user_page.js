$(document).ready(function() {
	
	axios.defaults.xsrfCookieName = 'csrftoken'
	axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

	Vue.component('request_handler', {
		props: ['ident', 'id', 'name', 'is_staff'],
		data: function () {
		    return {
		    }
		},
		template: `
		<div class='d-none'></div>
		`,
		mounted: function() {
	        this.$root[this.ident] = {
	        	'id': this.id,
	        	'name': this.name,
	        	'is_staff': this.is_staff == 'True'? true : false,
	        }
	    },
	    delimiters: ['[[', ']]']
	})

	Vue.component('create_hero', {
		data: function () {
		    return {
		    	items:null,
		    	current_hero:null,
		    }
		},
		template: `
		<div>
			<div class='close-button' @click='$emit("close")'>X</div>
			<div>Heroes</div>
			<div class='d-flex flex-row'>
				<div v-for='(item, index) in items' @click='current_hero = index' class='hero-box' :class='{"selected-hero": current_hero==index}'>
					<div>
						<span>{{item.name}}</span>
					</div>
					<div>
						<span>{{item.description}}</span>
					</div>
				</div>
			</div>
			<div>
				<input type="submit" value='Далее' @click='send' v-if='current_hero != null'/>
			</div>
		</div>`,
		mounted: function() {
			axios.get('/auth/hero_api/', {
			}).then((response) => {
			 	this.items = response.data.items;
			});
		},
		methods: {
			send: function () {
				form = new FormData()
				form.append('hero', this.items[this.current_hero].name)
				axios.post('/auth/hero/', form)
				.then((response) => {
					document.location.href = '/auth/register/';
				}).catch((error) => {
				  console.error(error);
				});
			},
		}
	})


	Vue.component('hero_param', {
		props: ['text', 'instance', 'param', 'url'],
		data: function () {
		    return {
		    	true_str: 'True'
		    }
		},
		template: `
		<div>
			<span>{{text}}</span>
			<span>{{instance[param]}}</span>
			<span v-if='$root.user.is_staff == true'>
				<a href="#" @click.prevent='increase(true)'>+</a>
				<a href="#" @click.prevent='increase(false)'>-</a>
			</span>
		</div>
		`,
		methods: {
			increase: function (up) {
				var value = up == true ? 1 : -1
				var param = this.param
				axios.put(`/api/v1/hero/${this.instance.id}`, {
				  [param]: this.instance[param]+value,
				}).then((response) => {
				  	this.instance[param] = this.instance[param]+value;
				}).catch((error) => {
				  console.error(error.response.data);
				}).finally(() => {
				  // TODO
				});
			}
		}
	})

	Vue.component('heroes', {
		data: function () {
		    return {
		    	heroes:null,
		    	blank_heroes:[],
		    	selected_hero:null,
		    	create_hero:false
		    }
		},
		template: `
		<div class='d-flex flex-row'>
			<div v-for='(hero, index) in heroes' class='hero-block' :class='{"hero-block-selected": hero.id == selected_hero}'>
				<div>{{hero.name}}</div>	
				<div class='d-flex flex-column'>
					<hero_param text='Атака' :instance='hero' param='attack' url='#'></hero_param>
					<hero_param text='Защита' :instance='hero' param='defense' url='#'></hero_param>
					<hero_param text='Мана' :instance='hero' param='mana' url='#'></hero_param>
					<hero_param text='Сила магии' :instance='hero' param='spell_power' url='#'></hero_param>
					<hero_param text='Иницатива' :instance='hero' param='initiative' url='#'></hero_param>
				</div>
				<div>
					<div v-for='(unit, index) in hero.army'>
						<span>{{unit.name}}: {{unit.count}}</span>
					</div>
				</div>
				<button type="button" class="btn btn-outline-primary" @click.prevent='select_(hero.id)'>Выбрать</button>
			</div>
			<div v-for='(hero, index) in blank_heroes' class='hero-block'>
			<a href="#" @click.prevent='create_hero = true'>+</a>
			</div>
			<div v-if='create_hero == true' class='popup'>
				<create_hero @close='create_hero = false'></create_hero>
			</div>
		</div>
		`,
		mounted: function() {
	        axios.get(`/user/${this.$root.owner.id}`)
	        .then((response) => {
	        	this.selected_hero = response.data.heroapp.selected_hero;
	        	this.heroes = response.data.heroes;
	        	var blank_heroes = 3-this.heroes.length;
	        	for (let i = 0; i < blank_heroes; i++) { // выведет 0, затем 1, затем 2
	        		this.blank_heroes.push(i)
				}
	        }).catch((error) => {
	            console.error(error);
	        });
	    },
	    methods: {
	    	select_: function (id) {
	    		axios.put('/user/'+parseInt(this.$root.owner.id)+'/', {
	    		    heroapp: {
	    		    	selected_hero: id
	    		    },
	    		}).then((response) => {
	    		    this.selected_hero = id
	    		}).catch((error) => {
	    		    console.error(error.response.data);
	    		}).finally(() => {
	    		  // TODO
	    		});
	    	}
	    }
	})

	var vm = new Vue({
		el: "#app",
		delimiters: ['[[', ']]'],
		data: {
			'user': null,
			'owner': null
		}
	})

});
