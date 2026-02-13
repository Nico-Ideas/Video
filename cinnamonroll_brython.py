from browser import document, html
import math

# Variables globales
canvas = None
ctx = None
pen_x = 0
pen_y = 0
pen_angle = 0
pen_down = True
pen_color = "black"
fill_color = "white"
pen_size = 4
is_filling = False
fill_path = None

def init_canvas(canvas_id):
    """Inicializa el canvas para dibujar"""
    global canvas, ctx, pen_x, pen_y, pen_angle
    canvas = document[canvas_id]
    if canvas:
        ctx = canvas.getContext("2d")
        # Reset transform y limpiar el canvas
        ctx.setTransform(1, 0, 0, 1, 0, 0)
        ctx.clearRect(0, 0, canvas.width, canvas.height)

        # Transformar el canvas para que Y+ vaya hacia arriba (como turtle)
        ctx.translate(canvas.width / 2, canvas.height / 2)  # Mover origen al centro
        ctx.scale(1, -1)  # Invertir eje Y
        
        # Posición inicial (ahora en sistema turtle)
        pen_x = 0
        pen_y = 0
        pen_angle = 0
        ctx.lineWidth = pen_size
        ctx.strokeStyle = pen_color
        ctx.fillStyle = fill_color
        ctx.lineCap = "round"
        ctx.lineJoin = "round"

def penup():
    global pen_down
    pen_down = False

def pendown():
    global pen_down
    if not pen_down and not is_filling:
        ctx.beginPath()
        ctx.moveTo(pen_x, pen_y)
    pen_down = True

def goto(x, y):
    """Mover a posición absoluta (ahora en coords turtle directamente)"""
    global pen_x, pen_y
    
    if pen_down:
        ctx.lineTo(x, y)
        if not is_filling:
            ctx.stroke()
    else:
        if not is_filling:
            ctx.beginPath()
        ctx.moveTo(x, y)
    
    pen_x = x
    pen_y = y

def setheading(angle):
    """Establecer dirección en grados (0 = este, 90 = norte)"""
    global pen_angle
    pen_angle = angle

def circle(radius, extent=360):
    """Dibujar un arco/círculo - precisión optimizada"""
    global pen_x, pen_y, pen_angle
    
    # Guardar posición inicial
    start_x = pen_x
    start_y = pen_y
    start_heading = pen_angle
    
    # Calcular centro del círculo en coordenadas turtle
    # radius > 0: centro a la izquierda (heading + 90°)
    # radius < 0: centro a la derecha (heading - 90°)
    direction = 1 if radius > 0 else -1
    center_heading = start_heading + (90 * direction)
    
    center_heading_rad = math.radians(center_heading)
    center_x = start_x + abs(radius) * math.cos(center_heading_rad)
    center_y = start_y + abs(radius) * math.sin(center_heading_rad)
    
    # Ángulo inicial desde centro hacia posición inicial
    start_angle_rad = math.atan2(start_y - center_y, start_x - center_x)
    
    # Dibujar con pasos suaves (más pasos = más precisión)
    steps = max(int(abs(extent) / 2), 1)  # 1 paso cada 2 grados
    
    for i in range(1, steps + 1):
        # Rotación progresiva alrededor del centro
        rotation_rad = math.radians(direction * extent * i / steps)
        current_angle_rad = start_angle_rad + rotation_rad
        
        # Calcular nueva posición en coordenadas turtle
        new_x = center_x + abs(radius) * math.cos(current_angle_rad)
        new_y = center_y + abs(radius) * math.sin(current_angle_rad)
        
        # Dibujar línea
        if pen_down:
            ctx.lineTo(new_x, new_y)
        else:
            ctx.moveTo(new_x, new_y)
        
        pen_x = new_x
        pen_y = new_y
    
    # Actualizar heading final
    pen_angle = (start_heading + (direction * extent)) % 360
    
    # Stroke si no estamos en fill mode
    if pen_down and not is_filling:
        ctx.stroke()

def pensize(size):
    global pen_size
    pen_size = size
    ctx.lineWidth = size

def pencolor(color):
    global pen_color
    pen_color = color
    ctx.strokeStyle = color

def fillcolor(color):
    global fill_color
    fill_color = color
    ctx.fillStyle = color

def begin_fill():
    global is_filling, fill_path
    is_filling = True
    ctx.beginPath()
    ctx.moveTo(pen_x, pen_y)

def end_fill():
    global is_filling
    if is_filling:
        ctx.closePath()
        ctx.fill()
        ctx.stroke()
        is_filling = False

def go(x, y):
    """Función auxiliar equivalente a penup, goto, pendown"""
    penup()
    goto(x, y)
    pendown()

def draw_cinnamonroll():
    """Dibuja a Cinnamonroll completo"""
    init_canvas("cinna-canvas")
    
    pencolor("black")
    fillcolor("white")
    
    # Cuerpo principal
    go(90.36, 50.50)
    begin_fill()
    setheading(335.48)
    circle(184.32, 49.04)
    setheading(29.62)
    circle(43.20, 85.3)
    setheading(120.63)
    circle(52.95, 94.33)
    setheading(209.57)
    circle(-104.61, 54.85)
    setheading(160.45)
    circle(49.63, 68.51)
    setheading(160.38)
    circle(123.19, 66.97)
    setheading(175.54)
    circle(51.51, 59.01)
    setheading(234.55)
    circle(-193.42, 30.71)
    setheading(190.87)
    circle(65.22, 29.81)
    setheading(238.45)
    circle(40.72, 121.52)
    setheading(0.63)
    circle(108.89, 66.86)
    setheading(293.19)
    circle(63.23, 7.9)
    setheading(310.94)
    circle(38.76, 38.84)
    setheading(357.3)
    circle(394.86, 24.1)
    setheading(19.1)
    circle(48.19, 58.73)
    setheading(90)
    circle(50.57, 61.76)
    end_fill()
    
    # Líneas internas cabeza
    go(52.48, 97.04)
    setheading(151.45)
    circle(123.192, 83.7)
    
    go(-114.54, 34.24)
    setheading(238.9)
    circle(63.23, 62.2)
    
    # Nariz/boca
    go(0, 0)
    setheading(284.57)
    circle(-3.94, 141.58)
    setheading(155.93)
    circle(19.37, 74.76)
    setheading(216.84)
    circle(-5.73, 111.73)
    
    # Ojos (DeepSkyBlue)
    pensize(6)
    pencolor("DeepSkyBlue")
    fillcolor("DeepSkyBlue")
    pensize(4)
    
    go(55.06, 23.35)
    setheading(168.87)
    circle(34.23, 41.37)
    setheading(57.66)
    circle(-44.08, 36.45)
    
    go(-71.49, -3.85)
    begin_fill()
    setheading(70.71)
    circle(20.48, 72.59)
    setheading(153.37)
    circle(5.41, 71.85)
    setheading(225.22)
    circle(18.29, 89.94)
    setheading(320.4)
    circle(8.39, 110.31)
    end_fill()
    
    # Mejillas (LightPink)
    pencolor("LightPink")
    fillcolor("LightPink")
    
    go(55.30, -8.89)
    begin_fill()
    setheading(356.76)
    circle(35.78, 49.23)
    setheading(61.68)
    circle(10.85, 71.8)
    setheading(149.39)
    circle(25.98, 78.22)
    setheading(224.84)
    circle(10.95, 127.88)
    end_fill()
    
    go(-79.52, -30.64)
    begin_fill()
    setheading(43.04)
    circle(10.08, 113.14)
    setheading(154.55)
    circle(26.35, 60)
    setheading(219.12)
    circle(9.62, 90)
    setheading(313.32)
    circle(21.61, 89.72)
    end_fill()
    
    # Brazos/patas (blanco)
    pencolor("black")
    fillcolor("white")
    
    go(52.17, -71.53)
    begin_fill()
    setheading(56.48)
    circle(-41.155)
    end_fill()
    
    go(52.17, -71.53)
    setheading(235.37)
    circle(23.90, 164.98)
    setheading(50.62)
    circle(10.70, 81.85)
    
    # Cuerpo/ropa
    go(41.96, -26.99)
    begin_fill()
    setheading(197.01)
    circle(-394.86, 16.06)
    setheading(215.23)
    circle(25.44, 72.43)
    setheading(232.24)
    circle(55.76, 31.75)
    setheading(238.91)
    circle(-26.90, 71.18)
    setheading(229.02)
    circle(15.89, 120.9)
    setheading(349.42)
    circle(62.55, 34.42)
    setheading(336.13)
    circle(109.16, 36.79)
    setheading(259.29)
    circle(27.96, 53.73)
    setheading(309.39)
    circle(17.50, 85.76)
    setheading(85.18)
    circle(-22.97, 31.31)
    setheading(60.59)
    circle(91.51, 15.57)
    setheading(31.53)
    circle(60.12, 91.14)
    setheading(62.33)
    circle(-69.61, 27.96)
    setheading(347.04)
    circle(10.24, 165.01)
    setheading(164.03)
    circle(42.22, 77.17)
    end_fill()
    
    # Detalles internos
    go(-59.31, -57.97)
    setheading(208.74)
    circle(55.76, 66.4)
    
    go(-81.70, -129.58)
    setheading(329.65)
    circle(109.16, 49.27)
    
    go(34.17, -138.64)
    setheading(23.17)
    circle(60.12, 99.51)
    
    go(58.48, -56.57)
    setheading(67.48)
    circle(-69.61, 33.11)
    
    go(38.37, -35.71)
    setheading(74.03)
    circle(-42.22, 90)

def clear_canvas():
    """Limpia el canvas"""
    if canvas and ctx:
        ctx.setTransform(1, 0, 0, 1, 0, 0)
        ctx.clearRect(0, 0, canvas.width, canvas.height)

# Exponer funciones al scope global de JavaScript
from browser import window 
window.drawCinnamonrollPython = draw_cinnamonroll
window.clearCinnamonrollPython = clear_canvas
