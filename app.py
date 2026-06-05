from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Tu clave de TMDB ya integrada de forma segura
TMDB_API_KEY = "584eb7805dc971aa9403b5dd0f6a90ae" 

@app.route('/buscar_pelicula', methods=['GET'])
def buscar_pelicula():
    nombre_pelicula = request.args.get('nombre')
    if not nombre_pelicula:
        return jsonify({"error": "Falta el nombre de la película"}), 400

    # Conexión directa a la base de datos de TMDB en español
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={nombre_pelicula}&language=es-ES"
    
    try:
        respuesta = requests.get(url).json()
        
        # Si encuentra resultados, tomamos la primera película que coincida
        if respuesta.get('results'):
            datos_peli = respuesta['results'][0]
            
            # Limpiamos los datos para enviárselos de forma ordenada a tu Blogger
            resultado = {
                "titulo": datos_peli.get('title'),
                "sinopsis": datos_peli.get('overview'),
                "anio": datos_peli.get('release_date', '')[:4], # Extrae solo el año de lanzamiento
                "portada": f"https://image.tmdb.org/t/p/w500{datos_peli.get('poster_path')}",
                "puntuacion": datos_peli.get('vote_average')
            }
            return jsonify(resultado)
        else:
            return jsonify({"error": "No se encontró ninguna película"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# ⚠️ PEGA AQUÍ TU LLAVE DE TMDB (La que conseguiste en themoviedb.org)
TMDB_API_KEY = "TU_API_KEY_AQUÍ" 

@app.route('/buscar_pelicula', methods=['GET'])
def buscar_pelicula():
    nombre_pelicula = request.args.get('nombre')
    if not nombre_pelicula:
        return jsonify({"error": "Falta el nombre de la película"}), 400

    # Nos conectamos a la base de datos de TMDB en español
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={nombre_pelicula}&language=es-ES"
    
    try:
        respuesta = requests.get(url).json()
        
        # Si encontró la película, tomamos el primer resultado
        if respuesta.get('results'):
            datos_peli = respuesta['results'][0]
            
            # Construimos la información limpia para Blogger
            resultado = {
                "titulo": datos_peli.get('title'),
                "sinopsis": datos_peli.get('overview'),
                "anio": datos_peli.get('release_date', '')[:4], # Tomamos solo el año
                "portada": f"https://image.tmdb.org/t/p/w500{datos_peli.get('poster_path')}",
                "puntuacion": datos_peli.get('vote_average')
            }
            return jsonify(resultado)
        else:
            return jsonify({"error": "No se encontró ninguna película"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
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
