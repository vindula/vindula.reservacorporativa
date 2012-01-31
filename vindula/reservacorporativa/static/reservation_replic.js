$j = jQuery.noConflict();

function replic(){
	var check = $j('#form-widgets-replic_semana-0').attr('checked');
	if (check != null) {
		if (check == true) {
			$j('input[type="checkbox"].single-checkbox-widget').each(function(){
				this.checked = true;
			});
			$j('input[type="text"].time-field').each(function(){
				if (/(_start|_end)$/.test(this.id)) {
					this.disabled = true;
				};
							});
			
			$j('#form-widgets-mon_start').removeAttr('disabled');
			$j('#form-widgets-mon_end').removeAttr('disabled');
			
		}
		else {
			$j('input[type="checkbox"].single-checkbox-widget').each(function(){
				this.checked = false;
				this.value = '';
			});
			$j('input[type="text"].time-field').each(function(){
				this.disabled = false;
				this.value = '';
			});
		};
	};
};

$j(document).ready(function(){

	replic();
	$j('#form-widgets-replic_semana-0').click(function() {
		replic();
	});

	$j('#form-widgets-mon_start').keyup(function(){
		var check = $j('#form-widgets-replic_semana-0').attr('checked');
		var valor = this.value; 
		if (check == true) {
			$j('input[type="text"].time-field').each(function(){
				if (/_start$/.test(this.id)) {
					this.value = valor;
				};
			});
		};
		
	});
	$j('#form-widgets-mon_end').keyup(function(){
		var check = $j('#form-widgets-replic_semana-0').attr('checked');
		var valor = this.value; 
		if (check == true) {
			$j('input[type="text"].time-field').each(function(){
				if (/_end$/.test(this.id)){
					this.value = valor;
				};
			});
		};
	});
	
	$j('#form-buttons-save').click(function(){
		$j('input[type="text"].time-field').each(function(){
			if (/(_start|_end)$/.test(this.id)) {
				this.disabled = false;
			};
		});	

	});

});
