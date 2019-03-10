$(document).ready(function() {
    $(".top-menuitem.nav-link:eq(2)").addClass("active");

    // Initialize markdown editor and tags in Search Tab.
    var simplemde = new SimpleMDE({ element: $("#blogcontent")[0] });
    InitTags();
    ChangeActiveTab(parseInt($(".activepanel").text()));

    // Common function: Change Active Tab by id. eg. 0,1,2...
    function ChangeActiveTab(id) {
        $(".list-group-item").eq(id).tab("show")
    }

    // Common function: Set response message
    function SetResponse(jquery, msg) {
        insertHTML = "<div class=\"alert alert-warning alert-dismissible fade show\" role=\"alert\"><strong>" +
            msg + "</strong><button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\">" +
            "<span aria-hidden=\"true\">&times;</span></button></div>";
        jquery.append($(insertHTML).slideDown(500).delay(3000).fadeOut(500));
        setTimeout(function () {
            ChangeActiveTab(0);
        }, 3500);
    }

    // Write Tab: Ajax submit new blog.
    $("#writeform").submit(function(event) {
        event.preventDefault();
        $.post('/blog/new', $("#writeform").serialize()).done(function(data) {
            resObj = JSON.parse(data);
            if (resObj.resCode === 0) {
                SetResponse($("#writetabresponse"), resObj.resMsg);
            } else {
                alert(resObj.resMsg);
            }
        });      
    });

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
