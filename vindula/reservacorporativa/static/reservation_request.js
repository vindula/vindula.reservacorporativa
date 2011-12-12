$j = jQuery.noConflict();

$j(document).ready(function(){
	
	/* AJAX RESERVE INFORMATION */

	getInfoReserve();
	
	$j('#reserves').change(function() {
		getInfoReserve();
	});

	function getInfoReserve() {
		$j("#reserves option:selected").each(function () {
	 		var reserve = $j(this).val();
			var url = $j('#view-info-reserve').val();
			$j.get(url,{ id: reserve }, function(data){
				$j('#info-reserve').html(data);
			});
		});
	}

	/* AJAX LOADER */
	
	$j('#info-reserve').ajaxStart(function(){  
	   $j(this).hide();  
	   $j('#ajax-loader').show();
	});  
	
	$j('#info-reserve').ajaxStop(function(){  
	   $j(this).show();  
	   $j('#ajax-loader').hide();
	}); 	
	
});