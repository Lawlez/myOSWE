import tempfile, glob, os
from werkzeug.utils import secure_filename
from application import main
from PIL import Image

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

generate = lambda x: os.urandom(x).hex()

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def petmotion(bee, frames):
    outputFrames = []

    for frame in frames:
        newFrame, i = Image.new('RGBA', frame.size), frames.index(frame)
        width   = int(75*(0.8 + i * 0.02))
        height  = int(75*(0.8 + i * 0.05))
        kaloBee = bee.resize((width, height))
        frame   = frame.convert('RGBA')
        newFrame.paste(kaloBee, mask=kaloBee, box=(30, 37))
        newFrame.paste(frame, mask=frame)
        outputFrames.append(newFrame)
    
    return outputFrames

def save_tmp(file):
    tmp  = tempfile.gettempdir()
    path = os.path.join(tmp, secure_filename(file.filename))
    file.save(path)
    return path

def petpet(file):

    if not allowed_file(file.filename):
        return {'status': 'failed', 'message': 'Improper filename'}, 400

    try:
        
        tmp_path = save_tmp(file)

        bee = Image.open(tmp_path).convert('RGBA')
        frames = [Image.open(f) for f in sorted(glob.glob('application/static/img/*'))]
        finalpet = petmotion(bee, frames)

        filename = f'{generate(14)}.gif'
        finalpet[0].save(
            f'{main.app.config["UPLOAD_FOLDER"]}/{filename}', 
            save_all=True, 
            duration=30, 
            loop=0, 
            append_images=finalpet[1:], 
        )

        os.unlink(tmp_path)

        return {'status': 'success', 'image': f'static/petpets/{filename}'}, 200

    except:
        return {'status': 'failed', 'message': 'Something went wrong'}, 500