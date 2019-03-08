$(document).ready(function() {
    $(".top-menuitem.nav-link:eq(1)").addClass("active");
    
    // Init form element: 'custom-file'.
    bsCustomFileInput.init();

    // Validate upload file extension.
    function isValidFileExtension(filename) {
        var validFileExtensionList = ".jpg|.jpeg|.gif|.svg|.png";
        if (validFileExtensionList.search(filename.slice(-4).toLocaleLowerCase()) >= 0) {
            return true;
        } else {
            return false;
        }
    }

    // Empty form file.
    function resetFormFile(fileobj) {
        fileobj.val("");
        $(".custom-file-label").text("JPG/GIF/SVG/PNG accepted");
    }

    // Validate form file when its content changed.
    $("#photo").change(function () {
        var filename = $(this).val();
        if(!isValidFileExtension(filename)) {
            alert('Select IMAGE file please.');
            resetFormFile($("#photo"));
        }
    });

    // Ajax upload file.
    $("#uploadform").submit(function(event) {
        event.preventDefault();

        var formData = new FormData($(this)[0]);
        $.ajax({
            url: "/do/upload",
            type: "POST",
            data: formData,
            async: true, // false,
            cache: false,
            contentType: false,
            processData: false,
        }).done(function( data ) {
            if (data.search("Error") === 0) {
                alert(data);
            } else {
                $("#viewphoto").prop("src", data);
                resetFormFile($("#photo"));
            }
        }).fail(function(err) {
            alert(err);
        });
    });
});
