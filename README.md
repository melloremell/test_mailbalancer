MailBalancer is and Flask based API that balancing email sending via two email service MailGun and SendGrid. By default the email will be sent using MailGun, if the sending is failed then it will automatically send the email via SendGrid. 

#PARAMETER

MailBalancer is HTTP POST API that is based on JSON input. Below are the parameters to use this API

{
	"to"       :"Email of the receiving party (COMPULSORY)",
	"to_name"  :"Name of the receiving party (OPTIONAL, default: Sender)",
	"from"     :"Email of the sending party (COMPULSORY)",
	"from_name":"Name of the sending party (OPTIONAL, default: Receiver)",
	"subject"  :"title of the email (OPTIONAL, default: No Subject)",
	"body"     :"content of the email in HTML format (COMPULSORY)",
	"setdown"  :"email service to be disabled. MAILGUN or SENDGRID (OPTIONAL, default: default)"
}


#EXAMPLE

Here is an example to use this API using Postman. Body:raw, JSON(application/json). POST "http:0.0.0.0:5000/email"

{
	"to"       :"muzztestmuzz@gmail.com",
	"to_name"  :"Mr Muzz",
	"from"     :"muzzammil@moverobotic.com",
	"from_name":"Mr M",
	"subject"  :"This is a test email",
	"body"     :"<h1>Hi all</h1><p>I am here to test email</p>",
	"setdown"  :"default"
}

#RESPONSE

There are few response you will get after running the API. The response are in JSON and are as follows:

1) {"status": true, "response": "Email Sent with SendGrid"}                   : Email successfully sent and it is sent using SendGrid email service
2) {"status": true, "response": "Email Sent with MailGun"}                    : Email successfully sent and it is sent using MailGun email service
3) {"status": false,"response": "Target email is compulsory"}                 : Email sending failed sent because the target email is not given or not in correct format
3) {"status": false,"response": "Sender email is compulsory"}                 : Email sending failed sent because the sender email is not given or not in correct format
4) {"status": false,"response": "Email body is compulsory"}                   : Email sending failed sent because the email content in body is not given or empty
4) {"status": false,"response": "Email Sent via MailGun or SendGrid Failed"}  : Email sending failed sent because target email is not active or both MailGun and SendGrid service is down

#DEPLOYMENT

MailBalancer is a in Docker container. You can pull docker at: "docker run -p 5000:5000 melloremell/mailbalancer"
You can build it with : "docker build --rm -t melloremell/mailbalancer:latest ."
You can run it with : "docker run -p 5000:5000 melloremell/mailbalancer"
You can change 5000 to any port you desire and make sure the port is not blocked

#ENDPOINT

Once you run the conntainer, the endpoint the POST API will be: "IPADDRESS:5000/email". 
The IPADDRESS is the IP address of the computer running the container.
Example: "http:192.168.13.23:5000/email"

#RESTRICTION

As this API is running from a demo account of SendGrid and MailGun. The target and sending email is restricted.
You can only sending the email to muzztestmuzz@gmail.com and the sender must be muzzammil@moverobotic.com
You can check the API successfully sent to muzztestmuzz@gmail.com by login on into the email account with password:"muzztestmuzz2021"
You can send to any email you like if you are using SendGrid, however the sender must be muzzammil@moverobotic.com. To force sending
via SendGrid. You must set MailGun to down. This is the example to force sending using SendGrid to any of desire target email.

{
	"to"       :"any@email.com",
	"to_name"  :"Anybody",
	"from"     :"muzzammil@moverobotic.com",
	"from_name":"Mr M",
	"subject"  :"This is a test email",
	"body"     :"<h1>Hi all</h1><p>I am here to test email</p>",
	"setdown"  :"MAILGUN"
}

#SOURCE

The source code is at: "https://github.com/melloremell/test_mailbalancer"
Feel free to use it with your own MailGun and SendGrid Key