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

	Vue.component('army_choose', {
		props: ['hero'],
		data: function () {
		    return {
		    	armyes: [],
		    	changes: false
		    }
		},
		template: `
		<div class='hero-block-2'>
			<div class='close-button' @click='$emit("close")'>X</div>
			<div>
				<div v-for='(unit, index) in armyes' class='d-flex flex-row mb-2'>
					<div><a href="#" class='button_additional' @click.prevent='add(index, -1)'>-</a></div>
					<div class='flex-grow-1'>
						<div class='text-center'>{{unit.name}}</div>
						<div class="progress">
					    	<div class="progress-bar" :class='{"bg-danger": unit.count == 0, "bg-success": unit.count == unit.count+unit_aviable(unit)}' role="progressbar" :style='calculate_bar(unit)' :aria-valuenow="unit.count" aria-valuemin="0" :aria-valuemax="unit_aviable(unit)">{{unit.count}}</div>
						</div>
						{{unit_aviable(unit)}}
					</div>
					<div><a href="#" class='button_additional' @click.prevent='add(index, 1)'>+</a></div>
				</div>
				<div v-if='changes == true'>
					<button type="button" class="btn btn-success" @click.prevent='save'>Сохранить</button>
				</div>
			</div>
		</div>`,
		mounted: function () {
			this.calculate_army();
		},
		methods: {
			calculate_army: function () {
				var armyes = {}
				console.log(this.hero.available)
				for (let i = 0; i < this.hero.available.length; i++) {
					armyes[this.hero.available[i].name] = {
						'count': 0,
						'cost': this.hero.available[i].cost
					};
				}
				for (let i = 0; i < this.hero.army.length; i++) {
					if (this.hero.army[i].name in armyes) {
						armyes[this.hero.army[i].name]['count'] = this.hero.army[i].count;
					}
				}
				for (const [key, value] of Object.entries(armyes)) {
					this.armyes.push({ 
						name:key,
						count:value.count,
						cost:value.cost,
						max_value:10000,
					})
				}
			},
			add: function(unit, value) {
				if (this.armyes[unit].count + value <= this.unit_aviable(this.armyes[unit])+this.armyes[unit].count && this.armyes[unit].count + value >= 0) {
					this.armyes[unit].count = this.armyes[unit].count + value;
					this.changes = true;
				}
			},
			calculate_bar: function (unit) {
				let width = parseInt(unit.count/(this.unit_aviable(unit)+unit.count)*100);
				if (width == 0){
					width = 100;
				}
				return 'width: ' + width + '%'
			},
			save: function () {
				var army_manager = {};
				this.armyes.forEach(function (item, index) {
				    army_manager[item.name] = item.count;
				});
				axios.put(`/api/v1/hero/${this.hero.id}`, {
				    army_manager: army_manager
				}).then((response) => {
					this.$emit('update', this.hero.id, response.data.army);
				    this.$emit('close');
				}).catch((error) => {
				  console.error(error.response.data);
				}).finally(() => {
				  // TODO
				});
			},
			unit_aviable: function (unit) {
				var count = parseInt((this.hero.level_info.army_power - this.army_cost)/ unit.cost)
				return count > unit.unit_aviable ? unit.unit_aviable : count
			}
 		},
 		computed: {
 			army_cost: function() {
 				var cost = 0
				this.armyes.forEach(function (item, index) {	
				    cost = cost + item.count*item.cost;
				});
				return cost;
 			}
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
		    	create_hero:false,
		    	choose_army:false
		    }
		},
		template: `
		<div class='row mt-3'>
			<div v-for='(hero, index) in heroes' class='col-xl-4 col-lg-4 col-md-4 col-sm-12 col-12 mb-3'>
				<div class='hero-block h-100' :class='{"hero-block-selected": hero.id == selected_hero}'>
					<div class='hero-header p-2 d-flex flex-row justify-content-between align-items-center'>
					<span class='pl-2'>{{hero.name}}</span>
					<button type="button" class="btn btn-outline-light" @click.prevent='select_(hero.id)' v-if='$root.equal() == true && hero.id != selected_hero'>Выбрать</button>
					</div>
					<div>	
						<div class='d-flex flex-column w-100 p-3'>
							<hero_param text='Атака' :instance='hero' param='attack' url='#'></hero_param>
							<hero_param text='Защита' :instance='hero' param='defense' url='#'></hero_param>
							<hero_param text='Мана' :instance='hero' param='mana' url='#'></hero_param>
							<hero_param text='Сила магии' :instance='hero' param='spell_power' url='#'></hero_param>
							<hero_param text='Иницатива' :instance='hero' param='initiative' url='#'></hero_param>
						</div>
						<div class='w-100 flex-grow-1 px-3 py-2 hero-army d-flex flex-column justify-content-end align-items-center'>
							<div class='d-flex flex-row'>
								<div v-for='(unit, index) in hero.army'>
									<a href="#" class='unit-img-block'>
										<img :src="unit.icon" :alt="unit.name" height='40px' width='40px' />
										<div class='unit-count'>{{unit.count}}</div>
									</a>
								</div>
							</div>
							<button type="button" class="btn btn-outline-primary m-2" @click.prevent='choose_army = hero.id' v-if='$root.equal() == true'>Набор армии</button>
						</div>
					</div>
				</div>

				<!-- Army select -->
					<div v-if='choose_army == hero.id' class='popup-2'>
						<army_choose @update='update(index, arguments)' @close='choose_army = false' :hero='hero'></army_choose>
					</div>

			</div>
			<div v-for='(hero, index) in blank_heroes' class='col-xl-4 col-lg-4 col-md-4 col-sm-12 col-12 mb-3' v-if='$root.equal() == true'>
				<div class='hero-block h-100'>
					<a href="#" @click.prevent='create_hero = true' class='blank-hero'>+</a>
				</div>
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
	    	},
	    	update: function (index, args) {
	    		this.heroes[index].army = args[1];
	    	}
	    }
	})

	var vm = new Vue({
		el: "#app",
		delimiters: ['[[', ']]'],
		data: {
			'user': null,
			'owner': null
		},
		methods: {
			equal: function () {
				return this.user.id == this.owner.id
			}
		}
	})

});
