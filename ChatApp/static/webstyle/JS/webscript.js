
function signup_function(){
    email = document.signup_form.EMAIL.value;
    user = document.signup_form.USERNAME.value;
    password = document.signup_form.PASSWORD.value;
    confirm_password = document.signup_form.CPASSWORD.value;

    if (email==null || email==""){
        alert("Email field can't be empty");
        return false
    }
    else if(user== null || user== ""){
        alert("Username can't be empty");
        return false
    }
    else if(password.length<8){
        alert("Password must be at least 8 characters");
        return false
    }
    else if(password==null || password==""){
        alert("Password field can't be empty");
        return false
    }
    else if(password==confirm_password){
        return true
    }
    else if(password != confirm_password){
        alert("Password Not Matching");
        return false
    }
}

function signin_function(){
    user = document.Signin_form.USERNAME.value;
    pass = document.Signin_form.PASSWORD.value;

    if(user==null || user==""){
        alert('Enter username ')
        return false
    }
    else if(pass==null || pass==""){
        alert("Enter Password ")
        return false
    }
}