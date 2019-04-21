import face_recognition
import numpy as np
import matplotlib.pyplot as plt

def get_faces(filename, show=False):
    image = face_recognition.load_image_file(filename)
    faces = face_recognition.face_locations(image)
    encodings = []
    for f in faces:
        sub_image = image[f[0] : f[2], f[3] : f[1]]
        encoding = face_recognition.face_encodings(sub_image)
        if len(encoding) == 1:
            encodings += encoding
        else:
            encodings.append(np.array([0] * len(encodings[-1])))
    if show:
        plt.figure(figsize=(12, 8))
        plt.imshow(image)
        for f in faces:
            plt.plot([f[1], f[1], f[3], f[3], f[1]], [f[0], f[2], f[2], f[0], f[0]])
        plt.show()
    return faces, encodings


def get_stat(photo_before, photo_after, tolerance=0.5, debug=False):
    faces_before, encodings_before = get_faces(photo_before, show=True)
    faces_after, encodings_after = get_faces(photo_after, show=True)
    before_count = len(faces_before)
    after_count = len(faces_after)
    results = []
    for i, face in enumerate(encodings_after):
        result = face_recognition.compare_faces(
            encodings_before, face, tolerance=tolerance
        )
        if debug:
            print(i, result)
        results.append(result)
    get_on_count = 0
    for face in np.array(results):
        if True not in face:
            get_on_count += 1
    got_off_count = before_count + get_on_count - after_count
    return [before_count, get_on_count, got_off_count, after_count]
