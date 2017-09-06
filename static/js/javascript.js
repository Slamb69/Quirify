"use strict";

// Success function when item added to or deleted from user's library.
function alertLibraryResult(result, pieceid) {
    var addSelectorString = "#add-"+pieceid;
    var delSelectorString = "#del-"+pieceid;
    var addButton = $(addSelectorString);
    var delButton = $(delSelectorString);
    if (addButton.prop("hidden")){
      addButton.prop("hidden", false);
    }else{
      addButton.prop("hidden", true);
    }

    if (delButton.prop("hidden")){
      delButton.prop("hidden", false);

    }else{
      delButton.prop("hidden", true);
      
    }

    alert(result.message);

}


// event listener & handler to delete Piece from UserPiece library.
$(".del_upiece").on("click", function (evt) {
    var formInput = {"piece_id": $(evt.currentTarget).data("pieceid")};

    console.log(evt.currentTarget);
    console.log(formInput);

    $.post("/del_upiece.json",
           formInput,
           function(evt) {
           alertLibraryResult(evt, formInput.piece_id);
           });
});

// event listener & handler to add Piece to UserPiece library.
$(".add_upiece").on("click", function (evt) {

    var formInput = {"piece_id": $(evt.currentTarget).data("pieceid")};

    // console.log(evt.currentTarget);
    // console.log(formInput);

    $.post("/add_upiece.json",
           formInput,
           function(evt) {
           alertLibraryResult(evt, formInput.piece_id);
           });
});


// event listener & handler to delete Sheet from UserSheet library.
$(".del_usheet").on("click", function (evt) {
    var formInput = {"sheet_id": $(evt.currentTarget).data("sheetid")};

    console.log(evt.currentTarget);
    console.log(formInput);

    $.post("/del_usheet.json",
           formInput,
           function(evt) {
           alertLibraryResult(evt, formInput.sheet_id);
           });
});

// event listener & handler to add Sheet to UserSheet library.
$(".add_usheet").on("click", function (evt) {

    var formInput = {"sheet_id": $(evt.currentTarget).data("sheetid")};

    // console.log(evt.currentTarget);
    // console.log(formInput);

    $.post("/add_usheet.json",
           formInput,
           function(evt) {
           alertLibraryResult(evt, formInput.sheet_id);
           });
});

// event listener & handler to delete audiofile from UserAudioFile library.
$(".del_ufile").on("click", function (evt) {
    var formInput = {"file_id": $(evt.currentTarget).data("fileid")};

    console.log(evt.currentTarget);
    console.log(formInput);

    $.post("/del_uaudiofile.json",
           formInput,
           function(evt) {
           alertLibraryResult(evt, formInput.file_id);
           });
});

// event listener & handler to add file to UserAudioFile library.
$(".add_ufile").on("click", function (evt) {
    
    console.log(evt.currentTarget);
    console.log(formInput);
    
    var formInput = {"file_id": $(evt.currentTarget).data("fileid")};

    // console.log(evt.currentTarget);
    // console.log(formInput);

    $.post("/add_uaudiofile.json",
           formInput,
           function(evt) {
           alertLibraryResult(evt, formInput.file_id);
           });
});