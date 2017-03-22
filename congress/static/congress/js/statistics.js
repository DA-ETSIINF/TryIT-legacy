var ctxAssistance = $("#assistanceChart");
var ctxGrade = $("#gradeChart");

var data;

$(document).ready(function () {

	$.get("/stats/charts").success(function (data) {

		jsonData = JSON.parse(data);
		asistanceData = jsonData.chartAttendants;
		gradeData = jsonData.chartGrade;

		var assistanceChart = new Chart(ctxAssistance, {
			type: 'pie',
			data: {
				'labels': asistanceData.label,
				'datasets': [
					{
						'data': asistanceData.data,
						'backgroundColor': asistanceData.backgroundColor
					}]
			}
		});

		var gradeChart = new Chart(ctxGrade, {
			type: 'bar',
			data: {
				'labels': gradeData.label,
				'datasets': [
					{
						'label': 'Asistencia por curso',
						'data': gradeData.data,
						'backgroundColor': gradeData.backgroundColor
					}]
			}
		});


		var data_test = [70, 80, 65, 78, 58, 80, 78, 80, 70, 50, 75, 65, 80, 70, 65, 90, 65, 80, 70, 65, 90, 65, 78, 58, 80, 78, 80, 70, 50, 75, 65, 80, 70, 65, 90, 65, 80, 70, 65, 90];

		// Bar chart (New tickets today)
		$("#tickets-total").sparkline(data_test, {
			type: 'bar',
			barColor: '#C7FCC9',
			negBarColor: '#81d4fa',
			zeroColor: '#81d4fa',
		});

		// Line chart ( New Invoice)
		$("#tickets-new").sparkline(data_test, {
			type: 'line',
			width: '100%',
			height: '25',
			lineWidth: 2,
			lineColor: '#FFFFFF',
			//fillColor: '#388e3c', // green darken 2
			fillColor: '#E1D0FF', // green darken 2
			highlightSpotColor: '#FFFFFF',
			highlightLineColor: '#FFFFFF',
			minSpotColor: '#000000',
			maxSpotColor: '#f44336',
			spotColor: '#E1D0FF',
			spotRadius: 4,

			//tooltipFormat: $.spformat('{{value}}', 'tooltip-class')
		});

	});
});


