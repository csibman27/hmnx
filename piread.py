from sense_hat import SenseHat

sense = SenseHat()
#sense.clear()


def pi_sense():
        blue = (0, 0, 255)
        yellow = (255, 255, 0)

        while True:
          f = open("outnum", "r")
          i = f.read()
          sense.show_message("%s" % i, scroll_speed = 0.2)

if __name__ == '__main__':
    pi_sense()
