function makeSameHeightDivs() {
    // This function is used to make same size of Asides and Article
    var center = document.getElementById('article').offsetHeight;
    console.log(center);
    document.getElementById("asideL").style.height = center + "px";
    document.getElementById('asideR').style.height = center + "px";;
    setTimeout(() => { makeSameHeightDivs() }, 500);
    }

function hideAlert() {
    // Close flashed messages
    var flash = document.getElementById("alert");
    if (flash.style.display === "none") {
        flash.style.display = "block";
    } else {
            flash.style.display = "none";
        }
    }

function deleteNote(noteId) {
   // POST information about deleting specific note to server
   // That help to remove this note from DB
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({ noteId: noteId })
        }).then((_res) => {
            window.location.href = "/notes";
            })
    }

function redirectProfile(email){
   // When clicked at Profile button in the chat
   // Redirect user to the target user page.
    console.log(email);
    window.location.href = "/profile/"+email;
    console.log(window.location.href);
    }
