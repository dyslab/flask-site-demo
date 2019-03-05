$(document).ready(function() {
    $(".top-menuitem.nav-link:eq(1)").addClass('active');

    // Remove tag
    $(".custom-tag-container").on("click", ".custom-tag", function() {
        $(this).remove();
    })

    // Add tag
    $("#addtag").click(function() {
        if($("#taglist").val() !== "") {
            if(!isTagExists($("#taglist").val())) {
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

    // Is the tag existed?
    // Return value: true or false
    function isTagExists(val) {
        var rflag = false;
        $("input#tags").each(function() {
            if ($(this).val() === val) rflag = !rflag;
        });
        return rflag;
    }
});
