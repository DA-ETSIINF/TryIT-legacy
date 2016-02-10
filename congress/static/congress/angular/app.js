'use strict';

(function () {
	var app = angular.module('ngApp', []);

	app.controller('lastEditionsController', ['$scope', '$http', function ($scope, $http) {
		$scope.sessionActive = {};

		// Petición AJAX
		$scope.openModal = function (id) {
			console.log("click");
			$http.get('/editions-api/sessions/' + id).success(function (data) {
				$scope.sessionActive = data;
				$('#modal').openModal();
			});
		};

	}]);

	app.controller('ticketValidationController', ['$scope', '$http', function ($scope, $http) {
		$scope.attendant = {student: true, upm_student: true, college: 'etsiinf'};

		$scope.createTicket = function () {
			// TODO
			if (!$scope.ticketForm.$valid) {
				console.log("Form invalid");
				return
			}

			$http({
				method: 'POST',
				url: 'create/',
				data: $scope.attendant,
				headers: {'Content-Type': 'application/x-www-form-urlencoded'}
			})
				.success(function (data) {
					// TODO
				});
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

})();