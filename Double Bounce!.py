from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

W_Width, W_Height = 800,600

freeze = False
gameOver = False
score = 0
speed = 0.2

ps = False
dn = False
jumping = False
ball_speed = 0.15
jump_count = 0
jump_start = 0
ball_return = False
second_jump = False

lines = [([random.randint(30,60),[i*100, random.randint(5,200)]]) for i in range(8)]
ball_pos = [400+(lines[4][0]/2),lines[4][1][1]+15-2]
special_shape = [([random.randint(1,3),[random.randint(800,1600), random.randint(250,500)]]) for i in range(5)]

def draw_shapes():
    global special_shape
    for i,j in special_shape:
        uniqe = i
        x,y = j
        if uniqe == 1:
            glPointSize(2)
            glColor3f(1.0, 0.5, 1.0)
            draw(x, y, x+20, y)
            draw(x,y+10,x+20,y-10)
            draw(x,y-10,x+20,y+10)
        elif uniqe == 2:
            glPointSize(2)
            glColor3f(1.0, 0.5, 0.0)
            draw(x, y+6, x + 20, y+6)
            draw(x, y - 6, x + 20, y - 6)
            draw(x+3, y - 10, x + 8, y + 10)
            draw(x+14, y-10, x+17, y+10)
        elif uniqe == 3:
            glPointSize(2)
            glColor3f(0.1, 0.5, 0.1)
            draw(x, y, x + 10, y +10)
            draw(x,y,x+10,y-10)
            draw(x+10,y+10,x+20,y)
            draw(x+10,y-10,x+20,y)

def draw_lines():
    global lines,ball_pos
    for i,j in lines:
        l = i
        lx, ly = j
        glColor3f(0.0, 0.4, 1.0)
        glPointSize(4)
        draw(lx, ly, lx+l, ly)
        glPointSize(2)
        MidpointCircle(ball_pos[0], ball_pos[1], 10, (1.0, 0.2, 0.0))

def refresh_game():
    global special_shape, gameOver,score,freeze,speed,ball_pos,jumping,jump_count,jump_start,ball_return,second_jump
    if not freeze and not gameOver:
        by_ball, bl_ball = int(ball_pos[1] - 10), int(ball_pos[0] - 10)

        for i, j in special_shape:
            j[0]-= speed+0.1
            x,y = j
            if (bl_ball < int(x+20)) and ((bl_ball + 20) > int(x)) and (by_ball < int(y+10)) and (by_ball+20 > int(y-10)):
                if i == 1:
                    score += 3
                    special_shape.remove([i,j])
                    special_shape.append([random.randint(1,3),[j[0]+800, random.randint(250,500)]])
                    print(f'Score: {score}')
                elif i == 3:
                    score += 5
                    special_shape.remove([i,j])
                    special_shape.append([random.randint(1,3),[j[0]+800, random.randint(250,500)]])
                    print(f'Score: {score}')
                else:
                    print(f"Game Over. Final Score: {score}")
                    freeze = True
                    gameOver = True
            elif x+20<=0:
                special_shape.remove([i,j])
                special_shape.append([random.randint(1,3),[800,random.randint(250,500)]])

        for i, j in lines:
            l = int(i)
            lx, ly = j

            j[0]-= speed
            if jumping and not ball_return:
                if ball_pos[1]<=jump_start+200:
                    ball_pos[1] += ball_speed
                elif ball_pos[1]>=jump_start+200:
                    ball_return = True
                elif (bl_ball < int(lx+l)) and ((bl_ball+20)>int(lx)) and (by_ball<int(ly-2)) and (by_ball>int(ly+3)):
                    ball_return = True
            elif not jumping:
                if (bl_ball < int(lx+l)) and ((bl_ball+20)>int(lx)) and (by_ball>int(ly-2)) and (by_ball<int(ly+3)):
                    ball_pos[1]=ly+10+3
                    ball_return = False
                    jumping = False
                    jump_count = 0
                else:
                    ball_pos[1] -= ball_speed

            if ball_return:
                if second_jump:
                    second_jump = False
                    jumping = True
                    ball_return = False
                if (bl_ball < int(lx+l)) and ((bl_ball+20)>int(lx)) and (by_ball>int(ly-2)) and (by_ball<int(ly+3)):
                    ball_pos[1]=ly+10+3
                    ball_return = False
                    jumping = False
                    jump_count = 0
                else:
                    ball_pos[1] -= ball_speed
            if lx+l <=0:
                lines.remove([i,j])
                score += 1
                lines.append([random.randint(30,60),[800, random.randint(5,200)]])
                print(f'Score: {score}')
        if by_ball <= 0:
                print(f"Game Over. Final Score: {score}")
                freeze = True
                gameOver = True
    elif gameOver:
        glPointSize(5)
        glColor3f(0.0, 0.0, 0.5)
        draw(200,150,600,450)
        draw(200,450,600,150)

def convert_coordinate(x,y):
    global W_Width, W_Height
    a = x
    b = (W_Height) - y
    return a,b

def keyboardListener(key, x, y):
    global freeze,jumping,jump_count,ball_pos,jump_start,second_jump,ball_pos
    if not freeze:
        if key == b' ':
            if jump_count <2:
                jumping = True
                jump_count += 1
                if jump_count == 2:
                    second_jump = True
                jump_start = ball_pos[1]
    glutPostRedisplay()

def special_key(key, x, y):
    global freeze,jumping,jump_count,ball_pos,jump_start,second_jump,ball_pos
    if not freeze:
        n = ball_pos[0]
        if key == GLUT_KEY_LEFT:                                                  #left_arrow
            if n-15>0:
                ball_pos[0]-=5
            else:
                ball_pos[0]=10
                print("Already in boundary")
        elif key == GLUT_KEY_RIGHT:                                                #right_arrow
            if n + 15 < 800:
                ball_pos[0] += 5
            else:
                ball_pos[0] = 790
                print("Already in boundary")
    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global freeze,gameOver,score,ps,dn,lines,ball_pos,jumping,jump_count,second_jump,ball_return,special_shape

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        #print(x,y)
        c_x, c_y = convert_coordinate(x, y)

        if 20 < c_x < 60 and 540 < c_y < 580:      #reset
            n = -20
            freeze = False
            gameOver = False
            score = 0
            jumping = False
            jump_count = 0
            second_jump = False
            ball_return = False
            dn = False
            lines = [([random.randint(30, 60), [i * 100, random.randint(5, 200)]]) for i in range(8)]
            ball_pos = [400 + (lines[4][0] / 2), lines[4][1][1] + 15 - 2]
            special_shape = [([random.randint(1, 3), [random.randint(800, 1600), random.randint(250, 500)]]) for i in
                             range(5)]
            print( "Starting Over")

        elif 680 < c_x < 720 and 540 < c_y < 580:       #pause
            if not gameOver:
                ps = not ps
                freeze = not freeze
                if freeze:
                    print("Frozen")
                else:
                    print("Unfreeze")
        elif 740 < c_x < 780 and 540 < c_y < 580:   #exit
            print(f"Goodbye. Final Score: {score}")
            glutLeaveMainLoop()
        elif 80< c_x < 120 and 540 <c_y <580:   #daynight
            dn = not dn

def MidpointCircle(cx, cy, r,color):
    d = 1-r
    x=0
    y=r
    circlePoints(x,y,cx,cy,color)
    while(x<y):
        if d<0:
            d = d+ 2*x + 3
            x = x+1
        else:
            d = d + 2*x - 2*y + 5
            x = x+1
            y = y-1
        circlePoints(x,y,cx,cy,color)

def circlePoints(x,y,cx,cy,color):
    #glPointSize(2)
    glBegin(GL_POINTS)
    glColor3f(*color)

    glVertex2f(x+cx,y+cy)
    glVertex2f(y+cx,x+cy)
    glVertex2f(y+cx,-x+cy)
    glVertex2f(x+cx,-y+cy)
    glVertex2f(-x+cx,-y+cy)
    glVertex2f(-y+cx,-x+cy)
    glVertex2f(-y+cx,x+cy)
    glVertex2f(-x+cx,y+cy)
    glEnd()

def draw_button():

    glPointSize(2.5)
    glColor3f(0.0, 0.4, 1.0)
    draw(20,580,60,580)
    draw(20,540,60, 540)
    draw(20,580,21,540)
    draw(20,540,21,580)
    draw(59, 580, 60, 540)
    draw(59, 540, 60, 580)

    draw(25,560,50,575)
    draw(25,560,50,545)

    glColor3f(1.0, 0.1, 0.1)
    draw(740, 580, 780, 580)
    draw(740, 540, 780, 540)
    draw(740, 580, 741, 540)
    draw(740, 540, 741, 580)
    draw(779, 580, 780, 540)
    draw(779, 540, 780, 580)

    draw(750,575,770,545)
    draw(750,545,770,575)

    draw_Pbutton()
    draw_dnbutton()

def draw_dnbutton():                           #Day night
    global dn
    if dn:
        glClearColor(0.2, 0.2, 0.2, 1.0)
        glColor3f(1.0, 1.0, 1.0)
        draw(80, 580, 120, 580)
        draw(80, 540, 120, 540)
        draw(80, 580, 81, 540)
        draw(80, 540, 81, 580)
        draw(119, 580, 120, 540)
        draw(119, 540, 120, 580)
        glPointSize(4)
        MidpointCircle(100, 560, 10, (1.0, 1.0, 0.1))
        glPointSize(10)
        MidpointCircle(100, 560, 3, (1.0, 1.0, 0.1))

        #moon
        glPointSize(2)
        MidpointCircle(300, 550, 25, (1.0, 1.0, 1.0))
        MidpointCircle(300, 550, 28, (1.0, 1.0, 1.0))
        glPointSize(1)
        MidpointCircle(300, 550, 31, (1.0, 1.0, 1.0))
        glPointSize(4)
        MidpointCircle(300,550,23,(1.0,1.0,1.0))
        glPointSize(8)
        MidpointCircle(300, 550, 21, (1.0, 1.0, 1.0))
        glPointSize(20)
        MidpointCircle(300, 550, 8, (1.0, 1.0, 1.0))




    else:
        glClearColor(0.5, 1.0, 1.0, 1.0)
        glColor3f(0.0, 0.0, 0.0)
        draw(80, 580, 120, 580)
        draw(80, 540, 120, 540)
        draw(80, 580, 81, 540)
        draw(80, 540, 81, 580)
        draw(119, 580, 120, 540)
        draw(119, 540, 120, 580)
        MidpointCircle(100, 560, 12, (1.0, 1.0, 1.0))

        # sun
        glPointSize(2)
        MidpointCircle(300, 550, 25, (1.0, 1.0, 0.5))
        MidpointCircle(300, 550, 28, (1.0, 1.0, 0.5))
        draw(335, 550, 350, 550)
        draw(250, 550, 265, 550)
        draw(313, 582, 320, 595)
        draw(287, 582, 280, 595)
        draw(280, 505, 287, 518)
        draw(313, 518, 320, 505)

        glPointSize(1)
        MidpointCircle(300, 550, 31, (1.0, 1.0, 0.5))
        glPointSize(4)
        MidpointCircle(300, 550, 23, (1.0, 1.0, 0.0))
        glPointSize(8)
        MidpointCircle(300, 550, 21, (1.0, 1.0, 0.0))
        glPointSize(20)
        MidpointCircle(300, 550, 8, (1.0, 1.0, 0.0))

def draw_Pbutton():
    global ps
    if ps:
        glColor3f(1.0, 1.0, 0.1)
        draw(680, 580, 720, 580)
        draw(680, 540, 720, 540)
        draw(680, 580, 681, 540)
        draw(680, 540, 681, 580)
        draw(719, 580, 720, 540)
        draw(719, 540, 720, 580)

        draw(685,575,715,560)
        draw(685,545,715,560)
        draw(685, 575, 686, 545)
        draw(685, 545, 686, 575)

    else:
        glColor3f(0.0, 1.0, 0.1)
        draw(680, 580, 720, 580)
        draw(680, 540, 720, 540)
        draw(680, 580, 681, 540)
        draw(680, 540, 681, 580)
        draw(719, 580, 720, 540)
        draw(719, 540, 720, 580)

        draw(690, 575, 691, 545)
        draw(690, 545, 691, 575)
        draw(710, 575, 711, 545)
        draw(710, 545, 711, 575)

def writePixel(x,y,z):
    if z == 0:
        x,y=x,y
    else:
        (x,y)=convertOriginal(x,y,z)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def draw(x1,y1,x2,y2):
    z = FindZone(x1,y1,x2,y2)
    if z== 0:
        MidpointLine(x1,y1,x2,y2,z)
    else:
        (x1,y1) = convert_nTo0(x1,y1,z)
        (x2,y2) = convert_nTo0(x2,y2,z)
        MidpointLine(x1, y1, x2, y2, z)

def MidpointLine(x1,y1,x2,y2,z):
    dx = x2 - x1
    dy = y2 - y1
    d = 2*dy - dx
    incE = 2*dy
    incNE = 2*(dy - dx)
    x = x1
    y = y1
    writePixel(x,y,z)
    while x<x2:
        if d<=0:
            d = d + incE
            x += 1
        else:
            d += incNE
            x += 1
            y += 1
        writePixel(x,y,z)

def FindZone(x1,y1,x2,y2):
    dx = x2 - x1
    dy = y2 - y1
    z = 0
    if abs(dx)>abs(dy):
        if dx>0 and dy>0:
            z = 0
        elif dx<0 and dy>0:
            z = 3
        elif dx<0 and dy<0:
            x = 4
        elif dx>0 and dy<0:
            z = 7
    else:
        if dx>0 and dy>0:
            z = 1
        elif dx<0 and dy>0:
            z = 2
        elif dx<0 and dy<0:
            x = 5
        elif dx>0 and dy<0:
            z = 6
    return z

def convert_nTo0(X,Y,z):
    if z==1: x,y = Y,X
    elif z==2: x,y = Y,-X
    elif z==3: x,y = -X,Y
    elif z==4: x,y = -X,-Y
    elif z==5: x,y = -Y,-X
    elif z==6: x,y = -Y,X
    elif z==7: x,y = X,-Y
    return (x,y)

def convertOriginal(X,Y,z):
    if z==1: x,y = Y,X
    elif z==2: x,y = -Y,X
    elif z==3: x,y = -X,Y
    elif z==4: x,y = -X,-Y
    elif z==5: x,y = -Y,-X
    elif z==6: x,y = Y,-X
    elif z==7: x,y = X,-Y
    return (x,y)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.5, 1.0, 1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    draw_button()
    draw_lines()
    draw_shapes()
    refresh_game()

    glutSwapBuffers()

def init():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, W_Width, 0, W_Height)

glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)

wind = glutCreateWindow(b"Double Bounce!")
init()
glutDisplayFunc(display)
glutIdleFunc(display)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(special_key)
glutMouseFunc(mouseListener)
glutMainLoop()
