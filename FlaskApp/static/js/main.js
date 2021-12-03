var aliveSecond = 0;
var heartbeatRate = 5000;

var myChannel = "kierans-pi-channel"

function keepAlive()
{
	var request = new XMLHttpRequest();
	request.onreadystatechange = function(){
		if(this.readyState === 4){
			if(this.status === 200){

				if(this.responseText !== null){
					var date = new Date();
					aliveSecond = date.getTime();
					var keepAliveData = this.responseText;
					//convert string to JSON
					var json_data = this.responseText;
					var json_obj = JSON.parse(json_data);
					if(json_obj.motion == 1){
						document.getElementById("Motion_id").innerHTML = "Yes";
					}
					else{
						document.getElementById("Motion_id").innerHTML ="No";
					}
					console.log(keepAliveData);
				}
			}
		}
	};
	request.open("GET", "keep_alive", true);
	request.send(null);
	setTimeout('keepAlive()', heartbeatRate);
}

function time()
{
	var d = new Date();
	var currentSec = d.getTime();
	if(currentSec - aliveSecond > heartbeatRate + 1000)
	{
		document.getElementById("Connection_id").innerHTML = "DEAD";
	}
	else
	{
		document.getElementById("Connection_id").innerHTML = "ALIVE";
	}
	setTimeout('time()', 1000);
}

pubnub = new PubNub({
            publishKey : "pub-c-e967d84c-d953-4871-8593-f3004be3650c",
            subscribeKey : "sub-c-8ce5e2e8-3bc5-11ec-b2c1-a25c7fcd9558",
            uuid: "0842c6b2-970f-4882-99e7-c7baeb98c3f7"
        })

pubnub.addListener({
        status: function(statusEvent) {
            if (statusEvent.category === "PNConnectedCategory") {
                console.log("Successfully connected to Pubnub")
                publishSampleMessage();
            }
        },
        message: function(msg) {
            console.log(msg.message.title);
            console.log(msg.message.description);
        },
        presence: function(presenceEvent) {
            // This is where you handle presence. Not important for now :)
        }
    })

function publishSampleMessage() {
        console.log("Publish to a channel 'hello_world'");

        // With the right payload, you can publish a message, add a reaction to a message,
        // send a push notification, or send a small payload called a signal.
        var publishPayload = {
            channel : "hello_world",
            message: {
                title: "greeting",
                description: "This is my first message!"
            }
        }
        pubnub.publish(publishPayload, function(status, response) {
            console.log(status, response);
        })
}

function handleClick(cb)
{
	if(cb.checked)
	{
		value = "ON";
	}
	else
	{
		value = "OFF";
	}
	var ckbStatus = new Object();
	ckbStatus[cb.id] = value;
	var event = new Object();
	event.event = ckbStatus;
	publishUpdate(event, myChannel);
}

pubnub.subscribe({channels: [myChannel]})

function publishUpdate(data, channel)
{
    pubnub.publish({
        channel : channel,
        message : data
        },
        function(status, response)
        {
            if(status.error){
                console.log(status);
            }
            else
            {
                console.log("Message published with timetoken", response.timetoken);
            }
        });
}
	
function logout()
{
    console.log("Logging out and unsubscribing from the channel");
    pubnub.unsubscribe({
        channels : [myChannel]
    })
    location.replace("/logout");
}

function facebookLogin()
{
    location.replace("/facebook_login");
}

// add new functions to access admin endpoints through buttons

function roomDetails()
{
    location.replace("/house_room/1234567");
}

function userDetails()
{
    location.replace("/login");
}

function oilLevelDetails()
{
    location.replace("/oil_level_current/1234567");
}

// show different info based on user clicks
function displayUserDetails(){
//    console.log("User Clicked")
    // set div inner html to be certain text
    document.getElementById("content").innerHTML = "User Details<br><h2>Please install our mobile based app in order to access our app functionality</h2>";
    var element = document.getElementById("user");
    element.classList.toggle("active");
    var element = document.getElementById("admin");
    element.classList.remove("active");
}

function displayAdminDetails(){
//    console.log("Admin Clicked")
    // set div inner html to be certain text
    document.getElementById("content").innerHTML = "Admin Login<br><br><label for \"username\"><b>Username<b></label><br><input type=\"text\" placeholder=\"Enter Username\" name=\"username\" id=\"username\" required><br><br><label for=\"password\"><b>Password</b></label><br><input type=\"password\" placeholder=\"Enter Password\" name=\"password\" id=\"password\" required><br><br><button onclick=\"adminLogin()\" type=\"submit\">Login</button>";
    var element = document.getElementById("admin");
    element.classList.toggle("active");
    var element = document.getElementById("user");
    element.classList.remove("active");
}

function adminLogin(){
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    if ( username == "admin" && password == "adminPassword"){
        // alert ("Login successfully");
        document.getElementById("content").innerHTML = "Login successfully<br><br><button onclick=\"userDetails()\">Check User Login</button><br><br><button onclick=\"oilLevelDetails()\">Oil Level</button><br><br><button onclick=\"roomDetails()\">Room Details</button>";
    } else {
        alert("Incorrect credentials! Try Again!");
    }
}