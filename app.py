from flask import Flask, request, render_template, jsonify, send_file
import time
import os
from mytiktok.video import Video



app = Flask(__name__)

@app.route('/')
def index():
      	
    return render_template('index.html')


@app.route('/info', methods=['POST'])
def info():
    url = request.form.get('url')
    if url:
        try:
        
            # initialize video class  
            global video
            video = Video(url=url)
            file_name = f'{video._info.get("embed_product_id")}.mp4'
            thumbnail_url = video._info.get('thumbnail_url')
            title = video._info.get('title')
            author = video._info.get('author_name')

            response = {'success': True, 'message': 'info received successfully', 'file_name':file_name, 'thumpnail_url':thumbnail_url, 'title':title, 'author':author}
        except Exception as e:
            response = {'success':False, 'message':'Url Invalid'}

    return jsonify(response)

@app.route('/download', methods=['GET'])
def download():
    try:
        # remove videos if they are any
        # remove_videos()
        file_name = f'{video._info.get("embed_product_id")}.mp4'
        video.download(video_path(file_name))

        # send response that video was downloaded successfully
        response = {'success': True, 'message': 'downloaded successfully'}
    except Exception as e:
        print(e)
        response = {'success':False, 'message': 'Failed'}
    
    return jsonify(response)
        

@app.route("/videos/<file_name>", methods = ["GET"])
def file(file_name):
    file_path = video_path(file_name)

    if os.path.exists(file_path):
       
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({'success': False, 'message': 'File not found'})
    
def remove_videos(directory = 'videos'):
    "remove each file in a directory"
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file, )
        os.remove(file_path)

def video_path(file_name):
    return os.path.join('videos', file_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
