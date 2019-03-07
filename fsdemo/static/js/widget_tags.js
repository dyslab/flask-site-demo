$(document).ready(function() {
    //  Is the tag existed?
    //  Parameter:
    //      jquery: jQuery object string.
    //      prop: the property of the object for comparison.
    //      val: the value for comparison.
    //  Return value: 
    //      Boolean: TRUE or FALSE
    function isTagExists(jquery, prop, val) {
        var rflag = false;
        $(jquery).each(function() {
            if (prop === "text") {
                if ($(this).text() === val) rflag = !rflag;
            } else if (prop === "value") {
                if ($(this).val() === val) rflag = !rflag;
            }
        });
        return rflag;
    }

    // Remove tag
    $(".custom-tag-container").on("click", ".custom-tag", function() {
        $(this).remove();
    })

    // Add tag
    $("#addtag").click(function() {
        if($("#taglist").val() !== "") {
            if(!isTagExists("input#tags", "value", $("#taglist").val())) {
                inserttag = "<input type=\"hidden\" name=\"tags\" id=\"tags\" value=\"" + $("#taglist").val() + "\">";
                inserthtml = "<li class=\"list-inline-item custom-tag\">" +
                    "<span class=\"badge badge-primary\">" +
                    "<span class=\"h6\">" +
                    $("#taglist").val() +
                    " &times;</span>" +
                    "</span></li>";
                $(inserttag).appendTo($(inserthtml).appendTo(".custom-tag-container"));
            } else {
                $("input#tags").filter(function(index) {
                    return $(this).val() === $("#taglist").val();
                }).parent().fadeOut().fadeIn();
            }
        }
        else {
            alert("Select tag first please.");
        }
    });

    // Manage Tags: Initialize tag list
    $("#mt-tags").click(function() {
        $(".custom-mt-tag-container").children().remove();
        $("#taglist").children().each(function() {
            if ($(this).val() !== "") {
                $(".custom-mt-tag-container").append($("<div class=\"form-row custom-mt-tag-row mt-1 mb-1\">" +
                "<div class=\"col-11 custom-mt-tag-name\">" +
                $(this).val() + "</div><div class=\"col-1\" title=\"Remove Tag\">" +
                "<button type=\"button\" class=\"btn btn-sm btn-danger custom-mt-tag-remove\"><strong>&minus;</strong></button>" +
                "</div>")); 
            }
        });
        $("#tagsMangementModal").modal('show');
    });

    // Manage Tags: Remove tag
    $(".custom-mt-tag-container").on("click", ".custom-mt-tag-remove", function() {
        $(this).parent().parent().remove();
    });

    // Manage Tags: Add tag
    $("#mt-addtag").click(function() {
        $("#mt-addtag-text").val(String.trim($("#mt-addtag-text").val()));
        if($("#mt-addtag-text").val() !== "") {
            if(!isTagExists("div.custom-mt-tag-name", "text", $("#mt-addtag-text").val())) {
                inserthtml = "<div class=\"form-row custom-mt-tag-row mt-1 mb-1\">" +
                    "<div class=\"col-11 custom-mt-tag-name\">" + $("#mt-addtag-text").val() + "</div>" +
                    "<div class=\"col-1\" title=\"Remove Tag\">" +
                    "<button type=\"button\" class=\"btn btn-sm btn-danger custom-mt-tag-remove\"><strong>&minus;</strong></button>" +
                    "</div></div>";
                $(inserthtml).appendTo(".custom-mt-tag-container");
            } else {
                $("div.custom-mt-tag-name").filter(function(index) {
                    return $(this).text() === $("#mt-addtag-text").val();
                }).fadeOut().fadeIn();
            }
        } else {
            alert("Tag name cannot be empty.");
        }
    });

    // Manage Tags: Save changes
    $(".mt-save").click(function() {
        // Ajax call to save tags on server side.
        // ...

        // Synchronize changes for '#taglist'
        $("#taglist").children().remove();
        $("#taglist").append($("<option value=\"\" selected>Select Tag</option>"));
        $("div.custom-mt-tag-name").each(function() {
            $("#taglist").append($("<option value=\"" + $(this).text() + "\">" +
                $(this).text() + "</option>")); 
        });
        $("#tagsMangementModal").modal('toggle');
    });
});
