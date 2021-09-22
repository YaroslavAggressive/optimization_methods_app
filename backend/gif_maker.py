import imageio
import os
import datetime

RES_GIF_NAME = "graphic_gif"
RES_IMAGE_PREFIX = "image_for_gif_"
GIF_OPTIONS = {'duration': 1}  # constantly set duration of result gif
DEFAULT_DIRECTORY = "C:/"
PATH_DELIMITER = "//"
GIF_FORMAT = ".gif"
EMPTY_STR = ""


class GifMaker:

    """
    Class with methods for creating gif-result of minimization process of application
    """

    @staticmethod
    def create_result_dir_and_idx(dir_name: str = EMPTY_STR) -> int:

        """
        Function for creating graph result directory and its index

        Parameters:
        ----------
        dir_name: str
            Name of result folder

        Returns:
        -------
            Index of result directory for current image (for gif creation in future)
        """

        tmp_path = DEFAULT_DIRECTORY
        result_idx = 0
        while os.path.isdir(tmp_path):
            result_idx = int(datetime.datetime.now().timestamp())
            tmp_path = dir_name + PATH_DELIMITER + RES_IMAGE_PREFIX + str(result_idx)
        os.mkdir(tmp_path)
        return result_idx

    @staticmethod
    def create_gif_result(filenames: list = [], dir_name: str = EMPTY_STR) -> str:

        """
        Method for creating GIF animation from a set of images with recording the result in the required directory

        Parameters:
        ----------
        filenames: list
            List of images used to build the animation
        dir_name: str
            Name of the directory, the result is saved

        Returns:
        -------
            Name of gif-result of optimization process
        """

        images = []
        for filename in filenames:
            images.append(imageio.imread(filename))
        # check, that there is no test with such number
        result_path = dir_name + PATH_DELIMITER + RES_GIF_NAME
        if not os.path.isdir(result_path):
            # save it to the working directory and send it back to the program
            imageio.mimsave(result_path + GIF_FORMAT, images,
                            'GIF', **GIF_OPTIONS)
        else:
            raise NameError("such gif-file named <" + RES_GIF_NAME + "> already exists")  ####

        return result_path + GIF_FORMAT

    @staticmethod
    def clear_temp_images(folder_name: str = EMPTY_STR):

        """
        Method for cleaning the current directory from all files
         (in particular, it was created to remove intermediate images created for the resulting GIF animation)

        Parameters:
        ----------
        folder_name: str
            Name of the directory to be cleared

        Returns:
        -------
            None just for now
        """

        for file in os.listdir(folder_name):
            os.remove(os.path.join(folder_name, file))

    @staticmethod
    def check_images_folder(folder_name: str = ""):

        """
        Method for checking a directory before filling it with temporary files

        Parameters:
        ----------
        folder_name: str
            Name of the folder, the presence and emptiness of which you want to check
        """

        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        else:
            GifMaker.clear_temp_images(folder_name)
