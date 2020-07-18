$(document).ready(function() {

	axios.defaults.xsrfCookieName = 'csrftoken'
	axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

	Vue.component('heroes', {
		data: function () {
		    return {
		    	items:null,
		    	current_hero:0,
		    }
		},
		template: `
		<div style='height: 100vh;'>
			<div class='info-box d-flex flex-row' style='height: 70vh;'>
				<div class='w-25 h-100 d-inline-block'>
					<div v-for='(value, key) in items[current_hero].stats'>
						{{key}}: {{value}}
					</div>
				</div>
				<div class='w-75 h-100 d-inline-block'>

				</div>
			</div>
			<div class='unit-box' style='height: 10vh;'>
			</div>
			<div class='heroes-box d-flex flex-column justify-content-around align-items-center' style='height: 20vh;'>
				<div class='d-flex flex-row justify-content-center align-items-center'>
					<div v-for='(item, index) in items' @click='current_hero = index''>
						<img :src="item.image" :alt="item.name" class='hero-box' width='120px' height='120px' :class='{"selected-hero": current_hero==index}'/>
					</div>
				</div>
				<button @click='send' type="button" class="btn btn-danger">Далее</button>
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
				form.append('hero_class', this.items[this.current_hero].class_name)
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



