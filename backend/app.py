from flask import Flask, request , jsonify
from flask_cors import CORS
from main import Resume_scorer
import os
import cv2
import numpy as np
import base64
from vol_crtl import give_posture

upload_folder='uploads'
os.makedirs(upload_folder,exist_ok=True)
app=Flask(__name__)
CORS(app, origins=[
    "http://localhost:3000",
    "https://project-website-frontend.netlify.app"
])
@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method=='POST':
        file=request.files['pdf']
        job=request.form.get('job')
        if file.name=='':
            return {'error': 'No selected file'}, 400
        path=os.path.join(upload_folder,file.name)
        file.save(path)
        r=Resume_scorer(path,job)
        text=r.extract_text_from_pdf()
        analysis = r.parse_analyse()
        score=analysis[:3]
        emails, phones = r.extract_contacts(text)
        os.remove(path)

        return jsonify({
            'extracted_text': text,
            'emails': emails,
            'phones': phones,
            'analysis': analysis[2:],
            'score':score
        })
    
@app.route('/process', methods=['POST'])
def process_image():
    data = request.get_json()
    image_data = data['image'].split(',')[1]  # remove header
    img_bytes = base64.b64decode(image_data)
    nparr = np.frombuffer(img_bytes, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    print(img_np.shape)
    # 🧠 PROCESS THE FRAME HERE (e.g., draw box)
    # cv2.putText(img_np, "Processed", (50, 50),
    #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    # cv2.rectangle(img_np, (60, 60), (260, 180), (255, 0, 0), 2)
    img_np=give_posture(img_np)
    print(img_np.shape)
    # Encode back to base64
    _, buffer = cv2.imencode('.jpg', img_np)
    encoded_img = base64.b64encode(buffer).decode('utf-8')
    encoded_img = "data:image/jpeg;base64," + encoded_img

    return jsonify({ "processed_image": encoded_img })



if __name__ == '__main__':
    app.run(debug=True)
        
        




