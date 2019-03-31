import cv2
import time
import socket
import Image
import StringIO

cap = cv2.VideoCapture(0)

HOST, PORT = '10.1.1.237', 9999

sock =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

#fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
fourcc = cv2.cv.FOURCC('M', 'J', 'P', 'G')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

while cap.isOpened():
    ret, frame = cap.read()

    if ret == True:
        # frame = cv2.flip(frame, 0)

        out.write(frame)

        cv2.imshow('frame', frame)
        #if cv2.waitKey(1) & 0xFF == ord('q'):
         #   break
        if ret is False:
            print("can not get this frame")
            continue

        pi = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        buf = StringIO.StringIO()
        pi.save(buf, format='JPEG')
        jpeg = buf.getvalue()
        buf.close()
        transfer = jpeg.replace('\n', '\-n')
        print len(transfer), transfer[-1]
        sock.sendall(transfer + "\n")
        # time.sleep(0.2)
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()
sock.close()

