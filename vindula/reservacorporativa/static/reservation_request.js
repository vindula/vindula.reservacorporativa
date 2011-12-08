$j = jQuery.noConflict();

$j(document).ready(function(){
	
	/* AJAX RESERVE INFORMATION */
	
	$j('#reserves').change(function() {
		$j("#reserves option:selected").each(function () {
	 		var reserve = $j(this).val();
			var url = $j('#view-info-reserve').val();
			$j.get(url,{ id: reserve }, function(data){
				$j('div#info-reserve').html(data);
			});
		});
	});
	
	/* AJAX LOADER */
	
	$j('div#info-reserve').ajaxStart(function(){  
	   $j(this).hide();  
	   $j('div#ajax-loader').show();
	});  
	
	$j('div#info-reserve').ajaxStop(function(){  
	   $j(this).show();  
	   $j('div#ajax-loader').hide();
	}); 

});