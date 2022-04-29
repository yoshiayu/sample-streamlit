import streamlit as st
import io
import requests
import json
from PIL import Image
from PIL import ImageDraw, ImageFont

st.title('顔認識アプリ')


SUBSCRIPTION_KEY = '7382d82ba05b473b9ae5800910b8fdb2'

assert SUBSCRIPTION_KEY
face_api_url = 'https://yoshiayu.cognitiveservices.azure.com/face/v1.0/detect'


def get_draw_text(faceDictionary):
    rect = faceDictionary.face_rectangle
    age = int(faceDictionary.face_attributes.age)
    gender = faceDictionary.face_attributes.gender
    text = f'{gender} {age}'

    # 枠に合わせてフォントサイズを調整
    font_size = max(50, int(rect.width / len(text)))
    font = ImageFont.truetype(r'C:\windows\fonts\meiryo.ttc', font_size)

    return (text, font)


def get_text_rectangle(faceDictionary, text, font):
    rect = faceDictionary.face_rectangle

    text_width, text_height = font.getsize(text)
    left = rect.left + rect.width / 2 - text_width / 2
    top = rect.top - text_height - 1

    return (left, top)


def draw_text(faceDictionary):
    text, font = get_draw_text(faceDictionary)
    text_rect = get_text_rectangle(faceDictionary, text, font)
    draw.text(text_rect, text, align='center', font=font, fill='green')


upload_file = st.file_uploader("Choose an image...", type="jpg")
if upload_file is not None:
    img = Image.open(upload_file)
    with io.BytesIO() as output:
        img.save(output, format="JPEG")
        binary_img = output.getvalue()

# with open('sample01.jpg', 'rb') as f:
#    binary_img = f.read()

    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY
    }
    params = {
        'returnFaceId': 'true',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
    }

    res = requests.post(face_api_url, params=params,
                        headers=headers, data=binary_img)
    results = res.json()
    for result in results:
        rect = result['faceRectangle']
        age = result['faceAttributes']['age']
        gender = result['faceAttributes']['gender']
        text = f'{gender} {age}'
        draw = ImageDraw.Draw(img)

        src = r"pillow_test_src.jpg"
        dest = r"pillow_test_dest.jpg"

        draw.rectangle([(rect['left'], rect['top']), (rect['left']+rect['width'],
                                                      rect['top'] + rect['height'])], fill=None, outline='green', width=5)
        draw_x = rect['left']-30
        draw_y = rect['top']-30

        text = result['faceAttributes']['gender'] + \
            '/'+str(result['faceAttributes']['age'])
        draw.text((draw_x, draw_y), text, fill='red')
    st.image(img, caption='Uploaded Image.', use_column_width=True)


print(json.dumps)


# st.write('データフレーム')
# st.write(
#    pd.DataFrame({
#        '1st column': [1, 2, 3, 4],
#        '2nd column': [10, 20, 30, 40]
#    })
# )


# """
# My 1st App
# """

# 20行3列作成
# if st.checkbox('Show DataFrame'):
#    chart_df = pd.DataFrame(
#        np.random.randn(20, 3),
#        columns=['a', 'b', 'c']
#    )
#    st.line_chart(chart_df)
