import streamlit as st
import io
import requests
from PIL import Image
from PIL import ImageDraw

st.title('顔認識アプリ')

subscription_key = "658a4bb366d048ecad727d04b6a808e8"
assert subscription_key

face_api_url = 'https://20211130tomoaki.cognitiveservices.azure.com/face/v1.0/detect'
headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key
}
params = {
    'returnFaceId': 'true',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
}


upload_file = st.file_uploader("Choose an image...", type='jpg')

if upload_file is not None:
    img = Image.open(upload_file)

    with io.BytesIO() as output:
        img.save(output,format="JPEG")
        binary_img = output.getvalue()


    res = requests.post(face_api_url, params=params, headers=headers,data=binary_img)
    results = res.json()

    for result in results:
        rect = result['faceRectangle']
        draw = ImageDraw.Draw(img)
        draw.rectangle([(rect['left'],rect['top']),(rect['left']+rect['width'], rect['top']+rect['height'])], fill=None, outline='red', width=2)

    st.image(img, caption='Uploaded image', use_column_width=True)
