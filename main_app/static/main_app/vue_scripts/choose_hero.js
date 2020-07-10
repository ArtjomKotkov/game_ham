$(document).ready(function() {

	axios.defaults.xsrfCookieName = 'csrftoken'
	axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

	Vue.component('heroes', {
		data: function () {
		    return {
		    	items:null,
		    	current_hero:null,
		    }
		},
		template: `
		<div>
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

	var vm = new Vue({
		el: "#app",
		data: {
		},
		delimiters: ['[[', ']]']
	})

});



