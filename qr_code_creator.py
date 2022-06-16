import qrcode
#import cv2

# for styles
from qrcode.image.styledpil import StyledPilImage

from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.moduledrawers import SquareModuleDrawer
from qrcode.image.styles.moduledrawers import GappedSquareModuleDrawer
from qrcode.image.styles.moduledrawers import CircleModuleDrawer
from qrcode.image.styles.moduledrawers import VerticalBarsDrawer
from qrcode.image.styles.moduledrawers import HorizontalBarsDrawer

from qrcode.image.styles.colormasks import SolidFillColorMask
from qrcode.image.styles.colormasks import SquareGradiantColorMask
from qrcode.image.styles.colormasks import RadialGradiantColorMask
from qrcode.image.styles.colormasks import HorizontalGradiantColorMask
from qrcode.image.styles.colormasks import VerticalGradiantColorMask
#from qrcode.image.styles.colormasks import ImageColorMask

import random


class QR_Code(object):

    def __init__(self, content:str, front_color=(0,0,0), background_color=(255,255,255), border=4, size=1, box_size=10, \
                                    draw_type=SquareModuleDrawer(), mask=SolidFillColorMask(front_color=(0,0,0), \
                                    back_color=(255,255,255)), center_color=(0,0,0), \
                                    edge_color=(0, 0, 255), left_color=(0, 0, 0), right_color=(0, 0, 255), \
                                    top_color=(0, 0, 0), bottom_color=(0, 0, 255),img_back=False):

        if type(content) == str and len(content) > 0:
            self.content = content
            self.front_color = front_color
            self.background_color = background_color
            self.border = border
            self.size = size
            self.box_size = box_size
            self.draw_type = draw_type
            self.mask = mask
            self.img_back = img_back

            self.img_type = "jpg"
        else:
            raise ValueError("The given content isn't valuable for the QR-Code!")

    def __del__(self):
        self.reset()

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.reset()

    def set_front_color(self, front_color):
        if type(self.mask) == SolidFillColorMask:
            self.front_color = front_color
            self.mask = SolidFillColorMask(front_color=front_color, back_color=self.background_color)
        elif type(self.mask) == SquareGradiantColorMask:
            self.center_color = front_color
            self.mask = SquareGradiantColorMask(back_color=self.background_color, center_color=front_color, edge_color=self.edge_color)
        elif type(self.mask) == RadialGradiantColorMask:
            self.center_color = front_color
            self.mask = RadialGradiantColorMask(back_color=self.background_color, center_color=front_color, edge_color=self.edge_color)
        elif type(self.mask) == HorizontalGradiantColorMask:
            self.left_color = front_color
            self.mask = HorizontalGradiantColorMask(back_color=self.background_color, left_color=front_color, right_color=self.right_color)
        elif type(self.mask) == VerticalGradiantColorMask:
            self.top_color = front_color
            self.mask = VerticalGradiantColorMask(back_color=self.background_color, top_color=front_color, bottom_color=self.bottom_color)

    def set_background_color(self, background_color):
        self.background_color = background_color

        if type(self.mask) == SolidFillColorMask:
            self.mask = SolidFillColorMask(front_color=self.front_color, back_color=self.background_color)
        elif type(self.mask) == SquareGradiantColorMask:
            self.mask = SquareGradiantColorMask(back_color=self.background_color, center_color=self.center_color, edge_color=self.edge_color)
        elif type(self.mask) == RadialGradiantColorMask:
            self.mask = RadialGradiantColorMask(back_color=self.background_color, center_color=self.center_color, edge_color=self.edge_color)
        elif type(self.mask) == HorizontalGradiantColorMask:
            self.mask = HorizontalGradiantColorMask(back_color=self.background_color, left_color=self.left_color, right_color=self.right_color)
        elif type(self.mask) == VerticalGradiantColorMask:
            self.mask = VerticalGradiantColorMask(back_color=self.background_color, top_color=self.top_color, bottom_color=self.bottom_color)

    def set_border(self, border):
        self.border = border
        self.create_qr_code()

    def set_size(self, size):
        self.size = size
        self.create_qr_code()

    def set_box_size(self, box_size):
        self.box_size = box_size
        self.create_qr_code()

    def set_color_mask(self, mask, front_color=(0,0,0), back_color=(255,255,255), center_color=(0,0,0), \
                                    edge_color=(0, 0, 255), left_color=(0, 0, 0), right_color=(0, 0, 255), \
                                    top_color=(0, 0, 0), bottom_color=(0, 0, 255)):
        if mask == 'off':
            self.mask = SolidFillColorMask(front_color=front_color, back_color=back_color)
        elif mask == "solid fill":
            self.front_color = front_color
            self.background_color = back_color
            self.mask = SolidFillColorMask(front_color=front_color, back_color=back_color)
        elif mask == "square gradient":
            self.center_color = center_color
            self.edge_color = edge_color
            self.background_color = back_color
            self.mask = SquareGradiantColorMask(back_color=back_color, center_color=center_color, edge_color=edge_color)
        elif mask == "radial gradient":
            self.center_color = center_color
            self.edge_color = edge_color
            self.background_color = back_color
            self.mask = RadialGradiantColorMask(back_color=back_color, center_color=center_color, edge_color=edge_color)
        elif mask in ["horizontal gradient", "horizontal"]:
            self.left_color = left_color
            self.right_color = right_color
            self.background_color = back_color
            self.mask = HorizontalGradiantColorMask(back_color=back_color, left_color=left_color, right_color=right_color)
        elif mask in ["vertical gradient", "vertical"]:
            self.top_color = top_color
            self.bottom_color = bottom_color
            self.background_color = back_color
            self.mask = VerticalGradiantColorMask(back_color=back_color, top_color=top_color, bottom_color=bottom_color)
        else:
            raise ValueError('Dont know this color mask')
        #elif mask == "image":
        #    self.mask = ImageColorMask(front_color=front_color, back_color=back_color)

    def set_image_back(self, img_type="jpg"):
        self.img_type = img_type
        self.img_back = True

    def set_draw_type(self, draw_type:str):
        if draw_type == "square":
            self.draw_type = SquareModuleDrawer()
        elif draw_type == "rounded":
            self.draw_type = RoundedModuleDrawer()
        elif draw_type in ["gapped square", "gapped_square"]:
            self.draw_type = GappedSquareModuleDrawer()
        elif draw_type == "circle":
            self.draw_type = CircleModuleDrawer()
        elif draw_type == "vertical bar":
            self.draw_type = VerticalBarsDrawer()
        elif draw_type == "horizontal bar":
            self.draw_type = HorizontalBarsDrawer()

    def set_content(self, content):
        self.content = content
        self.create_qr_code()

    def reset(self):
        self.front_color=(0,0,0)
        self.background_color=(255,255,255)
        self.border=4
        self.size=1
        self.box_size=10
        self.draw_type=SquareModuleDrawer()
        self.mask=SolidFillColorMask(front_color=(0,0,0), back_color=(255,255,255))
        self.center_color=(0,0,0)
        self.edge_color=(0, 0, 255)
        self.left_color=(0, 0, 0)
        self.right_color=(0, 0, 255)
        self.top_color=(0, 0, 0)
        self.bottom_color=(0, 0, 255)
        self.img_back=False

    def create_qr_code(self):
        self.created_qr_code = qrcode.QRCode(border=self.border, version=self.size, box_size=self.box_size)
        self.created_qr_code.add_data(self.content)
        #self.created_qr_code.make(fit=True)

    # static
    def random_color():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def random_creation(self):
        self.front_color = QR_Code.random_color() 
        self.background_color = QR_Code.random_color()
        self.center_color = QR_Code.random_color()
        self.edge_color = QR_Code.random_color()
        self.left_color = QR_Code.random_color()
        self.right_color = QR_Code.random_color()
        self.top_color = QR_Code.random_color()
        self.bottom_color = QR_Code.random_color()

        self.draw_type  = random.choice([SquareModuleDrawer(), RoundedModuleDrawer(), GappedSquareModuleDrawer(), \
                                        CircleModuleDrawer(), VerticalBarsDrawer(), HorizontalBarsDrawer()])

        self.mask = random.choice([
                                SolidFillColorMask(front_color=self.front_color, back_color=self.background_color), 
                                SquareGradiantColorMask(back_color=self.background_color, center_color=self.center_color, edge_color=self.edge_color),
                                RadialGradiantColorMask(back_color=self.background_color, center_color=self.center_color, edge_color=self.edge_color),
                                HorizontalGradiantColorMask(back_color=self.background_color, left_color=self.left_color, right_color=self.right_color),
                                VerticalGradiantColorMask(back_color=self.background_color, top_color=self.top_color, bottom_color=self.bottom_color)
                                    ])
    

        # not randomized yet
        # border=4, size=1, box_size=10
                                    

    def save(self, path:str, name="output.png", img_path="./input", img_name="input"):
        if not hasattr(self, 'created_qr_code'):
            self.create_qr_code()

        if self.img_back == True:
            self.img = self.created_qr_code.make_image(fill_color=self.front_color, back_color=self.background_color, \
                                                        image_factory=StyledPilImage, color_mask=self.mask, module_drawer=self.draw_type, embeded_image_path=img_path+"/"+img_name+"."+self.img_type)
        else:
           self.img = self.created_qr_code.make_image(fill_color=self.front_color, back_color=self.background_color, \
                                                        image_factory=StyledPilImage, module_drawer=self.draw_type, color_mask=self.mask)

        self.img.save(path+"/"+name)

    # static
    #def get_content_from_qr_code(path_with_filename:str):
    #    qr_reader = cv2.QRCodeDetector()
    #    value, points, qrcode_ = qr_reader.detectAndDecode(cv2.imread(path_with_filename))
    #    return value


