from flask import Flask, request, jsonify, render_template, send_from_directory
from deepface import DeepFace
import os
import tempfile

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["UPLOAD_FOLDER"] = "assets"

if not os.path.exists("assets"):
    os.makedirs("assets")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/v1/verify", methods=["POST"])
def verify_face():
    source_image = request.files.get("source_image") # gambar yang akan divalidasi
    target_image = request.files.get("target_image") # gambar referensi

    if not source_image or not target_image:
        return jsonify({"error": "source_image & target_image harus dikirim"}), 400

    source_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    target_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")

    source_image.save(source_tmp.name)
    target_image.save(target_tmp.name)

    try:
        result = DeepFace.verify(
            img1_path=source_tmp.name,
            img2_path=target_tmp.name,
            model_name="Facenet"
        )

        os.unlink(source_tmp.name)
        os.unlink(target_tmp.name)

        return jsonify({
            "match": result["verified"],
            "distance": result["distance"]
        })

    except Exception as e:
        if os.path.exists(source_tmp.name): os.unlink(source_tmp.name)
        if os.path.exists(target_tmp.name): os.unlink(target_tmp.name)

        return jsonify({"error": str(e)}), 500

@app.route("/assets/<path:filename>")
def serve_profile(filename):
    return send_from_directory("assets", filename)

if __name__ == "__main__":
    print("Server started on http://0.0.0.0:5500")
    app.run(host="0.0.0.0", port=5500)
