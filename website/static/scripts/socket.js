var socket;
var user_email;
socket = io();  // Making SocketIO ajax JS server by client side

function getEmail() {
    // Ask and listening to get email of current logged user
    socket.on('get_email', function(email){
//        console.log(email + " get_email");
        user_email = email;
        });
    }

function reciver() {
   // If in "/chat" -> ask about email of loggend user, then get (listen)
   // messages from Server and make "abracadabra" with HTML ;)
   // message is getted as Object, coz it's sended as Py dict.
    if (document.title == "Chat") {
        socket.emit('ask_email');
       // console.log(user_email + " reciver");
        socket.on('recive_message',
            function(news) {
               // listening to news from Server if someone shared post at /chat
               // console.log(news["email"], news["nick"], neaws["data"], news["date"])
   // <li></li>
                var post_content = document.createTextNode(news["data"] + ' ');
                var message = document.createElement("li");
               // console.log(user_email);
                if (news["email"] == user_email){
                    message.classList.add("to_right");}
                else {message.classList.add("to_left");}
                message.appendChild(post_content);
   // <span></span>
                var message_date = document.createTextNode(news["date"]);
                var hover_date = document.createElement("span");
                hover_date.appendChild(message_date);
                hover_date.classList.add("hover_description");
                message.appendChild(hover_date);
   // <button></button>
                var profile_nick = document.createTextNode(news["nick"]);
                var profile_button = document.createElement("button");
                profile_button.classList.add("profile");
                profile_button.setAttribute("onClick",'redirectProfile("'+news["email"]+'")');
                profile_button.appendChild(profile_nick);
                message.appendChild(profile_button);
   // summary commit/ create of page element
                document.getElementById("messages").appendChild(message);
                window.scrollTo(0,document.body.scrollHeight);
               // Scroll to bottom when there is any new message
                }
            );
        }
    }

function sender() {
    // Send message from client to server side if post is not empty
    var post = document.getElementById('message').value;
    if (post.length > 0) {
        socket.emit('client_send_msg', post)
        }
    }

