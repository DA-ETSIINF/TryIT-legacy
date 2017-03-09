var mytoken = "";
var element = "";
var mId = 0;

// Get a winner
function getWinner(id) {
	mId = id;

	if (mytoken !== "") {

		$(element).addClass('disabled');
		$(element).html('<i class="fa fa-cog fa-spin fa-3x fa-fw" style="margin-right:5px;"></i><span class="sr-only">Loading...</span>Obteniendo ganador...');

		$.ajax({
			url: "/contests-winners/" + mId + "/",
			type: "post",
			data: JSON.stringify({"token": mytoken, "id": mId}),
			headers: {'Content-Type': 'application/x-www-form-urlencoded'}
		})
			.done(function (json) {
				$(element).html('<i class="fa fa-check" style="margin-right:5px;"></i>Ganador encontrado');
				$(element).parent().parent().find("#winnerName").text("Ganador: Pepito Perez de Castro");
			})
			.fail(function (xhr, status, errorThrown) {
				$("#labelforpassword").attr("data-error", "Ocurrió un problema con la petición. Inténtalo de nuevo.");
				$("#password").addClass('invalid');

				$("#butonacces").removeClass('disabled');
				$("#butonacces").html('<i class="fa fa-lock" aria-hidden="true" style="margin-right: 5px;"></i>Continuar');
			});


	} else {
		$('#modalsec').modal('open');
	}

}


$(document).ready(function () {

	$('select').material_select();
	$('.modal').modal({
		dismissible: true, // Modal can be dismissed by clicking outside of the modal
		opacity: .5, // Opacity of modal background
		inDuration: 450, // Transition in duration
		outDuration: 200, // Transition out duration
		startingTop: '10%', // Starting top style attribute
		endingTop: '20%', // Ending top style attribute
		ready: function (modal, trigger) {
			$('#password').focus();
		},
		complete: function () {

		} // Callback for Modal close
	});

	// Submit Process of Code.
	$("#inputform").submit(function (e) {
		e.preventDefault();
		var password = document.getElementById("password").value;
		if (password === "") {
			$('#password').focus();
			$("#labelforpassword").attr("data-error", "Este campo no puede estar vacío.");
			$("#password").addClass('invalid');

		} else {
			$('#password').focus();
			$("#butonacces").addClass('disabled');
			$("#butonacces").html('<i class="fa fa-cog fa-spin fa-3x fa-fw" style="margin-right:5px;"></i><span class="sr-only">Loading...</span>Verificando...');

			mytoken = document.getElementById("password").value;
			getWinner(mId);

			// $.ajax({
			// 	url: "modal.html",
			// 	data: {
			// 		code: document.getElementById("password").value
			// 	},
			// 	type: "POST",
			// 	dataType: "html",
			// })
			//
			// 	.done(function (json) {
			// 		//Executes the winner function with the json token provided.
			// 		// OJO AL TOKEN DE PRUEBA.
			// 		mytoken = "pepe";
			// 		setTimeout(function () {
			// 			$("#rowcontent").addClass('scale-transition');
			// 			$("#rowcontent").addClass('scale-out');
			// 			$("#butonacces").removeClass('disabled');
			// 			$("#butonacces").html('<i class="fa fa-lock" aria-hidden="true" style="margin-right: 15px;"></i>Continuar');
			//
			// 			setTimeout(function () {
			// 				$("#rowcontent").html('<h5 class="center-align"><i class="fa fa-check" aria-hidden="true" style="margin-right: 5px;"></i>Identificación correcta</h5>');
			// 				$("#rowcontent").addClass('scale-in');
			// 				$("#rowcontent").removeClass('scale-out');
			// 				$("#rowcontent").removeClass('scale-in');
			//
			// 				setTimeout(function () {
			// 					$('#modalsec').modal('close');
			// 					setTimeout(function () {
			// 						getWinner();
			// 					}, 1000);
			//
			// 				}, 2000);
			// 			}, 500);
			// 		}, 1000);
			//
			// 	})
			//
			// 	.fail(function (xhr, status, errorThrown) {
			// 		$("#labelforpassword").attr("data-error", "Ocurrió un problema con la petición. Inténtalo de nuevo.");
			// 		$("#password").addClass('invalid');
			//
			// 		$("#butonacces").removeClass('disabled');
			// 		$("#butonacces").html('<i class="fa fa-lock" aria-hidden="true" style="margin-right: 5px;"></i>Continuar');
			//
			// 		console.log("Error: " + errorThrown);
			// 		console.log("Status: " + status);
			// 		console.dir(xhr);
			// 	});


		}

	});


});
