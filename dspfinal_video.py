import pathlib 
import cv2

cascade_path = pathlib.Path(cv2.__file__).parent.absolute() / "data/haarcascade_frontalface_default.xml"
print(cascade_path)

img = cv2.imread('nerd.jpg')
img_height, img_width, _ = img.shape
# print('image dimensions (HxW):',img_height,"x",img_width)

clf = cv2.CascadeClassifier(str(cascade_path))

camera = cv2.VideoCapture(0)


while True:
    # get_audio()
    _, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = clf.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    for (x , y, width, height) in faces:
        img = cv2.imread('nerd.jpg')
        img = cv2.resize(img, (width,height), interpolation=cv2.INTER_CUBIC)
        frame[ y:y+height , x:x+width ] = img

    cv2.imshow("Face", frame)
    if cv2.waitKey(1) == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
