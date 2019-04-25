import sys
sys.path.insert(0,'/home/iclab-arm/.local/lib/python3.5/site-packages/')
import cv2

cap = cv2.VideoCapture(0)

# 設定影像的尺寸大小
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

photo_id = 0
photo_path = './'
photo_name = 'zzz_'
photo_type = '.jpg'

while(cap.isOpened()):
  ret, frame = cap.read()
  
  if ret == True:
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('s'):
      photo_id+=1
      file_name = photo_path + photo_name + str(photo_id) + photo_type
      cv2.imwrite(file_name, frame)
      # print(str(photo_id) + 'save file to ' + file_name)

      print('Save no[%d] photo to %s.' %(photo_id, file_name))

    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
  else:
    print('ret == False:')

cap.release()
cv2.destroyAllWindows()
