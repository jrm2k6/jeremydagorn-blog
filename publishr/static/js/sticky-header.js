$(window).load(function() {
    var stickyBarElement = $(".menu");
    var stickyBarTop = stickyBarElement.offset().top;
    var stickyBarOriginalBackground = stickyBarElement.css("background");

    $(window).on("scroll", function(e) {
        var scrollbarTop = $(window).scrollTop();
        var cssProps = {};
        
        if (scrollbarTop > stickyBarTop) {
            cssProps = {
                "position": "fixed",
                "top": "0px",
                "width": "100%",
                "background-color": "rgb(128, 128, 128)"
            };
        } else {
            cssProps = {
                "position" : "static",
                "background": stickyBarOriginalBackground
            };
        }
        stickyBarElement.css(cssProps);
    });
});