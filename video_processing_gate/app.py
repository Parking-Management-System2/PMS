import os
import cv2
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
image_frames = 'image_frames'

def display_video():
    device = "test_video14.mp4"

    cap = cv2.VideoCapture(device)

    while not cap.isOpened():
        cap = cv2.VideoCapture(device)
        cv2.waitKey(2000)
        print("Waiting for video")

    while True:
        flag, frame = cap.read()
        if flag:
            cv2.imshow("Frame", frame)

        else:
            cv2.destroyAllWindows()
            break

        if cv2.waitKey(1) == 27:
            cv2.destroyAllWindows()
            break

def files():
    # Usuń wszystkie pliki w folderze image_frames, jeśli istnieje
    if os.path.exists(image_frames):
        for file in os.listdir(image_frames):
            file_path = os.path.join(image_frames, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
    else:
        os.makedirs(image_frames)

    src_vid = cv2.VideoCapture('test_video14.mp4')
    return src_vid

def process(src_vid):
    index = 0
    while src_vid.isOpened():
        ret, frame = src_vid.read()
        if not ret:
            break

        name = './image_frames/frame' + str(index) + '.png'

        if index % 100 == 0:
            cv2.imwrite(name, frame)
        index = index + 1
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    src_vid.release()
    cv2.destroyAllWindows()

def get_text():
    for i in os.listdir(image_frames):
        my_example = Image.open(image_frames + "/" + i)
        # W zmiennej tekst przechowywana jest tablica
        text = pytesseract.image_to_string(my_example, lang='eng')
        if i == os.listdir(image_frames)[-1]:
            print(f'Rejestracja: {text}')

# Main driver
if __name__ == '__main__':
    display_video()
    vid = files()
    process(vid)
    get_text()