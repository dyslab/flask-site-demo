$(document).ready(function() {
    $(".top-menuitem.nav-link:eq(2)").addClass('active');

    // Set active panel and sidebar menu.
    $("#menuList").children().eq($(".activepanel").text()).addClass("active");
    $("#panelList").children().eq($(".activepanel").text()).addClass("active");

    var simplemde = new SimpleMDE({ element: $("#blogcontent")[0] });
});
