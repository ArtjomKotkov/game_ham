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
			<div v-if='combat.battle_type == "DF" && combat.placement_type == "FR"' class='d-flex flex-row justify-content-between'>
				<div>
					<span v-if='combat.left_team.length < combat.team_size && $root.user.heroapp.selected_hero.in_battle == -1' @click.prevent='connect_to_left_team(combat, index)'>[Вступить]</span>
					<span v-for='(hero, index) in combat.left_team'>
						<a :href="hero.hero_url">{{hero.name}}</a>
					</span>
					<span>{{time}}</span>
					<span v-for='(hero, index) in combat.right_team'>
						<a :href="hero.hero_url">{{hero.name}}</a>
					</span>
					<span v-if='combat.right_team.length < combat.team_size && $root.user.heroapp.selected_hero.in_battle == -1' @click.prevent='connect_to_right_team(combat, index)'>[Вступить]</span>
				</div>
				<button v-if='$root.user.heroapp.selected_hero.in_battle == combat.id' @click='exit(combat, index)'>Выйти</button>
				<button @click='show_'>U</button>
			</div>

			<!-- default combat, equal placement -->
			<div v-else-if='combat.battle_type == "DF" &&  combat.placement_type == "EQ"' class='d-flex flex-row justify-content-between'>
				<div>
					<span v-if='combat.left_team.length < combat.team_size && combat.left_team.length <= combat.right_team.length && $root.user.heroapp.selected_hero.in_battle == -1' @click.prevent='connect_to_left_team(combat, index)'>[Вступить]</span>
					<span v-for='(hero, index) in combat.left_team'>
						<a :href="hero.hero_url">{{hero.name}}</a>
					</span>
					<span>{{time}}</span>
					<span v-for='(hero, index) in combat.right_team'>
						<a :href="hero.hero_url">{{hero.name}}</a>
					</span>
					<span v-if='combat.right_team.length < combat.team_size && combat.right_team.length <= combat.left_team.length && $root.user.heroapp.selected_hero.in_battle == -1' @click.prevent='connect_to_right_team(combat, index)'>[Вступить]</span>
				</div>
				<button v-if='$root.user.heroapp.selected_hero.in_battle == combat.id' @click='exit(combat, index)'>Выйти</button>
				<button @click='show_'>U</button>
			</div>

			<!-- meat grinder combat -->
			<div v-else class='d-flex flex-row justify-content-between'>
				<div>
					<span v-if='combat.mg_team.length < combat.team_size && $root.user.heroapp.selected_hero.in_battle == -1' @click.prevent='connect_to_mg_team(combat, index)'>[Вступить]</span>
					<span v-for='(hero, index) in combat.mg_team'>
						<a :href="hero.hero_url">{{hero.name}}</a>
					</span>
					<span>{{time}}</span>
				</div>
				<button v-if='$root.user.heroapp.selected_hero.in_battle == combat.id' @click='exit(combat, index)'>Выйти</button>
				<button @click='show_'>U</button>
			</div>

			<!-- common options -->
		    <div v-if='show == true'>
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
			show_: function () {
				if (this.show == true) {
					this.show = false;
				} else {
					this.show = true;
				}
			},
			calc_time: function () {
				if (this.time == 0) {
					return;
				}
				if (this.time == null) {
					this.time = this.combat.placement_time;
				}
				this.time--;
				setTimeout(() => this.calc_time(), 60000);
			},


		}
	})

	var combats = Vue.component('combats', {
		template:`
		<div>
			<div v-if='loaded == false'>
				<img src="/static/combat_app/loading.gif" alt="" />
			</div>
			<div v-else>
				<button @click='create_new'>Создать</button>
				<combat v-for='(combat, index) in combats' :combat='combat' :index='index' @left_team_connect='connect_to_left_team' @right_team_connect='connect_to_right_team' @mg_team_connect='connect_to_mg_team' @exit='exit'></combat>
			</div>
			
		</div>`,
		data: function () {
			return {
				combats: [],
				loaded: false,
			}
		},
		methods: {
			// WS
			onmessage: function (event) {
				this.loaded = true;
				var data = JSON.parse(event.data);
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
				data.forEach(element => this.combats.push(element));
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
				this.$root.user.heroapp.selected_hero.in_battle = -1;
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
				this.$root.user.heroapp.selected_hero.in_battle = data['combat_id'];
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