$(document).ready(function() {
	
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
				  param: this.instance[param]+value,
				}).then((response) => {
				  	this.instance[param] = this.instance[param]+value;
				}).catch((error) => {
				  console.error(error);
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
		    }
		},
		template: `
		<div class='d-flex flex-row'>
			<div v-for='(hero, index) in heroes'>
				<div>{{hero.name}}</div>	
				<div class='d-flex flex-column'>
					<hero_param text='Атака' :instance='hero' param='attack' url='#'></hero_param>
					<hero_param text='Защита' :instance='hero' param='defense' url='#'></hero_param>
					<hero_param text='Мана' :instance='hero' param='mana' url='#'></hero_param>
					<hero_param text='Сила магии' :instance='hero' param='spell_power' url='#'></hero_param>
					<hero_param text='Иницатива' :instance='hero' param='initiative' url='#'></hero_param>
				</div>	
			</div>
		</div>
		`,
		mounted: function() {
	        axios.get(`/user/${this.$root.owner.id}`)
	        .then((response) => {
	        	this.heroes = response.data.heroes
	        }).catch((error) => {
	          console.error(error);
	        });
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
