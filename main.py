import qr_code_creator
import sys
from ast import literal_eval
import climage

def exit():
    # delete output and input files -> or remember user
    # ...
    # now exit
    sys.exit()

def get_input(msg:str):
    user_input = input(msg)

    if user_input == "exit":
        exit()
    else:
        return user_input

def get_input_between(msg, min, max, type_):
    wrong_input = True

    while wrong_input:
        user_input = get_input(msg)
        try:
            value = type_(user_input)
            if value >= min and value <= max:
                wrong_input = False
        except ValueError:
            pass

    return value

def get_input_color(msg:str):
    not_a_color = True

    while not_a_color:
        user_input = get_input(msg)
        if not (user_input.startswith("(") or user_input.startswith("[")):
            user_input = f"({user_input})"

        if not ("," in user_input):
            user_input = user_input.replace(" ", ",")

        try:
            color = literal_eval(user_input)
            if type(color) == tuple or type(color) == list:
                check = True
                for i in color:
                    if i <= 255 and i >= 0:
                        check = False
                if check:
                    not_a_color = False
        except ValueError:
            pass
    return color
        

    return user_input

def get_input_key(msg:str, keys:list):
    user_input = get_input(msg)

    while user_input not in keys:
        user_input = get_input(msg)

    return user_input

def change_and_show(qr_code):
    while True:
        print("\nYou find the QR-Code in the output directory and can downloaded there.\n")
        qr_code.create_qr_code()
        qr_code.save("./output")

        print("\n\nQR-Code Preview:\n")
        output = climage.convert('./output/output.png', width=40, is_256color=True)
        print(output)

        msg = "Do you want to change something? [content, size, fill_color, back_color, box_size, type, color mask, no]:"
        choice = get_input_key(msg, ['content', 'size', 'fill_color', 'back_color', 'box_size', 'type', 'color mask', 'no'])
        if choice == "content":
            content = get_input("Type the Content which the QR-Code should contains:")
            qr_code.set_content(content)
        elif choice == 'no':
            print("Nice, your QR-Code is in the ouput directory.")
            break
        elif choice == 'size':
            msg = "Type a number from 1 to 40:"
            val = get_input_between(msg, 1, 40, int)
            qr_code.set_size(val)
        elif choice in ['box_size', 'box size', 'box-size']:
            msg = "Type a number bigger than 1:"
            val = get_input_between(msg, 1, 10000000, int)
            qr_code.set_box_size(val)
        elif choice == 'fill_color':
            msg = "Type a color with 3 values (rgb), like (255, 255, 255):"
            val = get_input_color(msg)
            qr_code.set_fill_color(val)
        elif choice == 'back_color':
            msg = "Type a color with 3 values (rgb), like (255, 255, 255):"
            val = get_input_color(msg)
            qr_code.set_background_color(val)
        elif choice == 'type':
            msg = "Type square, rounded, circle, gapped square, vertical bar or horizontal bar:"
            val = get_input_key(msg, ['off', 'square', 'rounded', 'circle', 'gapped square', 'vertical bar', 'horizontal bar'])
            qr_code.set_draw_type(val)
        elif choice in ['mask', 'color mask', 'color_mask']:
            msg = "Type :"
            mask_val = get_input_key(msg, ["solid fill", "square gradient", "radial gradient"\
                                            "horizontal gradient", "vertical gradient"])

            msg = "Type a color for front with 3 values (rgb), normal is (255, 255, 255):"
            color_front_val = get_input_color(msg)

            msg = "Type a color for background with 3 values (rgb), normal is (0,0,0)):"
            color_back_val = get_input_color(msg)

            qr_code.set_color_mask(mask_val, color_front_val, color_back_val)
        #elif choice == 'use image':
        #    msg = "Upload an image in the input directory with named as input. Which type is it (png/...):"
        #    val = get_input(msg)
        #    qr_code.set_image_back(img_type=val)

        
        qr_code.save(path="./output")


if __name__ == "__main__":
    #msg = "Do you want to create a QR-Code or read one? Type create or read:"
    #choice = get_input_key(msg, ['create', 'read'])

    #if choice == 'create':
    content = get_input("Type the Content which the QR-Code should contains:")
    qr_code = qr_code_creator.QR_Code(content)
    change_and_show(qr_code)
    #elif 'read':
    #    pass
