import orjson


class Handlandmark:
    def __init__(self,handedness):
        self.result_type="hand"
        self.handedness=handedness
        self.landmarks=list()

    def add_world_landmarks(self, world_landmarks):
        self.landmarks.clear()
        for lm in world_landmarks:
            #保留5位小数
            self.landmarks.append({"x": round(-lm.x, 5), "y": round(lm.y, 5), "z": round(-lm.z, 5)})

    def to_json(self):

        return orjson.dumps({
            "result_type":self.result_type,
            "handedness": self.handedness,
            "hand_world_landmarks": self.landmarks
        })

class Faceblendshape:
    def __init__(self):
        self.result_type="face_blendshape"
        self.face_blendshape=list()

    def add_face_blendshape(self, face_blendshape):
        self.face_blendshape.clear()
        for bs in face_blendshape:
            self.face_blendshape.append({"name":bs.category_name,"score":bs.score})

    def to_json(self):
        return orjson.dumps({

            "result_type":self.result_type,
            "face_blendshape": self.face_blendshape
        })

class Facelandmark:
    def __init__(self):
        self.result_type="face_landmarks"
        self.face_landmarks=list()

    def add_face_landmarks(self, face_landmarks):
        self.face_landmarks.clear()
        for lm in face_landmarks:
            self.face_landmarks.append({"x": round(-lm.x, 5), "y": round(lm.y, 5), "z": round(-lm.z, 5)})

    def to_json(self):
        return orjson.dumps({

            "result_type":self.result_type,
            "face_landmarks": self.face_landmarks
        })
class Poselandmark:
    def __init__(self):
        self.result_type="pose"
        self.landmarks=list()

    def add_world_landmarks(self, world_landmarks):
        self.landmarks.clear()
        for lm in world_landmarks:
            self.landmarks.append({"x": round(-lm.x, 5), "y": round(lm.y, 5), "z": round(-lm.z, 5)})

    def to_json(self):
        return orjson.dumps({
            "result_type":self.result_type,
            "landmarks": self.landmarks
        })












