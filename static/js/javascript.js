
// Success function when item added to or deleted from user's library.
function alertLibraryResult(result) {
    alert(result);
}

// event listener & handler to delete Piece from UserPiece library.
$(".del_upiece").on("click", function (evt) {

    var pieceId = $(evt.current).data("pieceId");

    console.log(pieceId);

    $.post("/del_upiece",
           pieceId,
           alertLibraryResult);
});