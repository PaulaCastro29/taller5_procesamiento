#-----------------------------------------
#TALLER 5: PAULA CASTRO Y MICHAEL CONTRERAS
#-----------------------------------------

#Importación de librerias
import cv2
import os
import numpy as np

#Se cargan todas las imagenes contenidas en el folder
input_images_path = "C:/CodigoPyCharmPaula/proyecciones/imagenes"
files_names = os.listdir(input_images_path)

#Se le muestra al usuario la cantidad de imagenes y su orden
print("El número de imagenes es: ", len(files_names))
print("las imagenes son:",files_names)

#Se le solicita al usuario seleccionar la imagen de referencia para aplicar las homografias y se valida que este dentro de la cantidad de imagenes
N = int(input('Ingrese el número de la imagen que quiere tomar como referencia:'))
if N>=1 and N <= len(files_names):
   N=N
   #print(N)
else:
   print ("Error! el número ingresado supera el número de imagenes")
#De acuerdo con la imagen de referencia seleccionada se aplica la homografia al primer par de imagenes Nota. en este código solo se ve el caso en el que la imagen de referencia es 2.
if N==2:

    lista=[]
    for file_name in files_names:
        image_path = input_images_path + "/" + file_name
        #print(file_name)
        #print(image_path)
        lista.append(image_path)
    image1 = lista[0]
    image2 = lista[1]
    image3 = lista[2]
    vista1=cv2.imread(image1)
    vista2=cv2.imread(image2)
    vista3=cv2.imread(image3)
    imagen1 = cv2.resize(vista1, (400, 400), interpolation=cv2.INTER_CUBIC)
    imagen2 = cv2.resize(vista2, (400, 400), interpolation=cv2.INTER_CUBIC)
    imagen3 = cv2.resize(vista3, (400, 400), interpolation=cv2.INTER_CUBIC)
    concat_horizontal1=cv2.hconcat([imagen1,imagen2])
    concat_horizontal2=cv2.hconcat([imagen2,imagen3])

    points = []

    def click(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            points.append((x, y))

    image = concat_horizontal1
    image_draw = np.copy(image)

    points1 = []
    points2 = []

    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", click)

    point_counter = 0
    while True:
        cv2.imshow("Image", image_draw)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("x"):
            points1 = points.copy()
            points = []
            break
        if len(points) > point_counter:
            point_counter = len(points)
            cv2.circle(image_draw, (points[-1][0], points[-1][1]), 3, [0, 0, 255], -1)

    point_counter = 0
    while True:
        cv2.imshow("Image", image_draw)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("x"):
            points2 = points.copy()
            points = []
            break
        if len(points) > point_counter:
            point_counter = len(points)
            cv2.circle(image_draw, (points[-1][0], points[-1][1]), 3, [255, 0, 0], -1)

    N = min(len(points1), len(points2))
    assert N >= 4, 'At least four points are required'

    pts1 = np.array(points1[:N])
    pts2 = np.array(points2[:N])

    u = []
    u1 = [400, 0]
    u2 = [400, 0]
    u3 = [400, 0]
    u4 = [400, 0]
    u.append(u1)
    u.append(u2)
    u.append(u3)
    u.append(u4)
    k = pts2 - u
    pts2 = k

    if False:
        H, _ = cv2.findHomography(pts1, pts2, method=0)
    else:
        H, _ = cv2.findHomography(pts1, pts2, method=cv2.RANSAC)

    image_warped = cv2.warpPerspective(image, H, (image.shape[1], image.shape[0]))
    #image_warped = cv2.cvtColor(image_warped, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Image", image)
    cv2.imshow("Image warped", image_warped)
    cv2.waitKey(0)

    # Se aplica la segunda homografia al segundo par de imagenes
    image2 = concat_horizontal2
    image_draw2 = np.copy(image2)

    points11 = []
    points22 = []

    cv2.namedWindow("Image2")
    cv2.setMouseCallback("Image2", click)

    point_counter1 = 0
    while True:
        cv2.imshow("Image2", image_draw2)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("x"):
            points11 = points.copy()
            points = []
            break
        if len(points) > point_counter1:
            point_counter1 = len(points)
            cv2.circle(image_draw2, (points[-1][0], points[-1][1]), 3, [0, 0, 255], -1)

    point_counter1 = 0
    while True:
        cv2.imshow("Image2", image_draw2)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("x"):
            points22 = points.copy()
            points = []
            break
        if len(points) > point_counter1:
            point_counter1 = len(points)
            cv2.circle(image_draw2, (points[-1][0], points[-1][1]), 3, [255, 0, 0], -1)

    N = min(len(points11), len(points22))
    assert N >= 4, 'At least four points are required'

    pts11 = np.array(points11[:N])
    pts22 = np.array(points22[:N])

    o = []
    o1 = [400, 0]
    o2 = [400, 0]
    o3 = [400, 0]
    o4 = [400, 0]
    o.append(o1)
    o.append(o2)
    o.append(o3)
    o.append(o4)
    l = pts22 - o
    pts22 = l

    if False:
        H, _ = cv2.findHomography(pts22, pts11, method=0)
    else:
        H, _ = cv2.findHomography(pts22, pts11, method=cv2.RANSAC)

    image_warped2 = cv2.warpPerspective(image2, H, (image2.shape[1], image2.shape[0]))
    #image_warped2 = cv2.cvtColor(image_warped2, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Image2", image2)
    cv2.imshow("Image warped2", image_warped2)
    cv2.waitKey(0)

#Se realiza la suma de imagenes y se visualiza
    promedio = (image_warped2 + image_warped)
    cv2.imshow("promedio", promedio)
    cv2.imwrite("promedio3.png", promedio)
    cv2.waitKey(0)

else:
   print ("Error! el número ingresado es diferente de 2 para efectos del taller utilice el 2 para ejecutar el caso")