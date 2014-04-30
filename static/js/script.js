var myApp={
	init: function(){
		var myLatlng = new google.maps.LatLng(-25.363882,131.044922);
		var mapOptions = {
		    zoom: 4,
		    center: myLatlng
		 };
		var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

		var marker = new google.maps.Marker({
		    position: myLatlng,
		    map: map,
		    title: 'Hello World!'
		});
	},
	validator: {
		login: function(){
			$.validator.setDefaults({
				submitHandler: function(form){
					form.submit();
				}
			});
			$("#formlogin").validate({
				submitHandler: function(form){
					form.submit();
				},
				rules: {
					email: {
						required: true,
						email: true
					},
					password:{
						required:true,
						minlength: 8
					}
				},
				messages:{
					email:{
						required:"Este campo es requerido",
						email: "Ingrese un email válido"
					},
					password:{
						required:"Este campo es requerido",
						minlength:"Ingrese al menos 8 caracteres"
					}
				}
			});
		},
		register: function(){
			$.validator.setDefaults({
				submitHandler: function(form){
					form.submit();
				}
			});
			$.validator.addMethod("leastdigit", function(value) {
			   return /(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])/.test(value);
			});
			$("#formregister").validate({
				submitHandler: function(form){
					form.submit();
				},
				rules: {
					email: {
						required: true,
						email: true
					},
					name: "required",
					password1: {	
						minlength: 8,
						required: true,
						leastdigit: true
					},
					password2: {
						required: true,
						equalTo: "#id_password1"
					}
				},
				messages: {
					email:{
						required: "Este campo es requerido",
						email: "Ingrese un email válido"
					},
					name: {
						required: "Este campo es requerido"
					},
					password1: {
						minlength: "Ingrese al menos 8 caracteres",
						required: "Este campo es requerido",
						leastdigit: "Ingrese al menos un digito y una mayúscula"
					},
					password2: {
						required: "Este campo es requerido",
						equalTo: "Las contraseñas no coinciden"
					}
				}
			});
		}	
	}	
};