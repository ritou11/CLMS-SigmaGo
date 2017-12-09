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
		if(data=='Success'){
			self.location.href = '/userinfo'
		}
		$('#login_password')[0].value = '';
	});
}
function doRegister() {
	username = $('#reg_username').val();
	password = $('#reg_password1').val();
	password2 = $('#reg_password2').val();
	if (password != password2) {
		alert('The passwords entered twice are not the same!');
		return;
	}
	if (password.length < 7) {
		alert('Password is too short!');
		return;
	}
	if (username == password) {
		alert('Password cannot be the same as username.');
		return;
	}
	$('#reg_password1')[0].value = $('#reg_password2')[0].value = hex_md5(password);
	$('#frmRegister').ajaxSubmit(function(data) {
		alert(data);
		$('#reg_password1')[0].value = '';
		$('#reg_password2')[0].value = '';
	})
}
