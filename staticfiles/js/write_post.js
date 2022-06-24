
function runSpeechRecognition() {
    //refrence: https://www.studytonight.com/post/javascript-speech-recognition-example-speech-to-text
    // get output div reference
    var output = document.getElementById("output");
    // get action element reference
    var action = document.getElementById("action");
    // new speech recognition object
    var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition;
    var recognition = new SpeechRecognition();

    // This runs when the speech recognition service starts
    recognition.onstart = function() {
        action.innerHTML = "<small>listening, please speak...</small>";
    };
    
    recognition.onspeechend = function() {
        action.innerHTML = "<small>stopped listening, hope you are done...</small>";
        recognition.stop();
    }
  
    // This runs when the speech recognition service returns result
    recognition.onresult = function(event) {
        var transcript = event.results[0][0].transcript;
        var confidence = event.results[0][0].confidence;
        // output.innerHTML = "<b>Text:</b> " + transcript + "<br/> <b>Confidence:</b> " + confidence*100+"%";
        // output.classList.remove("hide");
        var prev_data = editor.getData()
        var speak_data = prev_data + "<p>" + transcript + "</p>"
        editor.data.set(speak_data);
    };
  
     // start recognition
     recognition.start();
}

$(document).ready(function() {
    navigator.geolocation.getCurrentPosition(function(position) {
        document.getElementById("latitude").value=position.coords.latitude
        document.getElementById("longitude").value=position.coords.longitude
    });
});


function post_create(post_type){
    console.log("post_type__",post_type)
    var frm = $('#post-write-form');
    frm.append('<input type="hidden" name="post_type" value='+post_type+'>');
    event.preventDefault()
    $.ajax({
        type: frm.attr('method'),
        url: '/write-post',
        data: frm.serialize(),
        success: function (data) {
            if (data.status == 200) {
                window.location.href = data.success_url
            }        
        },
        error: function(data) {
            $("#MESSAGE-DIV").html("Something went wrong!");
        }
    });
}


function post_update(post_type){
    console.log("post_type__",post_type)
    var frm = $('#post-write-form');
    frm.append('<input type="hidden" name="post_type" value='+post_type+'>');
    event.preventDefault()
    $.ajax({
        type: frm.attr('method'),
        url: '/edit-write-post/'+post_id,
        data: frm.serialize(),
        success: function (data) {
            if (data.status == 200) {
                window.location.href = data.success_url
            }        
        },
        error: function(data) {
            $("#MESSAGE-DIV").html("Something went wrong!");
        }
    });
}


