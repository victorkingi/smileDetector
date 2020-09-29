import cv2

# haarcascade algorithm
video = cv2.VideoCapture('notsmile.mp4')

# pre-trained
classifier_file_face = 'face.xml'
classifier_file_smile = 'smile.xml'
classifier_file_eye = 'eye.xml'

# create car classifier
face_detector = cv2.CascadeClassifier(classifier_file_face)
smile_detector = cv2.CascadeClassifier(classifier_file_smile)
eye_detector = cv2.CascadeClassifier(classifier_file_eye)

# read forever until car stops/ crashes
while True:
    (read_successful, frame) = video.read()

    # Safe coding.
    if read_successful:
        # must convert to gray scale
        grayscaled_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    else:
        break

    # detect smiles
    faces = face_detector.detectMultiScale(grayscaled_frame, scaleFactor=1.1, minNeighbors=7)

    # Draw rectangles around smiles
    for (x, y, w, h) in faces:

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        the_face = frame[y:y+h, x:x+w]

        face_grayscale = cv2.cvtColor(the_face, cv2.COLOR_BGR2GRAY)
        smiles = smile_detector.detectMultiScale(face_grayscale, scaleFactor=1.9, minNeighbors=50)
        eyes = eye_detector.detectMultiScale(face_grayscale, scaleFactor=1.5, minNeighbors=20)

        for (_x, _y, _w, _h) in eyes:
            cv2.rectangle(the_face, (_x, _y), (_x + _w, _y + _h), (255, 255, 255), 4)

        if len(smiles) > 0:
            cv2.putText(frame, 'smiling', (x, y+h+40), fontScale=3,
                        fontFace=cv2.FONT_HERSHEY_PLAIN, color=(255, 255, 255))

    # display image
    cv2.imshow('smile detector', frame)

    # don't auto-close
    key = cv2.waitKey(1)

    if key == 81 or key == 113:
        break

# clean up
video.release()
cv2.destroyAllWindows()
