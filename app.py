from flask import Flask, request, jsonify, render_template, send_from_directory
from deepface import DeepFace
import os

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["UPLOAD_FOLDER"] = "assets"

# Buat folder assets kalau belum ada
if not os.path.exists("assets"):
    os.makedirs("assets")

@app.route("/")
def home():
    profiles = os.listdir("assets")
    return render_template("index.html", profiles=profiles)

@app.route("/upload_profile", methods=["POST"])
def upload_profile():
    file = request.files.get("image")
    user_id = request.form.get("user_id")

    if not file or not user_id:
        return jsonify({"error": "image and user_id are required"}), 400

    file_path = f"assets/{user_id}.jpg"
    file.save(file_path)

    return jsonify({"message": "Profile uploaded", "path": file_path})

@app.route("/verify", methods=["POST"])
def verify_face():
    file = request.files.get("image")
    user_id = request.form.get("user_id")

    if not file or not user_id:
        return jsonify({"error": "image and user_id required"}), 400

    temp_path = "temp.jpg"
    file.save(temp_path)

    profile_path = f"assets/{user_id}.jpg"

    if not os.path.exists(profile_path):
        return jsonify({"error": "Profile not found"}), 404

    try:
        result = DeepFace.verify(
            img1_path=temp_path,
            img2_path=profile_path,
            model_name="Facenet"
        )

        return jsonify({
            "match": result["verified"],
            "distance": result["distance"]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/assets/<path:filename>")
def serve_profile(filename):
    return send_from_directory("assets", filename)

if __name__ == "__main__":
    print("Server started on http://0.0.0.0:5500")
    app.run(host="0.0.0.0", port=5500)
