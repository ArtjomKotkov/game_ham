$(document).ready(function() {
	
	Vue.component('request_handler', {
		props: ['ident', 'id', 'name', 'is_staff', 'hero_in_battle'],
		data: function () {
		    return {
		    }
		},
		template: `
		<div class='d-none'></div>
		`,
		mounted: function() {
			axios.get('/user/'+this.id+'?short=true', {
			}).then((response) => {
			  this.$root[this.ident] = response.data;
			}).catch((error) => {
			  console.error(error);
			}).finally(() => {
			  // TODO
			});
	    },
	    delimiters: ['[[', ']]']
	})
	
	Vue.component('combat', {
		props:['combat', 'index'],
		data: function () {
			return {
				show: false,
				time: null
			}
		},
		template:`
		<div>

			<!-- default combat, free placement -->
			<div v-if='combat.battle_type == "DF" && combat.placement_type == "FR"' class='d-flex flex-row justify-content-center combat-box' @click.prevent='show_' ref='combat'>
				<div class='d-flex flex-row justify-content-center items-align-center'>

					<a href="#" v-if='combat.left_team.length < combat.team_size && $root.user.heroapp.selected_hero.in_battle == -1' @click.prevent='connect_to_left_team(combat, index)' class='vs-connect'>Вступить</a>
					<a :href="hero.hero_url" v-for='(hero, index) in combat.left_team' class='vs-hero-left'>{{hero.name}}</a>
					
					<div class='vs-time'>{{time}} мин.</div>
					
					<a :href="hero.hero_url" v-for='(hero, index) in combat.right_team' class='vs-hero-right'>{{hero.name}}</a>
					<a href="#" v-if='combat.right_team.length < combat.team_size && $root.user.heroapp.selected_hero.in_battle == -1' @click.prevent='connect_to_right_team(combat, index)' class='vs-connect'>Вступить</a>

					<button v-if='$root.user.heroapp.selected_hero.in_battle == combat.id' @click='exit(combat, index)'>Выйти</button>
				</div>
			</div>

			<!-- default combat, equal placement -->
			<div v-else-if='combat.battle_type == "DF" &&  combat.placement_type == "EQ"' class='d-flex flex-row justify-content-center combat-box' @click='show_' ref='combat'>
				<div class='d-flex flex-row justify-content-center items-align-center'>
					
					<a href="#" v-if='combat.left_team.length < combat.team_size && combat.left_team.length <= combat.right_team.length && $root.user.heroapp.selected_hero.in_battle == -1' @click.prevent='connect_to_left_team(combat, index)' class='vs-connect-eq-l'>Вступить</a>
					<a :href="hero.hero_url" v-for='(hero, index) in combat.left_team' class='vs-hero-left'>{{hero.name}}</a>
					
					<div class='vs-time'>{{time}} мин.</div>
					
					<a :href="hero.hero_url" v-for='(hero, index) in combat.right_team' class='vs-hero-right'>{{hero.name}}</a>
					<a href="#" v-if='combat.right_team.length < combat.team_size && combat.right_team.length <= combat.left_team.length && $root.user.heroapp.selected_hero.in_battle == -1' @click.prevent='connect_to_right_team(combat, index)' class='vs-connect-eq-r'>Вступить</a>

					<button v-if='$root.user.heroapp.selected_hero.in_battle == combat.id' @click='exit(combat, index)'>Выйти</button>
				</div>
			</div>

			<!-- meat grinder combat -->
			<div v-else class='d-flex flex-row justify-content-center combat-box' ref='combat'>
				<div class='d-flex flex-row justify-content-center items-align-center' @click='show_'>

					<a href="#" v-if='combat.mg_team.length < combat.team_size && $root.user.heroapp.selected_hero.in_battle == -1' @click.prevent='connect_to_mg_team(combat, index)' class='vs-connect'>Вступить</a>
					<a :href="hero.hero_url" v-for='(hero, index) in combat.mg_team' class='vs-hero-left'>{{hero.name}}</a>
					<div class='vs-time'>{{time}} мин.</div>
					
					<button v-if='$root.user.heroapp.selected_hero.in_battle == combat.id' @click='exit(combat, index)'>Выйти</button>
				</div>		
			</div>

			<!-- common options -->
		    <div v-if='show == true' class=''>
				<div>{{combat.name}}</div>
		    </div>

		</div>`,
		mounted: function () {
			this.calc_time()
		},
		methods: {
			connect_to_left_team: function (combat, index) {
				this.$emit('left_team_connect', this.$event, combat, index);
			},
			connect_to_right_team: function (combat, index) {
				this.$emit('right_team_connect', this.$event, combat, index);
			},
			connect_to_mg_team: function (combat, index) {
				this.$emit('mg_team_connect', this.$event, combat, index);
			},
			exit: function (combat, index) {
				this.$emit('exit', this.$event, combat, index);
			},
			show_: function (event) {
				if (this.$refs.combat != event.target) {
					return;
				}
				if (this.show == true) {
					this.show = false;
				} else {
					this.show = true;
				}
			},
			calc_time: function () {
				if (this.time == 0) {
					return;
				} else if (this.time == null) {
					this.time = this.combat.placement_time;
					setTimeout(() => this.calc_time(), 60000);
				} else {
					this.time--;
					setTimeout(() => this.calc_time(), 60000);
				}
			},


		}
	})

	var combats = Vue.component('create_combat_comp', {
		template:`
		<div class='create-combat'>
			<a href="#" class='close-button' @click='$emit("close")'>X</a>
			<form>
				<input type="email" class="form-control mb-2" id="nameInput" placeholder='Описание' v-model='name'>

				<span class='create-combat-input-label'>Распределение по командам:</span>
				<div class='d-flex flex-row justify-content-center items-align-center'>
					<a href='#' @click='selected_placement_type = 0' class='create_combat_button' :class='{"create_combat_button_selected": selected_placement_type == 0}'>Равномерно</a>
					<a href='#' @click='selected_placement_type = 1' class='create_combat_button' :class='{"create_combat_button_selected": selected_placement_type == 1}'>Свободно</a>
					<a href='#' @click='selected_placement_type = 2' class='create_combat_button' :class='{"create_combat_button_selected": selected_placement_type == 2}'>Каждый сам за себя</a>
				</div>

				<!-- battle size -->
				<div v-if='selected_placement_type == 0 || selected_placement_type == 1'>
					<span class='create-combat-input-label'>Размер команд:</span>
					<div class='create-combat-range-value'>{{team_size}}</div>
					<input type="range" class="form-control-range" id="formControlRange" min="1" max="3" v-model='team_size'>
				</div>
				<div v-else>
					<span class='create-combat-input-label'>Количество участников:</span>
					<div class='create-combat-range-value'>{{team_size}}</div>
					<input type="range" class="form-control-range" id="formControlRange" min="3" max="8" v-model='team_size'>
				</div>

				<div>
					<span class='create-combat-input-label'>Старт через:</span>
					<div class='create-combat-range-value'>{{placement_time}} мин.</div>
					<input type="range" class="form-control-range" id="formControlRange" min="3" max="15" v-model='placement_time'>
				</div>

				<span class='create-combat-input-label'>Поле:</span>
				<div class='d-flex flex-wrap flex-row justify-content-center items-align-center'>
					<div v-for='(field, index) in current_fields' class='field-box' :class='{"field-box-selected": index == selected_field}' @click='selected_field = index'>
						<span>{{field.name}} {{field.image}}</span>
					</div>
				</div>
				<div v-if='not_blank(name) == true' class='d-flex flex-row justify-content-center items-align-center mt-3'>
					<a href="#" class='create_combat_button d-block' @click.prevent='create_combat'>Создать бой</a>
				</div> 
			</form>
		</div>`,
		data: function () {
			return {
				selected_placement_type: 0,
				placement_time: 3,
				team_size: 1,
				fields: null,
				selected_field: 'Simple',
				name:''
			}
		},
		mounted: function () {
			axios.get('/combat/fields/', {
			}).then((response) => {
			   this.fields = response.data.fields;
			}).catch((error) => {
			  console.error(error);
			}).finally(() => {
			  // TODO
			});
		},
		watch: {
			selected_placement_type: function (newValue) {
				if (newValue == 2 && this.team_size < 3) {
					this.team_size = 3;
				} else if ((newValue == 1 || newValue == 0) && this.team_size > 3) {
					this.team_size = 1;
				}
				if (this.placement_type == 'EQ' || this.placement_type == 'FR') {
					if (!(this.selected_field in this.fields.DF[this.team_size])) {
						this.selected_field = 'Simple';
					}
				} else {
					if (!(this.selected_field in this.fields.MG[this.team_size])) {
						this.selected_field = 'Simple';
					}
				}
			},
			team_size: function (newValue) {
				if (this.placement_type == 'EQ' || this.placement_type == 'FR') {
					if (!(this.selected_field in this.fields.DF[newValue])) {
						this.selected_field = 'Simple';
					}
				} else {
					if (!(this.selected_field in this.fields.MG[newValue])) {
						this.selected_field = 'Simple';
					}
				}
			}
		},
		computed: {
			placement_type: function () {
				if (this.selected_placement_type == 0) {
					return 'EQ'
				} else if (this.selected_placement_type == 1) {
					return 'FR'
				} else if (this.selected_placement_type == 2) {
					return 'MG'
				}
			},
			current_fields: function() {
				if (this.fields == null) {
					return;
				}
				if (this.placement_type == 'EQ' || this.placement_type == 'FR') {
					return this.fields.DF[this.team_size];
				} else {
					return this.fields.MG[this.team_size];
				}
			},
			battle_type: function () {
				if (this.selected_placement_type == 0) {
					return 'DF'
				} else if (this.selected_placement_type == 1) {
					return 'DF'
				} else if (this.selected_placement_type == 2) {
					return 'MG'
				}
			},
		},
		methods: {
			create_combat: function () {
				this.$parent.send_json({
					create: {
						name: this.name,
						placement_time: this.placement_time,
						placement_type: this.placement_type,	
						battle_type: this.battle_type,
						team_size: this.team_size,
						field: this.selected_field
					}
				})
				this.$emit('close');
			},
			not_blank: function (field) {
				return field == null || field == '' ? false : true
			}
		}
	})

	var combats = Vue.component('combats', {
		template:`
		<div>
			<div v-if='loaded == false'>
				<img src="/static/combat_app/loading.gif" alt="" />
			</div>
			<div v-else>
				<button id='create-new-combat' type="button" class="btn btn-primary" @click='create_window = true' v-if='$root.user.heroapp.selected_hero.in_battle == -1'>Создать</button>
				<create_combat_comp v-if='create_window == true' @close='create_window = false'></create_combat_comp>
				<combat v-for='(combat, index) in combats' v-bind:key="combat.id" :combat='combat' :index='index' @left_team_connect='connect_to_left_team' @right_team_connect='connect_to_right_team' @mg_team_connect='connect_to_mg_team' @exit='exit'></combat>
			</div>
			
		</div>`,
		data: function () {
			return {
				combats: [],
				loaded: false,
				create_window: false,
				placement_time: 3
			}
		},
		methods: {
			// WS
			onmessage: function (event) {
				this.loaded = true;
				var data = JSON.parse(event.data);
				console.log(data)
				if ('created' in data) {
					this.create(data.created);
				} else if ('basic' in data) {
					this.combats = data.basic;
				} else if ('exit' in data) {
					this.exit_user(data.exit);
				} else if ('connect' in data) {
					this.connect(data.connect);
				}
			},
			send_json: function (message) {
				this.$root.ws.send(JSON.stringify(message))
			},
			create_new: function() {
				this.send_json({
					create: {
					}
				})
			},
			// BASIC
			create: function (data) {
				this.combats.push(data.combat);
				if (this.$root.user.heroapp.selected_hero.id == data.hero_id) {
					this.$root.user.heroapp.selected_hero.in_battle = data.combat.id;
				}
			},
			exit_user: function (data) {
				if (data.team == 'left') {
					for(var i = 0; i < this.combats[data.combat_index].left_team.length; i++) {
						if (this.combats[data.combat_index].left_team[i].id == data.hero_id) {
							this.combats[data.combat_index].left_team.splice(i, 1)
							break;
						}
					}
				} else if (data.team == 'right') {
					for(var i = 0; i < this.combats[data.combat_index].right_team.length; i++) {
						if (this.combats[data.combat_index].right_team[i].id == data.hero_id) {
							this.combats[data.combat_index].right_team.splice(i, 1)
							break;
						}
					}
				} else {
					for(var i = 0; i < this.combats[data.combat_index].mg_team.length; i++) {
						if (this.combats[data.combat_index].mg_team[i].id == data.hero_id) {
							this.combats[data.combat_index].mg_team.splice(i, 1)
							break;
						}
					}
				}
				if (this.$root.user.heroapp.selected_hero.id == data.hero_id) {
					this.$root.user.heroapp.selected_hero.in_battle = -1;
				}
			},
			connect: function(data) {
				if (data.team == 'left') {
					this.combats[data.combat_index].left_team.push({
						'id': data.hero_id,
						'name': data.hero_name,
						'hero_url': data.hero_url
					})
				} else if (data.team == 'right') {
					this.combats[data.combat_index].right_team.push({
						'id': data.hero_id,
						'name': data.hero_name,
						'hero_url': data.hero_url
					})
				} else {
					this.combats[data.combat_index].mg_team.push({
						'id': data.hero_id,
						'name': data.hero_name,
						'hero_url': data.hero_url
					})
				}
				if (this.$root.user.heroapp.selected_hero.id == data.hero_id) {
					this.$root.user.heroapp.selected_hero.in_battle = data.combat_id;
				}
			},
			// Messages
			connect_to_left_team: function (event, combat, index) {
				this.send_json({
					'connect':{
						combat_id: combat.id,
						combat_index: index,
						team:'left',
						hero_id: this.$root.user.heroapp.selected_hero.id
					}
				})
			},
			connect_to_right_team: function (event, combat, index) {
				this.send_json({
					'connect':{
						combat_id: combat.id,
						combat_index: index,
						team:'right',
						hero_id: this.$root.user.heroapp.selected_hero.id
					}
				})
			},
			connect_to_mg_team: function (event, combat, index) {
				this.send_json({
					'connect':{
						combat_id: combat.id,
						combat_index: index,
						team:'mg',
						hero_id: this.$root.user.heroapp.selected_hero.id
					}
				})
			},
			exit: function (event, combat, index) {
				console.log(event, combat, index);
				this.send_json({
					'exit':{
						combat_id: combat.id,
						combat_index: index,
						hero_id: this.$root.user.heroapp.selected_hero.id
					}
				})
			}
		}
	})

	var vm = new Vue({
	    el: "#app",
	    data: {
	  	    ws: null,
	  	    user: null
	    },
	    mounted: function () {
	  	    this.ws = new WebSocket("ws://127.0.0.1:8000/ws/combats/");
	    }
	})

	vm.ws.onmessage = function (event) {
		vm.$refs.combats.onmessage(event);
	}

});