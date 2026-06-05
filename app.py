from flask import Flask, request, send_file
from flask_cors import CORS
import yt_dlp
import os
import io

app = Flask(__name__)
CORS(app)  # Permite que Blogger se comunique con este servidor

@app.route('/descargar', methods=['GET'])
def descargar_video():
    video_url = request.args.get('url')
    
    if not video_url:
        return {"error": "Falta la URL del video"}, 400
        
    ydl_opts = {
        'format': 'best',  # Descarga la mejor calidad de video y audio juntos
        'outtmpl': '-',    # Envía el video directo a la memoria para no llenar el disco
        'logtostderr': True
    }
    
    try:
        buffer = io.BytesIO()
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            
        return send_file(
            buffer,
            mimetype='video/mp4',
            as_attachment=True,
            download_name='video.mp4'
        )
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
