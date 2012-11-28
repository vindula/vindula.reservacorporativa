//FONTE: http://www.htmlstaff.org/ver.php?id=22476

/*
 *    Script:    Mascaras em Javascript
 *    Autor:    Matheus Biagini de Lima Dias
 *    Data:    26/08/2008
 *    Obs:
 */
/*Fun��o Pai de Mascaras*/
function Mascara(o, f){
    v_obj = o
    v_fun = f
    setTimeout("execmascara()", 1)
}

/*Fun��o que Executa os objetos*/
function execmascara(){
    v_obj.value = v_fun(v_obj.value)
}



/*Fun��o que padroniza telefone (11) 4184-1241*/
function Telefone(v){
    if (v.length <= 15) {
        v = v.replace(/\D/g, "")
        v = v.replace(/^(\d\d)(\d)/g, "($1) $2")
        v = v.replace(/(\d{4})(\d)/, "$1-$2")
    }
    else {
        v = limitText(v, 15)
    }
    return v
}

/*Fun��o que padroniza DATA*/
function Data(v){
    if (v.length <= 10) {
        v = v.replace(/\D/g, "")
        v = v.replace(/(\d{2})(\d)/, "$1/$2")
        v = v.replace(/(\d{2})(\d)/, "$1/$2")
    }
    else {
        v = limitText(v, 10)
    }
    return v
}

/*Fun��o que Determina as express�es regulares dos objetos*/
function leech(v){
    v = v.replace(/o/gi, "0")
    v = v.replace(/i/gi, "1")
    v = v.replace(/z/gi, "2")
    v = v.replace(/e/gi, "3")
    v = v.replace(/a/gi, "4")
    v = v.replace(/s/gi, "5")
    v = v.replace(/t/gi, "7")
    return v
}

/*Fun��o que permite apenas numeros*/
function Integer(v){
    return v.replace(/\D/g, "")
}

/*Fun��o que padroniza CPF*/
function Cpf(v){
    if (v.length <= 14) {
        v = v.replace(/\D/g, "")
        v = v.replace(/(\d{3})(\d)/, "$1.$2")
        v = v.replace(/(\d{3})(\d)/, "$1.$2")
        
        v = v.replace(/(\d{3})(\d{1,2})$/, "$1-$2")
    }
    else {
        v = limitText(v, 14)
    }
    return v
}

/*Fun��o que padroniza CEP*/
function Cep(v){
    if (v.length <= 9) {
        v = v.replace(/D/g, "")
        v = v.replace(/^(\d{5})(\d)/, "$1-$2")
    }
    else {
        v = limitText(v, 9)
    }
    return v
}

/*Fun��o que padroniza CNPJ */
function Cnpj(v){
    if (v.length >= 18) {
        v = v.replace(/\D/g, "")
        v = v.replace(/^(\d{2})(\d)/, "$1.$2")
        v = v.replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3")
        v = v.replace(/\.(\d{3})(\d)/, ".$1/$2")
        v = v.replace(/(\d{4})(\d)/, "$1-$2")
    }
    else {
        v = limitText(v, 18)
    }
    return v
}

function FormataCnpj(campo, teclapres){
    var tecla = teclapres.keyCode;
    var vr = new String(campo.value);
    vr = vr.replace(".", "");
    vr = vr.replace("/", "");
    vr = vr.replace("-", "");
    tam = vr.length + 1;
    if (tecla != 14) {
        if (tam == 3) 
            campo.value = vr.substr(0, 2) + '.';
        if (tam == 6) 
            campo.value = vr.substr(0, 2) + '.' + vr.substr(2, 5) + '.';
        if (tam == 10) 
            campo.value = vr.substr(0, 2) + '.' + vr.substr(2, 3) + '.' + vr.substr(6, 3) + '/';
        if (tam == 15) 
            campo.value = vr.substr(0, 2) + '.' + vr.substr(2, 3) + '.' + vr.substr(6, 3) + '/' + vr.substr(9, 4) + '-' + vr.substr(13, 2);
    }
}

function limitText(limit, limitNum) {
        if (limit.length > limitNum) {
            return limit.substring(0, limitNum);
    }     
}
