#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configargparse

import cv2 as cv


from gestures import *


def get_args():
    print('## Reading configuration ##')
    parser = configargparse.ArgParser(default_config_files=['config.txt'])

    parser.add('-c', '--my-config', required=False, is_config_file=True, help='config file path')
    parser.add("--device", type=int)
    parser.add("--width", help='cap width', type=int)
    parser.add("--height", help='cap height', type=int)
    parser.add("--is_keyboard", help='To use Keyboard control by default', type=bool)
    parser.add('--use_static_image_mode', action='store_true', help='True if running on photos')
    parser.add("--min_detection_confidence",
               help='min_detection_confidence',
               type=float)
    parser.add("--min_tracking_confidence",
               help='min_tracking_confidence',
               type=float)
    parser.add("--buffer_len",
               help='Length of gesture buffer',
               type=int)
    parser.add("--min_no_hands_frames_for_word_break",
               help='Number of frames with no hands detected to recognize a break in words',
               type=int)
    parser.add("--min_consecutive_letters_recognized",
               help='Number of consecutive frames with the same letter needed to recognized that as a letter in the current word',
               type=int)

    args = parser.parse_args()

    return args


def select_mode(key, mode):
    number = -1
    if 48 <= key <= 57:  # 0 ~ 9
        number = key - 48
    if key == 110:  # n
        mode = 0
    if key == 107:  # k
        mode = 1
    if key == 104:  # h
        mode = 2
    return number, mode


def main():
    # init global vars
    global gesture_buffer
    global gesture_id
    global battery_status

    # Argument parsing
    args = get_args()
    WRITE_CONTROL = False

    """
    # Camera preparation
    tello = Tello()
    tello.connect()
    tello.streamon()

    cap = tello.get_frame_read()

    # Init Tello Controllers
    gesture_controller = TelloGestureController(tello)
    keyboard_controller = TelloKeyboardController(tello)
"""
    gesture_detector = GestureRecognition(args.use_static_image_mode, args.min_detection_confidence,
                                          args.min_tracking_confidence, 16, args.min_consecutive_letters_recognized, args.min_no_hands_frames_for_word_break)
    gesture_buffer = GestureBuffer(buffer_len=args.buffer_len)
    cap = cv.VideoCapture(0)


    mode = 0
    number = -1

    while True:

        # Process Key (ESC: end)
        key = cv.waitKey(1) & 0xff
        if key == 27:  # ESC
            break
        elif key == ord('n'):
            mode = 1
            WRITE_CONTROL = True
            KEYBOARD_CONTROL = True

        if WRITE_CONTROL:
            number = -1
            first_dig = -1
            sec_dig = -1
            if 48 <= key <= 57:  # 0 ~ 9
                first_dig = key-48  
                key2 = cv.waitKey(5000) & 0xff  
                if 48 <= key2 <= 57:  # 0 ~ 9
                    sec_dig = key2-48
                    number = int(str(first_dig) + str(sec_dig))
                    print(number)
                else:
                    #todo: print "invalid number if second dig is invalid?"
                    number = first_dig


        # Camera capture
        success, image = cap.read()
        debug_image, gesture_id = gesture_detector.recognize(image, number, mode)
        gesture_buffer.add_gesture(gesture_id)

        debug_image = gesture_detector.draw_info(debug_image, mode, number)

        # Battery status and image rendering
        cv.imshow('ASL Letter Recognition', debug_image)

    cv.destroyAllWindows()

if __name__ == '__main__':
    main()
