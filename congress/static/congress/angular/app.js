'use strict';

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

	app.controller('ticketValidationController', ['$scope', '$http', function ($scope, $http) {
		$scope.attendant = {student: true, upm_student: true, college: "10"};

		$scope.textError = 'Revisa los datos introducidos';
		$scope.formErrorSubmit = false;
		$scope.responseSuccess = false;
		$scope.btnSubmited = false;

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
			if (!$scope.ticketForm.$valid) {
				$scope.formErrorSubmit = true;
				return
			}

			$scope.btnSubmited = true;
			$scope.formErrorSubmit = false;
			$http({
				method: 'POST',
				url: 'create/',
				data: $scope.attendant,
				headers: {'Content-Type': 'application/x-www-form-urlencoded'}
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
					if (!$scope.attendant.student || !$scope.attendant.upm_student) {
						return true;
					}
					return regexp.test(value);
				}
			}
		})();

	}]);

	app.controller('volunteersValidationController', ['$scope', '$http', function ($scope, $http) {
		$scope.volunteer = {android: false, shirt: 'm'};

		$scope.shirts = [{id: 's', value: 'S'}, {id: 'm', value: 'M'}, {id: 'l', value: 'L'},
			{id: 'xl', value: 'XL'}, {id: 'xxl', value: 'XXL'}];
		$scope.textError = 'Revisa los datos introducidos';
		$scope.formErrorSubmit = false;
		$scope.responseSuccess = false;
		$scope.btnSubmited = false;

		$http.get('/editions-api/schools')
			.then(function (res) {
				$scope.colleges = res.data;
				$scope.degrees = $scope.colleges[9].degrees;
				$scope.volunteer.college = $scope.colleges[9].code;
				$scope.volunteer.degree = $scope.degrees[10].code;
			});

		$scope.collegeSelected = function () {
			for (var i = 0; i < $scope.colleges.length; i++) {
				if ($scope.colleges[i].code === $scope.volunteer.college) {
					$scope.degrees = $scope.colleges[i].degrees;
					$scope.volunteer.degree = $scope.degrees[0].code;
					break;
				}
			}
		};

		$scope.submitForm = function () {
			if (!$scope.volunteersForm.$valid) {
				$scope.formErrorSubmit = true;
				return
			}

			$scope.btnSubmited = true;
			$scope.formErrorSubmit = false;
			$http({
				method: 'POST',
				url: 'send/',
				data: $scope.volunteer,
				headers: {'Content-Type': 'application/x-www-form-urlencoded'}
			}).then(function successCallback(response) {
					$scope.responseSuccess = true;
				}, function errorCallback(response) {
					if (response.status === 400) {
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

	app.controller('registerValidationController', ['$scope', '$http', function ($scope, $http) {
		$scope.registerCompany = {sponsor: false, sponsorType: 'oro', type: 'ponencia'};

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
				headers: {'Content-Type': undefined}
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


		$scope.searchECTS = function (){
			$scope.dni_nie_error = validateNIF_NIE($scope.dni_nie)
			if($scope.dni_nie_error === ""){
				fetch(`${window.location.href}${$scope.dni_nie}`)
					.then(res => res.json())
					.then(json => {
						$scope.data = json[0];
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
						const myCredits = $scope.data.ntalks === 0 ? 0 : ($scope.data.talks.length/$scope.data.ntalks) * maxECTS

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
	}else
		return "Comprueba el DNI/NIE."
}