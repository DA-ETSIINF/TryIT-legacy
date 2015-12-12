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
})();