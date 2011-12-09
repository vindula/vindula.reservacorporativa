$j = jQuery.noConflict();

$j(document).ready(function(){

	/* LIST AVAILABLE TIMES */
	
	$j('#available-times #day span').click(function() {
		var list = $j(this).parent().find('ul');
		if (list.is(':hidden')) {
			list.slideDown('fast');
		} else {
			list.slideUp('fast');
			$j(this).parent()
		}
	})
	
	$j('#available-times #day li').click(function() {
		var form = $j('#scheduling-form form');
		var text = 'Dia' +  $j(this).parent().parent().find('span:first').text() + ', das ' + $j(this).find('span').text();
		var date = $j(this).parent().parent().find('input.date').val();
		var start = $j(this).find('input.start').val();
		var end = $j(this).find('input.end').val();
		
		form.find('input[name="date_view"]').val(text);
		form.find('input[name="event_date"]').val(date);
		form.find('input[name="event_start"]').val(start);
		form.find('input[name="event_end"]').val(end);
		
		$j('#available-times #day li').css('background-color', '#FFFFFF');
		$j(this).css('background-color', '#DDDDDD');
	})
	
});