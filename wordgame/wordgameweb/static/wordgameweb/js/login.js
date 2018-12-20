$( document ).ready(function() {
    
    $('#toggle_sign_up_btn').on('click', function(){

    	//hide the sign up section 
    	$('#SignInSection').hide();
    	$('#SignUpSection').show();

    });

    $('#toggle_sign_in_btn').on('click', function(){

    	//hide the sign in section 
    	$('#SignUpSection').hide();
    	$('#SignInSection').show();

    });


});