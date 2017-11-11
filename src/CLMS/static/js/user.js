$(document).ready(function (){
	//init
	$('#login_password').focus(function(){
		this.value = '';
	});
});
function doLogin() {
	username = $('#login_username').val();
	password = $('#login_password').val();
	$('#login_password')[0].value = hex_md5(password);
	//TODO: Some condition
	$('#frmLogin').ajaxSubmit(function(data) {
		alert(data);
		$('#login_password')[0].value = '';
	});
}