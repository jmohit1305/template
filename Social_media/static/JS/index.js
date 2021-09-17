var perfEntries = performance.getEntriesByType("navigation");

if (perfEntries[0].type === "back_forward") {
    window.location.reload();
}
var ec = "";
$(window).on("load", function() {
    $("#welcome > p").css({ "animation-name": "up", "animation-duration": "1s", "animation-fill-mode": "forwards" });
    $("#amigo > p").css({ "animation-name": "up", "animation-duration": "1s", "animation-fill-mode": "forwards", "animation-delay": "0.5s" });

    $("#login-container").fadeIn(2000);
    $("#login-container").css({ "display": "flex" });
    ec = $("#error").text()
    ec = ec.substr(0, 1);
    if (ec == "2") {
        var a = ($("#right").position().left);
        $("#right").css({ left: -a });
        $("#left").css({ left: a });
        $("#swing").text("Login");
        $("#login-container").css({ "display": "none" })
        $("#signup-container").css({ "display": "flex" });




    }





});
$(document).ready(function() {
    var click = 2;

    $("#swing").on("click", function() {
        var a = ($("#right").position().left);

        if (click % 2 === 0) {

            $("#right").animate({ left: -a });
            $("#left").animate({ left: a });
            $("#swing").text("Login");
            $("#login-container").fadeOut(500, function() {
                $("#signup-container").fadeIn(500);
                $("#signup-container").css({ "display": "flex" });
                $("#login-container").css({ "display": "none" });
            });






        } else {
            $("#right").animate({ left: a });
            $("#left").animate({ left: -a });
            $("#swing").text("Signup");

            $("#signup-container").fadeOut(500, function() {
                $("#login-container").fadeIn(500);
                $("#login-container").css({ "display": "flex" });
                $("#sigunup-container").css({ "display": "none" });
            });

        }
        click = click + 1;

    });

});