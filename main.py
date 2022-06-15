import qr_code_creator
import sys
from ast import literal_eval
import climage
import os

def exit(qr_code):
    if qr_code == None:
        sys.exit()
    else:
        # delete output and input files -> or remember user
        choice = get_input_key("Do you want your QR Code saved in backup?(y/n or nothing to skip):", ['n', 'y', ''], qr_code)
        if choice == 'y':
            # calc name
            files = os.listdir("./backup")
            counter = 0
            name = f"qrcode_{str(counter).zfill(4)}.png"    # variant 1
            while name in files:
                counter += 1
                name = f"qrcode_{counter:04}.png"

            qr_code.save(path="./backup", name=name)
        elif choice in ['n', '']:
            pass
        elif choice in ['clear']:
            files = os.listdir("./backup")
            for file in files:
                os.remove("./backup"+file)

        qr_code = qr_code_creator.QR_Code("make love not fear", front_color=(240, 70, 50), background_color=(40, 20, 20))
        qr_code.save(path="./output")

        # now exit
        sys.exit()

def get_input(msg:str, qr_code):
    user_input = input(msg)

    if user_input == "exit":
        exit(qr_code)
    else:
        return user_input

def get_input_between(msg, min, max, type_, qr_code):
    wrong_input = True

    while wrong_input:
        user_input = get_input(msg, qr_code)
        try:
            value = type_(user_input)
            if value >= min and value <= max:
                wrong_input = False
        except ValueError:
            pass

    return value

def get_input_color(msg:str, qr_code):
    not_a_color = True

    while not_a_color:
        user_input = get_input(msg, qr_code)
        if not user_input.startswith("(") and not user_input.startswith("["):
            user_input = f"({user_input})"

        if not "," in user_input:
            user_input = user_input.replace(" ", ",")

        try:
            color = literal_eval(user_input)
            if (type(color) == tuple or type(color) == list) and len(color) == 3:
                check = True
                for i in color:
                    if i > 255 and i < 0:
                        check = False
                if check:
                    not_a_color = False
        except ValueError:
            pass
    return color
        

    return user_input

def get_input_key(msg:str, keys:list, qr_code):
    user_input = get_input(msg, qr_code)

    while user_input not in keys:
        user_input = get_input(msg, qr_code)

    return user_input

def change_and_show(qr_code):
    while True:
        print("\nYou find the QR-Code in the output directory and can downloaded there.\n")
        qr_code.create_qr_code()
        qr_code.save("./output")

        print("\n\nQR-Code Preview:\n")
        output = climage.convert('./output/output.png', width=60, is_256color=False, is_truecolor=True, is_unicode=True)
        print(output)

        msg = "Do you want to change something? [content, size, fill_color, back_color, box_size, type, color mask, no]:"
        choice = get_input_key(msg, ['content', 'size', 'fill_color', 'back_color', 'box_size', 'type', 'color mask', 'mask', 'no'], qr_code)
        if choice == "content":
            content = get_input("Type the Content which the QR-Code should contains:", qr_code)
            qr_code.set_content(content)
        elif choice == 'no':
            print("Nice, your QR-Code is in the ouput directory.")
            exit(qr_code)
        elif choice == 'size':
            msg = "Type a number from 1 to 40:"
            val = get_input_between(msg, 1, 40, int, qr_code)
            qr_code.set_size(val)
        elif choice in ['box_size', 'box size', 'box-size']:
            msg = "Type a number bigger than 1:"
            val = get_input_between(msg, 1, 10000000, int, qr_code)
            qr_code.set_box_size(val)
        elif choice == 'fill_color':
            msg = "Type a color with 3 values (rgb), like (255, 255, 255):"
            val = get_input_color(msg, qr_code)
            qr_code.set_front_color(val)
        elif choice == 'back_color':
            msg = "Type a color with 3 values (rgb), like (255, 255, 255):"
            val = get_input_color(msg, qr_code)
            qr_code.set_background_color(val)
        elif choice == 'type':
            msg = "Type square, rounded, circle, gapped square, vertical bar or horizontal bar:"
            val = get_input_key(msg, ['off', 'square', 'rounded', 'circle', 'gapped square', 'vertical bar', 'horizontal bar'], qr_code)
            qr_code.set_draw_type(val)
        elif choice in ['mask', 'color mask']:
            msg = "Type solid fill, square gradient, radial gradient, horizontal or vertical:"
            mask_val = get_input_key(msg, ["solid fill", "square gradient", "radial gradient", \
                                            "horizontal gradient", "horizontal", "vertical gradient", "vertical"], qr_code)

            if mask_val == 'off':
                qr_code.set_color_mask(mask_val)
            elif mask_val == "solid fill":
                msg = "Type a color for front with 3 values (rgb), normal is (0,0,0):"
                color_front_val = get_input_color(msg, qr_code)

                msg = "Type a color for background with 3 values (rgb), normal is (255,255,255)):"
                color_back_val = get_input_color(msg, qr_code)

                qr_code.set_color_mask(mask_val, front_color=color_front_val,back_color=color_back_val)
            elif mask_val in ["radial gradient", "square gradient"]:
                msg = "Type a color for the center with 3 values (rgb), normal is (255, 255, 255):"
                color_center_val = get_input_color(msg, qr_code)

                msg = "Type a color for the edge/limit with 3 values (rgb), normal is (0, 0, 255):"
                color_edge_val = get_input_color(msg, qr_code)

                msg = "Type a color for the background with 3 values (rgb), normal is (255,255,255)):"
                color_back_val = get_input_color(msg, qr_code)

                qr_code.set_color_mask(mask_val, center_color=color_center_val, edge_color=color_edge_val, back_color=color_back_val)
            elif mask_val in ["horizontal gradient", "horizontal"]:
                msg = "Type a color for the left with 3 values (rgb), normal is (0,0,0):"
                color_left_val = get_input_color(msg, qr_code)

                msg = "Type a color for the right with 3 values (rgb), normal is (0, 0, 255):"
                color_right_val = get_input_color(msg, qr_code)

                msg = "Type a color for the background with 3 values (rgb), normal is (255,255,255)):"
                color_back_val = get_input_color(msg, qr_code)

                qr_code.set_color_mask(mask_val, left_color=color_left_val, right_color=color_right_val, back_color=color_back_val)
            elif mask_val in ["vertical gradient", "vertical"]:
                msg = "Type a color for the top with 3 values (rgb), normal is (0,0,0):"
                color_top_val = get_input_color(msg, qr_code)

                msg = "Type a color for the bottom with 3 values (rgb), normal is (0, 0, 255):"
                color_bottom_val = get_input_color(msg, qr_code)

                msg = "Type a color for the background with 3 values (rgb), normal is (255,255,255)):"
                color_back_val = get_input_color(msg, qr_code)

                qr_code.set_color_mask(mask_val, top_color=color_top_val, bottom_color=color_bottom_val, back_color=color_back_val)

        #elif choice == 'use image':
        #    msg = "Upload an image in the input directory with named as input. Which type is it (png/...):"
        #    val = get_input(msg)
        #    qr_code.set_image_back(img_type=val)

        
        qr_code.save(path="./output")


if __name__ == "__main__":
    #msg = "Do you want to create a QR-Code or read one? Type create or read:"
    #choice = get_input_key(msg, ['create', 'read'])

    #if choice == 'create':
    content = get_input("Type the Content which the QR-Code should contains:", None)
    qr_code = qr_code_creator.QR_Code(content)
    change_and_show(qr_code)
    #elif 'read':
    #    pass
