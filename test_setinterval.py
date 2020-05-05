import threading
import random


# code from http://stackoverflow.com/a/14035296/4592067
def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


# roll a die every 3 seconds
# cancel the timer once we roll a "6"
def roll6():
	roll = random.randint(1, 6)
	print("You rolled: " + str(roll))
	if roll == 6:
		timer.cancel() # doesn't seem to cancel though
		print("Finally, a 6! We can stop rolling.")

# set up the timer
timer = set_interval(roll6, 3)