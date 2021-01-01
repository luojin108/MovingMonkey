
from tkinter import *
import time
import random

# Constants
MONKEY_DEFAULT_POSITION = [15,
                           250]  # The position where the monkey first enter.
MOVEMENT_DISTANCE = 5  # The distance the monkey moves at a time
GAME_NAME = "Big Monkey"  # Name of the game


class BigMonkey:
    """
    Game name: Big Monkey
    In this game, a monkey is looking for bananas, which randomly appear
     on the map. Every time a banana is collected, one point is awarded.
     Meanwhile, a stone will be dropped on the map randomly. The game ends
     when the monkey hits either the edge or the stone. Press "Enter" or
     the soft key "Start" to start the game.You can control the monkey
     using both the keyboard or the soft key. Pressing "Enter" also enables
     restart of the game.

    """

    def __init__(self):
        """
        Constructor in which all the needed widgets, UI components and
         attributes are created.
        """
        self.window = Tk()
        self.window.geometry("500x600")
        self.window.resizable(0, 0)  # The window size is not changeable.

        # Create objects of the needed UI components and widgets.
        self.control_panel = Frame(self.window, width=500, height=100,
                                   bg="white")
        self.canvas = Canvas(width=500, height=500, bg='green')
        self.score_label = Label(self.control_panel, text="Score: ",
                                 bg="white")
        self.highest_score_label = Label(self.control_panel,
                                         text="Highest score: ", bg="white")
        self.current_score_text = Label(self.control_panel, text=0, bg="white")
        self.highest_score_text = Label(self.control_panel, text=0, bg="white")
        self.start_button = Button(self.control_panel, text="Start",
                                   bg="orange", command=self.init_game)
        self.stop_button = Button(self.control_panel, text="Quit", bg="orange",
                                  command=self.quit)
        self.move_up_button = Button(self.control_panel, text="↑", height=1,
                                     width=3, bg="orange",
                                     command=self.move_up)
        self.move_right_button = Button(self.control_panel, text="→", height=1,
                                        width=3, bg="orange",
                                        command=self.move_right)
        self.move_down_button = Button(self.control_panel, text="↓", height=1,
                                       width=3, bg="orange",
                                       command=self.move_down)
        self.move_left_button = Button(self.control_panel, text="←", height=1,
                                       width=3, bg="orange",
                                       command=self.move_left)

        # Import the images needed for the game.
        self.monkey_image = PhotoImage(file="moving_monkey.png")
        self.banana_image = PhotoImage(file="banana_image.png")
        self.barrier_image = PhotoImage(file="barrier_image.png")
        self.open_image_monkey = PhotoImage(file="monkey.png")
        self.failure_image_monkey = PhotoImage(file="dizzy_monkey.png")

        # Add image to the canvas as the open image
        self.welcome_image = self.canvas.create_image(250, 250,
                                                      image=self.open_image_monkey)
        # Create object of the game components, but not initialize them yet.
        self.moving_monkey = None
        self.banana = None
        self.barrier = None
        self.failure_image = None

        self.location_list = []  # A list containing all the coordinates
        # that banana can appear

        self.barrier_location_list = []  # A list containing the coordinates
        # that the barriers are in.

        self.x_moving_vector = MOVEMENT_DISTANCE  # Vector of monkey's movement
        # at x axis.

        self.y_moving_vector = 0  # Vector of monkey's movement at y axis

        self.score = 0  # The current score which is updated in real time
        self.highest_score = 0  # The highest score which is updated after each
        # game

        self.init_location_list()  # initialize the location list
        self.init_widgets()  # initialize all the widgets and UI components
        self.bind_keyboard()  # Bind keyboard so that the keyboard can be used
        # to control the monkey.

        self.window.mainloop()

    def remove_welcome_image(self):
        """
        Function used to remove the welcome image (an image of the big monkey)
        """
        self.canvas.delete(self.welcome_image)

    def init_widgets(self):
        """
        Initialize all the UI components and widgets
        """
        # Change the title and icon of the application.
        self.window.iconphoto(False, self.monkey_image)
        self.window.title(GAME_NAME)

        #  Designate the position of each widget and component.
        self.score_label.place(relx=0.2, rely=0.5)
        self.highest_score_label.place(relx=0.2, rely=0.2)
        self.current_score_text.place(relx=0.28, rely=0.5)
        self.highest_score_text.place(relx=0.36, rely=0.2)
        self.start_button.place(relx=0.05, rely=0.1)
        self.stop_button.place(relx=0.05, rely=0.5)
        self.move_up_button.place(relx=0.8, rely=0)
        self.move_right_button.place(relx=0.88, rely=0.32)
        self.move_down_button.place(relx=0.8, rely=0.65)
        self.move_left_button.place(relx=0.72, rely=0.32)
        self.control_panel.pack(side=BOTTOM)
        self.canvas.pack(side=TOP)

    def init_location_list(self):
        """
        Populate the location list with all the possible coordinates that
        bananas may appear.
        """
        #  The size of the canvas is 500x500. The coordinate start from (20,20)
        # to (495,495) with increment of 5 for each axis
        for x_position in range(20, 495, 5):
            for y_position in range(20, 495, 5):
                location = [x_position, y_position]
                self.location_list.append(location)

    def bind_keyboard(self):
        """
        Bind the keyboard with the direction control function so that the
        keyboard can be used to control the monkey.
        """
        self.window.bind('<Up>', self.move_up)
        self.window.bind('<Right>', self.move_right)
        self.window.bind('<Down>', self.move_down)
        self.window.bind('<Left>', self.move_left)
        self.window.bind('<Return>', self.init_game)

    def init_game(self, event=None):
        """
        Function used to start or restart the game.
        """
        self.remove_welcome_image()  # Remove the welcome image

        self.reset()  # Reset all the UI and attributes for game restart

        self.moving_monkey = self.canvas.create_image(
            MONKEY_DEFAULT_POSITION[0], MONKEY_DEFAULT_POSITION[1],
            image=self.monkey_image)  # The monkey enters the playground.

        self.init_banana()  # The first banana appears.

        self.default_move()  # The monkey starts to move to search for the
        # banana.

    def reset(self):
        """
        Reset all the UI and attributes for game restart
        """

        #  Reset is effective only if the game is over and the gamer press
        #  start. Reset all the attributes and the current score. Update
        # the highest score
        if self.failure_image is not None:
            self.canvas.delete(ALL)
            self.barrier_location_list = []
            self.location_list = []
            self.init_location_list()
            self.x_moving_vector = MOVEMENT_DISTANCE
            self.y_moving_vector = 0
            if self.score > self.highest_score:
                self.highest_score = self.score
                self.highest_score_text["text"] = self.highest_score
            self.score = 0
            self.current_score_text["text"] = self.score

    def quit(self):
        """
        Quit the game
        """
        self.window.destroy()

    def default_move(self):
        """
        Function enabling the monkey to move and checking whether a banana is
        collected or the monkey collide with the edge or barriers.
        """
        while True:
            self.start_button["state"] = DISABLED  # Disable the start button,
            # but the keyboard is still working for restart.

            monkey_position = self.canvas.coords(self.moving_monkey)  # Get the
            # monkey's position

            # If barrier exists,
            # check if the monkey hit barrier, if yes, game over.
            if self.barrier is not None:
                if self.check_hitting_barrier(monkey_position):
                    break

            # Check if the monkey gets the banana, if yes, update the score,
            # update the banana position, and add a new barrier on the map
            if self.check_eating_banana(monkey_position):
                self.update_score()
                self.init_banana()
                self.init_barrier()

            # Check if the monkey hits the edge, if yes, game over.
            if monkey_position[0] <= 10 or monkey_position[1] <= 10 or \
                    monkey_position[0] >= 490 or monkey_position[1] >= 490:
                break

            self.canvas.move(self.moving_monkey, self.x_moving_vector,
                             self.y_moving_vector)  # Move the monkey according
            # to the moving vector attributes.

            time.sleep(0.01)  # Duration of sleep to control the moving speed.

            self.canvas.update()  # Update the canvas

        # When jumping out of the loop, meaning the game is over, the failure
        # image appears.
        self.init_failure_image()

    def init_banana(self):
        """
        Function used to remove the previous banana which is collected by the
        monkey, and add a new banana on the map at random position
        """

        # If a banana already exists, remove it from the UI
        if self.banana is not None:
            old_banana_location = self.canvas.coords(self.banana)  # The
            # coordinate of the old banana

            self.location_list.append(old_banana_location)  # Add the
            # coordinate of the previous banana to the location list.

            self.canvas.delete(
                self.banana)  # Remove the collected banana from
            # the UI

        new_banana_location = random.choice(self.location_list)  # The
        # coordinate of the new banana.

        self.location_list.remove(new_banana_location)  # Remove the coordinate
        # of the new banana from the location list temporally so that the
        # barrier will appear at the same location ( the location of the
        # barrier is selected from the same list.

        # Create the banana in the UI.
        self.banana = self.canvas.create_image(new_banana_location[0],
                                               new_banana_location[1],
                                               image=self.banana_image)

    def init_barrier(self):
        """
        Initialize the the barrier on the map.
        """

        new_barrier_location = random.choice(self.location_list)  # The
        # location of the barrier.

        self.barrier_location_list.append(new_barrier_location)  # Add the
        # barrier location to the barrier location list.

        self.location_list.remove(new_barrier_location)  # Remove the barrier
        # location from the location list so that the next barrier will not
        # appear at the same location

        self.barrier = self.canvas.create_image(new_barrier_location[0],
                                                new_barrier_location[1],
                                                image=self.barrier_image)

    def init_failure_image(self):
        """
        Initialize the failure image, which will appear after each round of
        game is over.
        """
        self.failure_image = self.canvas.create_image(250, 250,
                                                      image=self.failure_image_monkey)
        self.start_button["state"] = NORMAL

    def move_up(self, event=None):
        """
        Function changing the moving direction up
        :param event: the button pressing event
        """
        self.x_moving_vector = 0
        self.y_moving_vector = -MOVEMENT_DISTANCE

    def move_right(self, event=None):
        """
        Function changing the moving direction right
        :param event: the button pressing event
        """
        self.x_moving_vector = MOVEMENT_DISTANCE
        self.y_moving_vector = 0

    def move_down(self, event=None):
        """
        Function changing the moving direction down
        :param event: the button pressing event
        """
        self.x_moving_vector = 0
        self.y_moving_vector = MOVEMENT_DISTANCE

    def move_left(self, event=None):
        """
        Function changing the moving direction left
        :param event: the button pressing event
        """
        self.x_moving_vector = -MOVEMENT_DISTANCE
        self.y_moving_vector = 0

    def check_eating_banana(self, monkey_position):
        """
        Function checking whether the banana is eaten/collected by the monkey.
        :param monkey_position:
        :return: boolean, whether the banana is eaten/collected by the monkey.
        """
        banana_position = self.canvas.coords(self.banana)  # Position of the
        # banana

        # If the monkey is close enough to the banana, return true
        if banana_position[0] - 20 < monkey_position[0] < banana_position[
            0] + 20 and banana_position[1] - 20 < monkey_position[1] < \
                banana_position[1] + 20:
            return True
        else:
            return False

    def check_hitting_barrier(self, monkey_position):
        """
        Function checking whether the barrier is hit by the monkey.
        :param monkey_position:
        :return: boolean, whether the barrier is hit by the monkey.
        """

        # Check if the monkey is close enough to the barrier by checking if
        # their coordinates are close enough. If so, return true.
        for location in self.barrier_location_list:
            if location[0] - 15 < monkey_position[0] < location[
                0] + 15 and location[1] - 15 < monkey_position[1] < \
                    location[1] + 15:
                return True
        return False

    def update_score(self):
        """
        Update the current score.
        """
        self.score += 1
        self.current_score_text["text"] = self.score


def main():
    BigMonkey()


if __name__ == "__main__":
    main()
