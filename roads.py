from car import *
from stoplight import *
from config import *


def convert_point(wind_w, wind_h, img_w, img_h):
    def img_point(img_x, img_y): 
        wind_x = wind_w*img_x/img_w
        wind_y = wind_h*abs(img_y)/img_h
        if img_y > 0:
            wind_y = -wind_h*img_y/img_h
        return wind_x, wind_y
    return img_point

point_conv = convert_point(MONITOR_WIDTH, MONITOR_HEIGHT, 14.2537655875977, 10.6457995712726)

stl = []
cal = []

sl1 = Stop_list()
cl1 = Car_list()
sl1.append(Stoplight(point_conv(7.6040508858542,-10.988897567), first = True))
sl1.append(Stoplight(point_conv(7.5857334281685,-10.4967569592598)))
sl1.append(Stoplight(point_conv(7.3808035940509,-7.1344267533614), red = True, fake = False))
sl1.append(Stoplight(point_conv(7.2595890988185,-5.7522480204051)))
sl1.append(Stoplight(point_conv(7.1784425539869,-5.052563467463)))
sl1.append(Stoplight(point_conv(7.1335558491196,-4.4526734406905)))
sl1.append(Stoplight(point_conv(7.0779503764026,-3.9245860696794)))
sl1.append(Stoplight(point_conv(6.9171351030933,-0.3918488307016)))
sl1.append(Stoplight(point_conv(6.8920992981044,0.4092969289417), last = True))
stl.append(sl1)
cal.append(cl1)

sl2 = Stop_list()
cl2 = Car_list()
sl2.append(Stoplight(point_conv(6.2702815345312,0.383241112322), first = True))
sl2.append(Stoplight(point_conv(6.3273454655618,-0.3134286624478)))
sl2.append(Stoplight(point_conv(6.4838530928216,-3.5462890847714), red = True, fake = False))
sl2.append(Stoplight(point_conv(6.5154798332493,-4.3102801564131)))
sl2.append(Stoplight(point_conv(6.5850245557927,-5.0542884075651)))
sl2.append(Stoplight(point_conv(6.6564253912464,-5.7694438619)))
sl2.append(Stoplight(point_conv(6.6911919028883,-6.2221292256159)))
sl2.append(Stoplight(point_conv(6.7247212460493,-7.2245105271871)))
sl2.append(Stoplight(point_conv(6.8327483656823,-10.0795428367535)))
sl2.append(Stoplight(point_conv(6.855268092129,-10.9888975673), last = True))
stl.append(sl2)
cal.append(cl2)

sl3 = Stop_list()
cl3 = Car_list()
sl3.append(Stoplight(point_conv(-0.5527340561054,-3.3493526113687), first = True))
sl3.append(Stoplight(point_conv(0.0623327235562,-3.6568860011995)))
sl3.append(Stoplight(point_conv(3.6162345714634,-5.1395906086797)))
sl3.append(Stoplight(point_conv(5.36420836424,-5.6743050384899), fake = False))
sl3.append(Stoplight(point_conv(6.2376031913596,-5.7604143876426)))
sl3.append(Stoplight(point_conv(7.2595890988185,-5.7522480204051)))
sl3.append(Stoplight(point_conv(8.0536728572808,-5.7443761636861)))
sl3.append(Stoplight(point_conv(13.1916475165768,-5.793333661)))
sl3.append(Stoplight(point_conv(14.647289039332,-5.8176163982), last = True))
stl.append(sl3)
cal.append(cl3)

sl4 = Stop_list()
cl4 = Car_list()
sl4.append(Stoplight(point_conv(14.6412658403626,-4.9979757561654), first = True))
sl4.append(Stoplight(point_conv(14.0354126046239,-4.9917068968246)))
sl4.append(Stoplight(point_conv(8.2104153812989,-4.9138054453419), fake = False))
sl4.append(Stoplight(point_conv(7.1424023471738,-4.9614702896462)))
sl4.append(Stoplight(point_conv(6.5197680946937,-4.9725887584405)))
sl4.append(Stoplight(point_conv(5.5191059032077,-4.9169964144691)))
sl4.append(Stoplight(point_conv(4.0247345545107,-4.4315570320057)))
sl4.append(Stoplight(point_conv(2.2833441826018,-3.7828990624901)))
sl4.append(Stoplight(point_conv(0.6330931851997,-3.084519798628)))
sl4.append(Stoplight(point_conv(-0.4361206568454,-2.6355857151185), last = True))
stl.append(sl4)
cal.append(cl4)
