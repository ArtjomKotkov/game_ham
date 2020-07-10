  export {request_handler};

  var request_handler = Vue.component('request_handler', {
	props: ['request'],
	data: function () {
	    return {
	    }
	},
	template: `
	<div class='d-none'></div>
	`,
	mounted: function() {
        this.$root.request = this.request
    },
})