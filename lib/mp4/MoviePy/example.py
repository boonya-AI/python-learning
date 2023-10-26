from skimage.filters import gaussian_filter
from moviepy.editor import VideoFileClip

def blur(image):
    """ Returns a blurred (radius=2 pixels) version of the image """
    return gaussian_filter(image.astype(float), sigma=2)

clip = VideoFileClip("my_video.mp4")
clip_blurred = clip.fl_image( blur )
clip_blurred.write_videofile("blurred_video.mp4")