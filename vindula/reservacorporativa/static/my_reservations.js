$j = jQuery.noConflict();

$j(document).ready(function(){
	var common_content_filter = '#content=*,dl.portalMessage.error,dl.portalMessage.info';
	var common_jqt_config = {fixed:false,speed:'fast',mask:{color:'#000',opacity: 0.4,loadSpeed:0,closeSpeed:0}};
	
	$j('a.editReservation').prepOverlay({
        subtype: 'ajax',
        filter: common_content_filter,
        closeselector: '[name=form.button.cancel],[name=form.actions.cancel]',
        formselector: '[id=zc.page.browser_form],[name=edit_form]',
        noform:'reload',
        width: '50%',
        config: common_jqt_config
    });
	
	$j('.delete-reserve').click(function(){
        var id = $j(this).parent().find('#id_event').val()
		if (confirm("Deseja mesmo excluir esta reserva?")){
			var url = $j(this).prevAll('#ab_url').val()
			window.location.href=window.location.href + '?delete-ev=' + id;
		}
		
    });
	
})
