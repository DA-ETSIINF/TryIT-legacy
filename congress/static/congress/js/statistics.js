var ctx = $("#assistanceChart");

$(document).ready(function () {
	$.get("/stats/charts").success(function (data) {

		var assistanceChart = new Chart(ctx, {
			type: 'pie',
			data: JSON.parse(data),
			options: {
				animation: {
					animateScale: true
				}
			}
		});

	});
});