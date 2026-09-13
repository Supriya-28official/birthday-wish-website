from flask import Flask, render_template, request
import os, uuid

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def home():
    data = {
        "name": "A Special Person",
        "event": "Birthday",
        "message": "Wishing you a day filled with happiness, smiles and beautiful memories! 💖",
        "moments": "Every moment with you is a beautiful memory. ✨",
        "photos": [],
        "music": ""
    }

    if request.method == "POST":
        data["name"] = request.form.get("name") or data["name"]
        data["event"] = request.form.get("event") or "Birthday"
        data["message"] = request.form.get("message") or data["message"]
        data["moments"] = request.form.get("moments") or data["moments"]

        music = request.files.get("music")
        if music and music.filename:
            ext = os.path.splitext(music.filename)[1].lower()
            filename = f"{uuid.uuid4().hex}{ext}"
            music.save(os.path.join(UPLOAD_FOLDER, filename))
            data["music"] = "/" + os.path.join(UPLOAD_FOLDER, filename).replace("\\", "/")

        for photo in request.files.getlist("photos"):
            if photo and photo.filename:
                ext = os.path.splitext(photo.filename)[1].lower()
                filename = f"{uuid.uuid4().hex}{ext}"
                photo.save(os.path.join(UPLOAD_FOLDER, filename))
                data["photos"].append("/" + os.path.join(UPLOAD_FOLDER, filename).replace("\\", "/"))

    return render_template("index.html", **data)

if __name__ == "__main__":
    app.run(debug=True)
