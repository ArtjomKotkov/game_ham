$(document).ready(function() {
	
	
	Vue.component('combat', {
		props:['combat'],
		template:`
		<div>

			<!-- default combat, free placement -->
			<div v-if='combat.battle_type == "DF" &&  combat.placement_type == "FR"' class='d-flex flex-row'>
				<div>{{combat.name}}</div>
				<div>
					<span v-if='combat.left_team.length < combat.team_size' @click.prevent='connect_to_left_team'>[Вступить]</span>
					<span v-for='(hero, index) in combat.left_team'>
						{{hero.name}}
					</span>
					<span> VS </span>
					<span v-for='(hero, index) in combat.right_team'>
						{{hero.name}}
					</span>
					<span v-if='combat.right_team.length < combat.team_size' @click.prevent='connect_to_right_team'>[Вступить]</span>
				</div>
			</div>

			<!-- default combat, equal placement -->
			<div v-else-if='combat.battle_type == "DF" &&  combat.placement_type == "EQ"' class='d-flex flex-row'>
				<div>{{combat.name}}</div>
				<div>
					<span v-if='combat.left_team.length < combat.team_size && combat.left_team.length <= combat.right_team.length' @click.prevent='connect_to_left_team'>[Вступить]</span>
					<span v-for='(hero, index) in combat.left_team'>
						{{hero.name}}
					</span>
					<span> VS </span>
					<span v-for='(hero, index) in combat.right_team'>
						{{hero.name}}
					</span>
					<span v-if='combat.right_team.length < combat.team_size && combat.right_team.length <= combat.left_team.length' @click.prevent='connect_to_right_team'>[Вступить]</span>
				</div>
			</div>

			<!-- meat grinder combat -->
			<div v-else class='d-flex flex-row'>
				<div>{{combat.name}}</div>
				<div>
					<span v-if='combat.mg_team.length < combat.team_size' @click.prevent='connect_to_mg_team'>[Вступить]</span>
					<span v-for='(hero, index) in combat.left_team'>
						{{hero.name}}
					</span>
				</div>
			</div>
		</div>`,
		data: function () {
			return {
			}
		},
		methods: {
			connect_to_left_team: function () {
				console.log('connected to left team');
			},
			connect_to_right_team: function () {
				console.log('connected to right team');
			},
			connect_to_mg_team: function () {
				console.log('connected to mg team');
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
				<div v-for='(combat, index) in combats'>
					<combat :combat='combat'></combat>
				</div>
			</div>
			
		</div>`,
		data: function () {
			return {
				combats: [],
				loaded: false
			}
		},
		methods: {
			// WS
			onmessage: function (event) {
				this.loaded = true;
				var data = JSON.parse(event.data);
				console.log(data);
				if ('created' in data) {
					console.log('asfsaf')
					this.handle(data.created);
				} else if ('basic' in data) {
					console.log('asf1212412saf')
					this.combats = data.basic;
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
			//BASIC
			handle: function (data) {
				data.forEach(element => this.combats.push(element));
			}
		}
	})

	var vm = new Vue({
	    el: "#app",
	    data: {
	  	    ws: null
	    },
	    mounted: function () {
	  	    this.ws = new WebSocket("ws://127.0.0.1:8000/ws/combats/");
	    }
	})

	vm.ws.onmessage = function (event) {
		vm.$refs.combats.onmessage(event);
	}

});