import mediapipe as mp

mp_hands = mp.solutions.hands
hands=mp_hands.Hands()
mp_draw=mp.solutions.drawing_utils

def give_posture(frame):
    results=hands.process(frame)
    if results.multi_hand_landmarks:
        for hand_lms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame,hand_lms,mp_hands.HAND_CONNECTIONS)
    return frame
