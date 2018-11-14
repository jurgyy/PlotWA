$(window).on('load', function() {
    $(".accordion").on("click", ".accordion-header", function() {
        $(this).toggleClass("active").next().slideToggle();
    });

    $(".howToLink").on("click", "a[id=howToLink]", function(event) {
        if (this.hash !== "") {
            event.preventDefault();
            var hash = this.hash;

            $('html, body').animate({
                scrollTop: $(hash).offset().top
            }, 500, function(){

                window.location.hash = hash;
            });

            var dst = $("#howTo").parent();
            if (!dst.hasClass("active")) {
                dst.toggleClass("active").next().slideToggle();
            }
        }
    });

    $("[type=file]").on("change", function(){
        // Name of file and placeholder
        var file = this.files[0].name;
        var dflt = $(this).attr("placeholder");

        if($(this).val() != ""){
            $(this).next().text(file);
        } else {
            $(this).next().text(dflt);
        }
    });

    $(".customize-nav li.nav-item").on("click", function(event) {
        $(this).parent().find("li.nav-item").toggleClass("active", false);
        $(this).toggleClass("active");
    });
});