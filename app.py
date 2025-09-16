from flask import Flask, request, render_template, url_for, flash, redirect
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nom = request.form["nom"]
        email = request.form["email"]
        message = request.form["message"]

        corps = f"""
            Nom : {nom}
            Email : {email}
            Message :
            {message}
        """
        msg = MIMEText(corps)
        msg["Subject"] = "Nouveau message de contact - Portfolio"
        msg["From"] = os.getenv("MAIL_USERNAME")
        msg["To"] = os.getenv("MAIL_USERNAME")

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
                smtp.starttls()
                smtp.login(os.getenv("MAIL_USERNAME"), os.getenv("MAIL_PASSWORD"))
                smtp.send_message(msg)
                flash("Message envoyé avec succés !", "success")
        except Exception as e:
            print("Erreur:", e)
            flash("Erreur lors de l'envoi du message.", "error")
        return redirect(url_for("index"))
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
