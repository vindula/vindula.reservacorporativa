$j = jQuery.noConflict();

function getHoursSelected(hours_selected){
    var events = [];
    hours_selected.sort();
	
	for(var i = 0; i < hours_selected.length; i++){
		hours_selected[i] = hours_selected[i].split('|');
		exist = false;
		var D = {};
		
		D['date'] = hours_selected[i][0];
        D['start'] = hours_selected[i][1];
        D['end'] = hours_selected[i][2];
		
		for (var j = 0; j < events.length; j++) {
			if ( (events[j]['date'] == D['date']) && (D['start'] == events[j]['end']) ){
                events[j]['end'] = D['end'];
                exist = true;
			}
		}
		
		if (!exist)
            events.push(D);
	}
    return events;
}

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
		var checkbox = $j(this).find('input.hours-selected');
		var mult_horarios = $j('input[name="mult_horarios"]').val() == 'True' ? true : false;
		
		if (mult_horarios) {
			if (checkbox.is(':checked')) {
				checkbox.attr('checked', false);
				$j(this).css('background-color', '#FFFFFF');
			}
			else {
				checkbox.attr('checked', true);
				$j(this).css('background-color', '#DDDDDD');
			}
		}
		else{
			$j('#available-times #day li').css('background-color', '#FFFFFF');

			checkbox.attr('checked', true);
			$j(this).css('background-color', '#DDDDDD');
		}
		form.find('input[name="date_view"]').val(text);
		$j('input[name="create_event"]').attr('disabled',false);
	})
	
	$j('form').submit(function() {
		var checked_elements = $j('input[name="hours-selected:list"]:checked');
		var hours_selected = [];
		msg = "Você deseja reservar um horário: \n\n";
		
		for(var i = 0; i < checked_elements.length; i++){
			hours_selected.push(checked_elements[i].value);
		}
		var hours_selected = getHoursSelected(hours_selected);
		
		for (var i = 0; i < hours_selected.length; i++) {
	        if (hours_selected[i]) {
				date = hours_selected[i]['date'];
				start = hours_selected[i]['start'];
				end = hours_selected[i]['end'];
				msg += "Dia: " + date + " entre as " + start + " e as " + end + "\n";
			}
		}
		
		if(confirm(msg)){
			return true;
		}else{
			return false;
		}
	})

});