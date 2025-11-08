from quart import Quart, request, render_template, jsonify, send_file, session, Response
from httpx import AsyncClient 
from TikTokApi import TikTokApi
import os
import aiofiles


#TiktokApi 
async def metadata_by_url(url: str) -> tuple[str, str, str]:
    tik_request = 'https://www.tiktok.com/oembed?url=' + url

    async with AsyncClient() as client:
        tik_response = await client.get(tik_request)
    info = tik_response.json()
    return info.get('embed_product_id'), info.get('thumbnail_url'), info.get('title'), info.get('author_name'), url

async def download_video_by_url(url: str, output_path: str | None = None) -> None: 
    async with TikTokApi() as api: 
        # ✅ Create browser sessions
        await api.create_sessions(num_sessions=1, headless=True, sleep_after=3)

        # ✅ Get the video object
        video =  api.video(url=url)
        
        # ✅ Call to ensure video is fetched
        await video.info()

        # ✅ Then request the video bytes
        data = await video.bytes()

        if data and output_path:
            async with aiofiles.open(output_path, "wb") as f:
                await f.write(data)

        print(f"✅ Downloaded {output_path}")    
    

#Helpers
def remove_videos(file_name = str) -> None:
    "remove file in a directory"
    file_path = video_path(file_name)
    os.remove(file_path)
    print(f"✅ Deleted {file_path}")


def video_path(file_name: str):
    return os.path.join('videos', file_name)



#Quart App
app = Quart(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
async def index():
    return await render_template('index.html')


@app.route('/info', methods=['POST'])
async def info():
    form = await request.form
    url = form.get('url')
    try:
            session['video'] = await metadata_by_url(url)
            session['file_name'], session['thumbnail_url'], session['title'], session['author'], *_ = session['video']
            session['file_name'] += '.mp4'
            
            response = {
                'success': True,
                'message': 'info received successfully',
                'file_name': session['file_name'],
                'thumbnail_url': session['thumbnail_url'],
                'title': session['title'],
                'author': session['author']
            }
    except Exception as e:
            print(e)
            response = {'success': False, 'message': 'Url Invalid'}

    return jsonify(response)


@app.route('/download', methods=['GET'])
async def download():
    try:
        url = session['video'][-1]
        output_path = video_path(session['file_name'])

        await download_video_by_url(url=url, output_path=output_path)

        response = {'success': True, 'message': 'downloaded successfully'}
    except Exception as e:
        print(e)
        response = {'success': False, 'message': 'Download Failed'}

    return jsonify(response)


@app.route("/videos/<file_name>", methods=["GET"])
async def file(file_name):
    file_path = video_path(file_name)
    if not os.path.exists(file_path):
        return jsonify({'success': False, 'message': 'file not found'})
    
    #Get total size in bytes
    total_size = os.path.getsize(file_path)
    
    # # stream freshly downloaded file in chuncks
    async def generate():
        async with aiofiles.open(file_path, "rb") as f:
            while chunk := await f.read(4096):
                yield chunk
        # Delete after streaming
        remove_videos(file_name)

    # Return streaming response with proper content type and attachment header
    headers = {
        "Content-Disposition": f'attachment; filename="{file_name}"',  "Content-Length": str(total_size)
    }
    return Response(generate(), headers=headers, mimetype="application/octet-stream")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
