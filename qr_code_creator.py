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


class QR_Code(object):

    def __init__(self, content:str, fill_color='black', background_color='white', border=4, size=1, box_size=10, \
                                    draw_type=SquareModuleDrawer(), mask=SolidFillColorMask(front_color=(0,0,0), back_color=(255,255,255)), img_back=False):
        if type(content) == str and len(content) > 0:
            self.content = content
            self.fill_color = fill_color
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

    def set_fill_color(self, fill_color):
        self.fill_color = fill_color

    def set_backgound_color(self, background_color):
        self.background_color = background_color

    def set_border(self, border):
        self.border = border
        self.create_qr_code()

    def set_size(self, size):
        self.size = size
        self.create_qr_code()

    def set_box_size(self, box_size):
        self.box_size = box_size
        self.create_qr_code()

    def set_color_mask(self, mask, front_color=(0,0,0), back_color=(255,255,255)):
        if mask == 'off':
            self.mask = SolidFillColorMask(front_color=(0,0,0), back_color=(255,255,255))
        elif mask == "solid fill":
            self.mask = SolidFillColorMask(front_color=front_color, back_color=back_color)
        elif mask == "square gradient":
            self.mask = SquareGradiantColorMask(front_color=front_color, back_color=back_color)
        elif mask == "radial gradient":
            self.mask = RadialGradiantColorMask(front_color=front_color, back_color=back_color)
        elif mask == "horizontal gradient":
            self.mask = HorizontalGradiantColorMask(front_color=front_color, back_color=back_color)
        elif mask == "vertical gradient":
            self.mask = VerticalGradiantColorMask(front_color=front_color, back_color=back_color)
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

    def set_content(content):
        self.content = content
        self.create_qr_code()

    def create_qr_code(self):
        self.created_qr_code = qrcode.QRCode(border=self.border, version=self.size, box_size=self.box_size)
        self.created_qr_code.add_data(self.content)
        #self.created_qr_code.make(fit=True)

    def save(self, path:str, name="output.png", img_path="./input", img_name="input"):
        if self.img_back == True:
            self.img = self.created_qr_code.make_image(fill_color=self.fill_color, back_color=self.background_color, image_factory=StyledPilImage, color_mask=self.mask, \
                                                                    module_drawer=self.draw_type, embeded_image_path=img_path+"/"+img_name+"."+self.img_type)
        else:
           self.img = self.created_qr_code.make_image(fill_color=self.fill_color, back_color=self.background_color, image_factory=StyledPilImage, \
                                                                    module_drawer=self.draw_type, color_mask=self.mask) 

        self.img.save(path+"/"+name)

    # static
    #def get_content_from_qr_code(path_with_filename:str):
    #    qr_reader = cv2.QRCodeDetector()
    #    value, points, qrcode_ = qr_reader.detectAndDecode(cv2.imread(path_with_filename))
    #    return value


