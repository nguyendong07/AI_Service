import face_recognition

def compare(path1, path2):
    known_image = face_recognition.load_image_file(path1)
    unknown_image = face_recognition.load_image_file(path2)
    biden_encoding = face_recognition.face_encodings(known_image)[0]
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
    face_distance = face_recognition.face_distance([biden_encoding],unknown_encoding)
    return face_distance[0]



