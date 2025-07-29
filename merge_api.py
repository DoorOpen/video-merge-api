from flask import Flask, request, send_file
from moviepy.editor import VideoFileClip, concatenate_videoclips, fadein, fadeout
import os

app = Flask(__name__)

@app.route("/merge", methods=["POST"])
def merge():
    files = request.files.getlist("videos")
    os.makedirs("./temp", exist_ok=True)
    clips = []

    for f in files:
        path = f"./temp/{f.filename}"
        f.save(path)
        clip = VideoFileClip(path).fx(fadein, 1).fx(fadeout, 1)
        clips.append(clip)

    final = concatenate_videoclips(clips, method="compose")
    output_path = "./temp/merged.mp4"
    final.write_videofile(output_path, codec="libx264", audio_codec="aac")

    return send_file(output_path, as_attachment=True)
