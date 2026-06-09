import os
import cv2
import numpy as np
import tensorflow as tf

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "mobilefacenet.tflite"
)

CASCADE_PATH = (
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)


class FaceService:

    def __init__(self):

        print("MODEL =", MODEL_PATH)
        print("EXISTS =", os.path.exists(MODEL_PATH))

        self.interpreter = tf.lite.Interpreter(
            model_path=MODEL_PATH
        )

        self.interpreter.allocate_tensors()

        self.input_details = (
            self.interpreter.get_input_details()
        )

        self.output_details = (
            self.interpreter.get_output_details()
        )

    def crop_face(self, image_path):

        image = cv2.imread(image_path)

        if image is None:
            return None

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        detector = cv2.CascadeClassifier(
            CASCADE_PATH
        )

        faces = detector.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(100, 100)
        )

        if len(faces) == 0:
            return None

        x, y, w, h = faces[0]

        face = image[
            y:y + h,
            x:x + w
        ]

        return face

    def generate_embedding(
        self,
        image_path
    ):

        face = self.crop_face(
            image_path
        )

        if face is None:
            raise Exception(
                "No face detected"
            )

        face = cv2.resize(
            face,
            (112, 112)
        )

        face = cv2.cvtColor(
            face,
            cv2.COLOR_BGR2RGB
        )

        face = (
            face.astype(np.float32)
            / 255.0
        )

        face = np.expand_dims(
            face,
            axis=0
        )

        self.interpreter.set_tensor(
            self.input_details[0]["index"],
            face
        )

        self.interpreter.invoke()

        output = self.interpreter.get_tensor(
            self.output_details[0]["index"]
        )

        return output[0]

    def cosine_similarity(
        self,
        emb1,
        emb2
    ):

        emb1 = np.array(
            emb1,
            dtype=np.float32
        )

        emb2 = np.array(
            emb2,
            dtype=np.float32
        )

        similarity = (
            np.dot(emb1, emb2)
            /
            (
                np.linalg.norm(emb1)
                *
                np.linalg.norm(emb2)
            )
        )

        return float(similarity)

    def verify_face(
        self,
        image_path,
        stored_embedding
    ):

        new_embedding = self.generate_embedding(
            image_path
        )

        similarity = self.cosine_similarity(
            new_embedding,
            stored_embedding
        )



        print("=" * 60)
        print("=" * 60)
        print("FACE SIMILARITY =", similarity)
        print("MATCH RESULT    =", similarity >= 0.70)
        print("=" * 60)
        print("=" * 60)

        # Testing threshold
        return similarity >= 0.30