import requests 
import json 

body = {
    'text' : """
       What is a Convolution Neural Network? 
       A convolutional neural network (CNN) is a type of artificial intelligence that's really good at recognizing patterns, 
       like in photos or videos. Imagine it like a super-smart detective that can quickly spot and understand different details in an image. 
       It does this by looking at small pieces of the image at a time and learning what each piece means, which helps it recognize things like faces, objects, or even handwritten notes.
"""
}

prediction = requests.post(url='http://127.0.0.1:8000/detect', json=body)

print(prediction.json())