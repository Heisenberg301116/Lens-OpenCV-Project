import face_recognition
import cv2

img1= face_recognition.load_image_file('Obama.jpg')
img1= cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
face1= face_recognition.face_locations(img1)[0]
encode_face1= face_recognition.face_encodings(img1)[0]
cv2.rectangle(img1, (face1[3],face1[0],face1[1],face1[2]), (0,255,0), 3)

img2= face_recognition.load_image_file('Trump.jpg')
img2= cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
face2= face_recognition.face_locations(img2)[0]
encode_face2= face_recognition.face_encodings(img2)[0]
cv2.rectangle(img2, (face2[3],face2[0],face2[1],face2[2]), (0,255,0), 3)

cv2.imshow("Obama",img1)


res= face_recognition.compare_faces([encode_face1],encode_face2)
face_dis= face_recognition.face_distance([encode_face1],encode_face2)
cv2.putText(img2, f"{res}, {round(face_dis[0],2)}", (20,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0),2)
cv2.imshow("Trump",img2)
print(res, face_dis)

cv2.waitKey()
cv2.destroyAllWindows()