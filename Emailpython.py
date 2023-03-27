import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Define sender and recipient email addresses
sender = "camperdhaouadi@gmail.com"
recipient = "chiheb.dhaouadi@istic.ucar.tn"

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "Your subject"
msg['From'] = sender
msg['To'] = recipient

# Create the HTML message content
html = """
<html>
  <head>
    <style>
      /* Define your CSS styles here */
      h1 {
        color: #0099cc;
        font-size: 30px;
      }
      p {
        color: #444444;
        font-size: 16px;
      }
    </style>
  </head>
  <body>
    <h1>Your heading here</h1>
    <p>Your message content here</p>
    <img src="image.jpg" alt="image">
  </body>
</html>
"""

# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(html, 'html')

# Attach parts into message container.
msg.attach(part1)


# Send the message via SMTP server.
s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login(sender, 'mnvlnpvwxoaqegzw') # Replace 'password' with your actual password
s.sendmail(sender, recipient, msg.as_string())
s.quit()
