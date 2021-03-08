'use strict';


// Live
fetch(`${window.location.origin}/streaming/api`)
	.then(r => r.json())
	.then(res => {
		if (res.streaming && window.location.pathname === '/streaming/') {
			document.getElementById('streaming-title').innerText = res.title;
			const regex = /v=(.*)$/gm;
			if (res["url"].includes("youtube")) {
				document.getElementById('youtube-iframe').setAttribute('src', `https://www.youtube.com/embed/${(regex.exec(res["url"]))[1]}`);
				const showYoutube = true;
			} else if (res["url"].includes("twitch")) {
				const div = document.createElement("div");
				div.setAttribute("id", "twitch-embed")
				document.getElementById("video-player").appendChild(div);
				new Twitch.Embed("twitch-embed", {
					width: 854,
					height: 480,
					channel: "tryit2021",
				});
				const showTwitch = true;
			}
		} else if (res.streaming) {
			Materialize.toast('<div class="tv"><i class="tv-live-icon material-icons">tv</i><div class="tv-container"></div><div class="tv-dot"></div></div><span class="tv-text">¡Estamos en directo!</span>')
			const toast = document.querySelector('.toast').addEventListener('click', () => window.location = `/streaming`);
		} else {
			document.getElementById('streaming-title').innerText = 'Actualmente el directo no está disponible';
		}
	});
let i = 10;
(function () {
	var app = angular.module('ngApp', []);

	app.controller('editionsController', ['$scope', '$http', '$location', function ($scope, $http, $location) {
		$scope.sessionActive = {};

		// Petición AJAX
		$scope.openModal = function (id) {
			$http.get('/editions-api/sessions/' + id).success(function (data) {
				$scope.sessionActive = data;
				$('#modal').modal('open');
				$location.url(id);
			});
		};

		var init = function () {
			if ($location.url()) {
				$scope.openModal($location.url().split('/')[1]);
			}
		};

		init();

	}]);

	app.controller('AsistenciaController', ['$scope', '$http', function ($scope, $http) {
		$scope.sendAsistencia = function () {
			if (!$scope.asistencia.$valid || [undefined, null, ""].includes($scope.student_id)) {
				i += 1;
				$scope.formErrorSubmit = true;
				$scope.textError = "Debes poner una matricula";
				return
			}
			console.log("Sending to the back, and I recommend you to not automatize call")

			$scope.btnSubmited = true;
			$scope.formErrorSubmit = false;

			const csrf = document.querySelector("[name='csrfmiddlewaretoken']").value;
			$http({
				method: 'POST',
				url: 'api',
				data: { "this_is_not_automated": $scope.student_id },
				headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf }
			}).then(function successCallback(response) {
				$scope.responseSuccess = true;
				$scope.textError = "";
			}, function errorCallback(response) {
				$scope.textError = "Ha habido un error";
				$scope.formErrorSubmit = true;
				$scope.btnSubmited = false;
			}
			);
		};
	}])

	app.controller('ticketValidationController', ['$scope', '$http', function ($scope, $http) {
		$scope.attendant = { student: true, is_upm_student: true, college: "10" };

		$scope.textError = 'Revisa los datos introducidos';
		$scope.formErrorSubmit = false;
		$scope.responseSuccess = false;
		$scope.btnSubmited = false;
		$scope.conditions = false;

		$http.get('/editions-api/schools')
			.then(function (res) {
				$scope.colleges = res.data;
				$scope.degrees = $scope.colleges[9].degrees;
				$scope.attendant.college = $scope.colleges[9].code;
				$scope.attendant.degree = $scope.degrees[10].code;
			});

		$scope.collegeSelected = function () {
			for (var i = 0; i < $scope.colleges.length; i++) {
				if ($scope.colleges[i].code === $scope.attendant.college) {
					$scope.degrees = $scope.colleges[i].degrees;
					$scope.attendant.degree = $scope.degrees[0].code;
					break;
				}
			}
		};

		$scope.createTicket = function () {
			if (!$scope.ticketForm.$valid || !$scope.conditions) {
				$scope.formErrorSubmit = true;
				return
			}

			$scope.btnSubmited = true;
			$scope.formErrorSubmit = false;
			$http({
				method: 'POST',
				url: 'create/',
				data: $scope.attendant,
				headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
			}).then(function successCallback(response) {
				$scope.responseSuccess = true;
			}, function errorCallback(response) {
				if (response.status == 400) {
					$scope.textError = response.data.message;
				}
				else {
					$scope.textError = 'Error';
				}
				$scope.formErrorSubmit = true;
				$scope.btnSubmited = false;
			}
			);
		};



		// DNI/NIE regex
		$scope.identityPattern = (function () {
			var regexp = /^[x-z]{1}[-]?\d{7}[-]?[a-z]{1}$|^\d{8}[-]?[a-z]{1}$/i;
			return {
				test: function (value) {
					if (!$scope.attendant.student || !$scope.attendant.is_upm_student) {
						return true;
					}
					return regexp.test(value);
				}
			}
		})();

	}]);

	app.controller('volunteersValidationController', ['$scope', '$http', function ($scope, $http) {
		$scope.volunteer = { android: false, shirt: 'm', schedule_options: [] };

		$scope.shirts = [{ id: 's', value: 'S' }, { id: 'm', value: 'M' }, { id: 'l', value: 'L' },
		{ id: 'xl', value: 'XL' }, { id: 'xxl', value: 'XXL' }];
		$scope.textError = 'Revisa los datos introducidos';
		$scope.formErrorSubmit = false;
		$scope.responseSuccess = false;
		$scope.conditions = false;
		$scope.conditionsVolunteers = false;
		$scope.btnSubmited = false;

		$scope.onCheckboxClick = (e) => {
			console.log(e)
		}

		$scope.submitForm = function () {
			if (!$scope.volunteersForm.$valid || !$scope.conditions || !$scope.conditionsVolunteers) {
				$scope.formErrorSubmit = true;
				return
			}
			Object.keys($scope.volunteer.schedule).map(key => {
				$scope.volunteer.schedule_options.push({ "schedule_type": key.split('_')[0], "date": key.split('_')[1] })
			})
			$scope.btnSubmited = true;
			$scope.formErrorSubmit = false;
			$http({
				method: 'POST',
				url: 'send/',
				data: $scope.volunteer,
				headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
			}).then(() => {
				$scope.volunteer.schedule_options = []
				$scope.responseSuccess = true;
			}, res => {
				$scope.textError = res.data.message !== undefined ? res.data.message : 'Error';
				$scope.formErrorSubmit = true;
				$scope.btnSubmited = false;
			}
			);
		};

	}]);

	app.controller('EscapeRoomValidationController', ['$scope', '$http', function ($scope, $http) {

		$scope.getDayName = (d) => {
			d = new Date(d);
			return d.toLocaleString(window.navigator.language, { weekday: 'long' });
		}

		$scope.getDate = (d) => {
			d = new Date(d);
			return `${d.getDate()} de ${d.toLocaleString(window.navigator.language, { month: 'long' })}`;
		}

		$scope.getCheckboxText = (session) => {
			const date = new Date(session.date);
			const hour = date.getHours();
			const minutes = date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes();
			return `${hour}:${minutes} | ${session.available} `
		}

		$scope.btnSubmited = false;
		$scope.responseSuccess = false;
		$scope.textError = '';
		$scope.attendant = { "identity": "" };
		$scope.session = 0;


		$http({
			method: 'GET',
			url: '/events/escape-room/api',
			headers: { 'Content-Type': undefined }
		}).then(res => {
			$scope.apiData = []
			let lastDate = "";
			const days = [];

			res.data[0].sessions.map(session => {
				const date = session.date.split('T')[0];
				if (lastDate !== date) {
					$scope.apiData.push([]);
				}
				lastDate = date;
				$scope.apiData[$scope.apiData.length - 1].push(session);
			});
		}, err => {
			$scope.textError = 'Ha habido un error. Vuelve a intentarlo en unos minutos.';
		})
		$scope.justCheckOne = function (id) {
			Array.from(document.querySelectorAll(".lightgreenTryIT.checkbox")).map(cb => cb.checked = false);
			document.getElementById(id).checked = true;
			$scope.session = id;
		};

		$scope.submitForm = function () {
			$scope.textError = validateNIF_NIE($scope.attendant.identity);
			if ($scope.textError !== '') {
				return
			}

			if ($scope.session === undefined) {
				$scope.textError = "Seleccione una sesión"
				return
			}
			$scope.btnSubmited = true;

			const csrf = document.querySelector("[name='csrfmiddlewaretoken']").value;
			$http({
				method: 'POST',
				url: `/events/escape-room/session/${$scope.session}/`,
				data: { "identity": $scope.attendant.identity },
				headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf }
			}).then(res => {
				$scope.responseSuccess = true;
			}, err => {
				$scope.textError = err.status == 400 ? err.data.message : 'Error';
				$scope.btnSubmited = false;
			}
			);
		}
	}]);

	app.controller('registerValidationController', ['$scope', '$http', function ($scope, $http) {
		$scope.registerCompany = { sponsor: false, sponsorType: 'oro', type: 'ponencia' };

		$scope.textError = 'Revisa los datos introducidos';
		$scope.formErrorSubmit = false;
		$scope.btnSubmited = false;

		$scope.submitForm = function () {
			if (!$scope.registerForm.$valid) {
				$scope.formErrorSubmit = true;
				return
			}

			$scope.btnSubmited = true;
			$scope.formErrorSubmit = false;

			var fd = new FormData();
			var doc = $("#document")[0].files[0];
			fd.append('document', doc);

			for (var key in $scope.registerCompany) {
				if ($scope.registerCompany.hasOwnProperty(key)) {
					fd.append(key, $scope.registerCompany[key]);
				}
			}

			$http({
				method: 'POST',
				url: 'send/',
				data: fd,
				headers: { 'Content-Type': undefined }
			}).then(function successCallback(response) {
				$scope.responseSuccess = true;
			}, function errorCallback(response) {
				if (response.status == 400) {
					$scope.textError = response.data.message;
				}
				else {
					$scope.textError = 'Error';
				}
				$scope.formErrorSubmit = true;
				$scope.btnSubmited = false;
			}
			);
		};

	}]);


	app.controller('attendanceController', ['$scope', '$http', function ($scope, $http) {
		// This number is the maximum number of credits
		const maxECTS = 2


		// Boolean used for see if data have loaded
		$scope.hasData = false

		$scope.currentYears = []
		let currentYear = new Date().getFullYear()
		const counterYear = 2016
		while (counterYear <= currentYear) {
			$scope.currentYears.push(currentYear--)
		}


		$scope.searchECTS = function () {
			$scope.dni_nie_error = validateNIF_NIE($scope.dni_nie)

			if ($scope.dni_nie_error === "") {
				let url = window.location.href
				if (url.substring(url.length - 1) === '?') {
					url = url.substring(0, url.length - 1)
				}

				fetch(`${url}${$scope.dni_nie}&${$scope.edition}`)
					.then(res => res.json())
					.then(json => {
						$scope.data = json[0]
						$scope.edition_error = ""
						if ($scope.data === undefined || $scope.data.talks.length === 0) {
							$scope.edition_error = 'No hay información disponible'
							$scope.hasData = false
							return
						}

						if (new Date($scope.data.first_day_of_event) > new Date()) {
							$scope.edition_error = `Todavía no hay información de la edición de ${$scope.edition}`
							$scope.hasData = false
							return
						}

						$scope.data.talks = $scope.data.talks.map(talk => {
							const date = new Date(talk.session__start_date)
							return `${date.getDate()}/${date.getMonth() + 1}/${date.getFullYear()} : ${talk.session__title}`
						})

						/*
						* This number is of credits per assistant. We take the number of workshops and talks assisted 
						* by the user and divided by the number of talks in that edition.
						*
						* Example 1: If I assisted to 3 talks and 2 workshop and the edition had 10 talks then I would 
						* have 1 ECTS.
						* Example 2: If I assisted to 8 talks and 3 workshop and the edition had 10 talks then I would 
						* have 2.2 ECTS.
						*/

						let myCredits = $scope.data.ntalks === 0 ? 0 : ($scope.data.talks.length / $scope.data.ntalks) * maxECTS
						myCredits = Math.round(myCredits * 100) / 100

						// If user have more than 2 ECTS, then the real number of ECTS is 2
						$scope.data.ects = Math.min(myCredits, maxECTS)

						$scope.hasData = true;
					})
					.catch(err => {
						console.log(err);
					})
			}
		}
	}]);

})();

// Checks if NIF or NIE are OK
function validateNIF_NIE(value) {
	if (value === undefined) {
		return "El DNI/NIE es obligatorio"
	}
	const validChars = 'TRWAGMYFPDXBNJZSQVHLCKET'
	const nifRexp = /^[0-9]{8}[TRWAGMYFPDXBNJZSQVHLCKET]{1}$/i
	const nieRexp = /^[XYZ]{1}[0-9]{7}[TRWAGMYFPDXBNJZSQVHLCKET]{1}$/i
	const str = value.toString().toUpperCase()

	if (!nifRexp.test(str) && !nieRexp.test(str))
		return "Comprueba el DNI/NIE. Debe tener letra."

	const nie = str
		.replace(/^[X]/, '0')
		.replace(/^[Y]/, '1')
		.replace(/^[Z]/, '2')

	const letter = str.substr(-1)
	const charIndex = parseInt(nie.substr(0, 8)) % 23

	if (validChars.charAt(charIndex) === letter) {
		return ""
	} else
		return "Comprueba el DNI/NIE."
}
