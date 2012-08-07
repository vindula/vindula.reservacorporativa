//FONTE: http://forum.imasters.com.br/topic/409072-mascara-simples-de-campo/

/*
*    Script:    Mascaras em Javascript
*    Autor:   Jair Humberto
*    Data:    20/01/2005
*    Obs:    
*/

    /*Função data*/
	function mascara(m, o) {
		o.onkeyup = function(e) {
		if(e.keyCode != 8) {
			var array_m = m.split('')
			var array_o_value = o.value.split('')
			retorno = new Array()
			for(var i=0; array_o_value[i]; i++) {
				retorno[i] = array_m[i] == '#' ? array_o_value[i] : array_m[i]
			    if(i == array_o_value.length - 1 && array_m[i+1] && array_m[i+1] != '#') retorno[i+1] = array_m[i+1]
			    	}            
			         o.value = retorno.join('')
			              }
			        }
			}

	    /*Função telefone*/
	 function Mascara(objeto){
	 	 if(objeto.value.length == 0)
			objeto.value = '(' + objeto.value;	
			if(objeto.value.length == 3)
			     objeto.value = objeto.value + ')';
				 if(objeto.value.length == 8)
				     objeto.value = objeto.value + '-';
				}
			
//FONTE: http://www.htmlstaff.org/ver.php?id=22476

/*
*    Script:    Mascaras em Javascript
*    Autor:    Matheus Biagini de Lima Dias
*    Data:    26/08/2008
*    Obs:    
*/

    /*Função Pai de Mascaras*/
    function Mascara(o,f){
        v_obj=o
        v_fun=f
        setTimeout("execmascara()",1)
    }
    
    /*Função que Executa os objetos*/
    function execmascara(){
        v_obj.value=v_fun(v_obj.value)
    }
    
    /*Função que permite apenas numeros*/
    function Integer(v){
        return v.replace(/\D/g,"")
    }
    
       
    /*Função que padroniza CEP*/
    function portal_address(v){
        v=v.replace(/D/g,"")                
        v=v.replace(/^(\d{5})(\d)/,"$1-$2") 
        return v
    }
    
    /*Função que padroniza CNPJ*/
    function Cnpj(v){
        v=v.replace(/\D/g,"")                   
        v=v.replace(/^(\d{2})(\d)/,"$1.$2")     
        v=v.replace(/^(\d{2})\.(\d{3})(\d)/,"$1.$2.$3") 
        v=v.replace(/\.(\d{3})(\d)/,".$1/$2")           
        v=v.replace(/(\d{4})(\d)/,"$1-$2")              
        return v
    }
    


