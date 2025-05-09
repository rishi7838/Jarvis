$(document).ready(function () {
    $('.text').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "bounceIn",

        },
        out: {
            effect: "bounceOut",

        },

    });

    // siri waves configuration
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 800,
        height: 200,
        style: "ios9",
        amplitude: "1",
        speed: "0.30",
        autostart: true
    });

    //siri msg animation

    $('.siri-message').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "fadeInUp",
            sync: true,

        },
        out: {
            effect: "fadeOutUp",
            sync: true,
        },

    });

    //mic button click event
    $("#Micbtn").click(function () {
        eel.playAssistantSound()

        $("#oval").attr("hidden", true);         // hide oval
        $("#SiriWave").removeAttr("hidden");     // show SiriWave
        eel.allCommands()()
    });

    function doc_keyUp(e) {
        // this would test for whichever key is 40 (down arrow) and the ctrl key at the same time

        if (e.key === 'j' && e.metaKey) {
            eel.playAssistantSound()
            $("#oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands()()
        }
    }
    document.addEventListener('keyup', doc_keyUp, false);


    // Handle message from input
    function PlayAssistant(message) {

        if (message != "") {

            $("#oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands(message);
            $("#chatbox").val("")
            $("#Micbtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);

        }

    }

    // toogle fucntion to hide and display mic and send button 
    function ShowHideButton(message) {
        console.log("Message typed:", message); // Debugging line
        if (message.length == 0) {
            $("#Micbtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        }
        else {
            $("#Micbtn").attr('hidden', true);
            $("#SendBtn").attr('hidden', false);
        }
    }
    // ShowHideButton("hi")
    // key up event handler on text box
    $("#chatbox").keyup(function () {

        let message = $("#chatbox").val();
        ShowHideButton(message)

    });

    // send button event handler
    $("#SendBtn").click(function () {

        let message = $("#chatbox").val()
        PlayAssistant(message)

    });


    // enter press event handler on chat box
    $("#chatbox").keypress(function (e) {
        key = e.which;
        if (key == 13) {
            let message = $("#chatbox").val()
            PlayAssistant(message)
        }
    });




});