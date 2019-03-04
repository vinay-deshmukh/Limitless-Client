$(document).on('ready',function(){
    $('#upload_form').submit(function(e){
        e.preventDefault();

        var interval = null;
        var form_data = new FormData($('#upload_form')[0]);
        progress = setInterval(updateProgressBar, 1000);

        function updateProgressBar(){
            $.ajax({
                type: 'POST',
                url: '/upload',
                data: data,
                data: form_data,
                contentType: false,
                processData: false,
                dataType: 'json'
            }).done(function(callback){
                    console.log(callback);
                    if (callback.written_content == "100"){
                        clearInterval(progress);
                    }
                    // Watch out for Cross Site Scripting security issues when setting dynamic content!
                    $('.progress-bar').css('width', callback.written_content+'%').attr('aria-valuenow', callback.written_content);
                    $('.progress-bar-label').text(callback.written_content+'%');
                    clearInterval(progress);
                }).fail(function(data){
                    alert('error!');
            });
        }
    });
});