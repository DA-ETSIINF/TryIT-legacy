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
		// Fake data from server
		$scope.data = {
			enrollment: "w1501XX",
			talks: ["Charla sobre ciberseguridad", "Bitcoins everywhere", "Come to the dart side", "SaaS, the new thing"],
			workshops: ["Android para novatos"],
			ntalks: 20
		}

		// This number is the maximum number of credits
		const maxECTS = 2

		/* 
		 * This number is of credits per assistant. We take the number of workshops and talks assisted 
		 * by the user and divided by the number of talks in that edition.
		 * 
		 * Example 1: If I assisted to 3 talks and 2 workshop and the edition had 10 talks then I would 
		 * have 1 ECTS. 
		 * Example 2: If I assisted to 8 talks and 3 workshop and the edition had 10 talks then I would 
		 * have 2.2 ECTS.
		 */
		const myCredits = (($scope.data.talks.length + $scope.data.workshops)/$scope.data.talks.length) * maxECTS
		
		// If user have more than 2 ECTS, then the real number of ECTS is 2
		$scope.data.ects = Math.min(myCredits, maxECTS)

		// Boolean used for see if data have loaded
		$scope.hasData = true
	}]);

})();