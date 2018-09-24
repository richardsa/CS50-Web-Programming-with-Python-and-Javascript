document.addEventListener('DOMContentLoaded', () => {
    // prompt user to set username if not already set
    if (!localStorage.getItem('displayname'))
        $('#login-modal').modal('show');


    const displayNameForm = document.getElementById('display-name-form');
    /* listen for form submit */
    $(displayNameForm ).on('submit', function(e){
         e.preventDefault();
         const displayName = $('#display-name').val();
         console.log(displayName)
         $('#login-modal').modal('hide');
         $('#display-name').val('');
         localStorage.setItem('displayname', displayName);
    });



});
