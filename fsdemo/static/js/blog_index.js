$(document).ready(function() {
    $(".top-menuitem.nav-link:eq(2)").addClass("active");

    // Set active panel and sidebar menu.
    $("#menuList").children().eq($(".activepanel").text()).addClass("active");
    $("#panelList").children().eq($(".activepanel").text()).addClass("active");

    // Initialize markdown editor and tags in Search Tab.
    var simplemde = new SimpleMDE({ element: $("#blogcontent")[0] });
    InitTags();

    // Search Tab: Initialize tags.
    function InitTags() {
        $("#taglist").children(".custom-option-tag").each(function() {
            if ($(this).val() !== "") {
                $(".custom-blog-search-tag-container").append($("<li class=\"list-inline-item custom-blog-search-tag\">" +
                    "<span class=\"badge badge-pill badge-warning\">" +
                    $(this).val() + " &times;</span></li>")); 
            }
        });
    }

    // Search Tab: Remove tag.
    $(".custom-blog-search-tag-container").on("click", ".custom-blog-search-tag", function() {
        $(this).remove();
    });

    // Search Tab: Reset options.
    $("#reset").click(function() {
        $("#searchterms").val("");
        $(".custom-blog-search-tag-container").children(".custom-blog-search-tag").remove();
        InitTags();
    });
});
