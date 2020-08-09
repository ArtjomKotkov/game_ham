export {loading};


var loading = Vue.component('loading', {
  data: function () {
	return {
	}
  },
  template: `
	<div>
		<loading_default ref='load' v-if='$root.battle_type=="DF"'></loading_default>
	</div>`,
})

var loading = Vue.component('loading_default', {
  data: function () {
	return {
		teams: null,
		loaded: false,
	}
  },

  template: `
	<div>
		<div class="contaner-fluid">
			<div class="row" v-if='loaded == true'>

				<div class="col-4">
					<div v-for='(hero, index) in teams.left' class='d-flex flex-column'>
						<loading_hero_block :hero='hero' :index='index'></loading_hero_block>
					</div>
				</div>
				<div class="col-2"></div>
				<div class="col-4">
					<div v-for='(hero, index) in teams.right' class='d-flex flex-column'>
						<loading_hero_block :hero='hero' :index='index'></loading_hero_block>
					</div>
				</div>
			</div>
		</div>
	</div>`,

	mounted: function () {
		var left_team = []
		var right_team = []

		for (let key in this.$root.heroes) {
			var value = this.$root.heroes[key];
			if (value.team == 'left') {
				left_team.push(value);
			}
			if (value.team == 'right') {
				right_team.push(value);
			}
		}
		this.teams = {
			left: left_team,
			right: right_team
		}
		this.loaded = true;
	},
	methods: {
		handle_commands: function (request) {
			console.log(request);
		},
	},

	computed: {
		all_ready: function () {
			var heroes_ready = []
			for (let key in this.$root.heroes) {
				var value = this.$root.heroes[key];
				heroes_ready.push(value.ready);
			}
			return heroes_ready.every(elem => elem == true) ? true : false
		}
	}

})

Vue.component('loading_hero_block', {
	props: ['hero', 'index'],
	data: function () {
		return {
			teams: null,
		}
	},
	template: `
	<div :class="{'hero-block-ready': hero.ready, 'hero-block-unready': !hero.ready}">
		<div>
			<img :src="hero.image" alt="Hero icon." />
		</div>
		<div>
			<div>{{hero.name}} <button @click='set_ready(index)'>Set Ready</button></div>
		</div>
	</div>`,

	methods: {
		set_ready: function (hero_index) {
			this.$root.manager.set_ready(hero_index);
		}
	}
})