$(document).ready(function() {
	var a = 2;
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
		    	name:name,
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
				<input type="text" v-model='name' />
				<input type="submit" value='Далее' @click='send' v-if='current_hero != null && is_null(name) != false' />
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
				axios.post('/api/v1/hero/', {
					user:this.$root.owner.id,
					name:this.name,
					hero_class:this.items[this.current_hero].class_name
				})
				.then((response) => {
					document.location.href = '/user/info'+this.$root.owner.name;
				}).catch((error) => {
				  	console.error(error);
				});
			},
			is_null: function (field) {
				return field == '' || field == null ? false : true
			}
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
		<tr>
			<td>{{text}}</td>
			<td class='hero-param-td'>{{instance[param]}}</td>
			<td v-if='instance.free_point == true && $root.owner.name == $root.user.name' class='hero-param-td'>
				<a href="#" @click.prevent='increase(true, true)' class='button_additional-sm'>+</a>
			</td>
			<td v-if='$root.user.is_staff == true' class='hero-param-td'>
				<a href="#" @click.prevent='increase(true, false)' class='button_additional-sm-admin'>+</a>
			</td>
			<td v-if='$root.user.is_staff == true' class='hero-param-td'>
				<a href="#" @click.prevent='increase(false, false)' class='button_additional-sm-admin'>-</a>
			</td>
		</tr>
		`,
		methods: {
			increase: function (up, free_point) {
				var value = up == true ? 1 : -1
				var param = this.param
				var data = {
				  [param]: this.instance[param]+value,
				}
				if (free_point == true) {
					data.free_point = false;
				}
				axios.put(`/api/v1/hero/${this.instance.id}`, data)
				.then((response) => {
				  	this.instance[param] = this.instance[param]+value;
				  	if (free_point == true) {
				  		this.$emit('false_free_point');
					}
				}).catch((error) => {
				  console.error(error.response.data);
				}).finally(() => {
				  // TODO
				});
			}
		}
	})

	Vue.component('progress_bar', {
		props: ['current', 'max'],
		data: function () {
		    return {
		    	true_str: 'True'
		    }
		},
		template: `
		<div class='w-100 outer-bar'>
			<div :style='{"width": width}' class='inner-bar h-100' :class='{"inner-bar-full": width == "100%"}' @click='level_up'>
				<div class='inner-text' v-if='width != "100%"'>
					{{current}} / {{max}}
				</div>
				<div class='inner-text' v-else>
					Новый уровень!
				</div>
			</div>
		</div>
		`,
		computed: {
			width: function () {
				let width = (this.current/this.max)*100;
				if (width > 100) {
					width = 100;
				}
				return width+'%';
			}
		},
		methods: {
			level_up: function () {
				if (this.width != "100%") {
					return;
				}
				this.$emit('level_up');
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
			<div v-for='(hero, index) in heroes' class='col-xl-4 col-lg-4 col-md-12 col-sm-12 col-12 mb-3'>
				<div class='hero-block h-100' :class='{"hero-block-selected": hero.id == selected_hero}'>
					<div class='hero-header p-2 d-flex flex-row justify-content-between align-items-center'>
					<span class='pl-2'>{{hero.name}}</span>
					<button type="button" class="btn btn-outline-light" @click.prevent='select_(hero.id)' v-if='$root.equal() == true && hero.id != selected_hero'>Выбрать</button>
					</div>
					<progress_bar @level_up='level_up(hero, index)' :current='hero.exp' :max='hero.level_info.exp'></progress_bar>
					<div>	
						<div class='d-flex flex-column w-100 p-3'>
							<table>
								<hero_param @false_free_point='hero.free_point = false' text='Атака' :instance='hero' param='attack' url='#'></hero_param>
								<hero_param @false_free_point='hero.free_point = false' text='Защита' :instance='hero' param='defense' url='#'></hero_param>
								<hero_param @false_free_point='hero.free_point = false' text='Мана' :instance='hero' param='mana' url='#'></hero_param>
								<hero_param @false_free_point='hero.free_point = false' text='Сила магии' :instance='hero' param='spell_power' url='#'></hero_param>
								<hero_param @false_free_point='hero.free_point = false' text='Иницатива' :instance='hero' param='initiative' url='#'></hero_param>
							</table>
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
			<div v-for='(hero, index) in blank_heroes' class='col-xl-4 col-lg-4 col-md-12 col-sm-12 col-12 mb-3' v-if='$root.equal() == true'>
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
	    	},
	    	level_up: function (hero, index) {
	    		console.log('asfsf')
				axios.put(`/api/v1/hero/${hero.id}`, {
				  level: hero.level+1,
				  exp: hero.exp - hero.level_info.exp,
				  free_point: true
				}).then((response) => {
					this.heroes[index].level = response.data.level;
					this.heroes[index].exp = response.data.exp;
					this.heroes[index].level_info.exp = response.data.level_info.exp;
					this.heroes[index].free_point = true;
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
		},
		methods: {
			equal: function () {
				return this.user.id == this.owner.id
			}
		}
	})

});
