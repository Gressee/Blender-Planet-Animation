# Generate the video of a point flying along the path
def create_images(points):
    global room_width
    global room_height

    color = [255, 0, 0]

    # Create all frames
    total_points = len(points)
    raw_img = np.zeros((room_height,room_width,3), dtype=np.uint8)
    index = 0
    for point in points:
        index += 1

        img = raw_img # HERE IS ERROR!!!! See:  https://www.geeksforgeeks.org/array-copying-in-python/
        img = draw.circle(img, point[0], point[1], 8, [255, 0, 125])
        img = Image.fromarray(img)
        #img = img.filter(ImageFilter.BoxBlur(4))
        image_name = 'img_' + str(index).rjust(5, '0') + '.png'
        img.save('images/' + image_name)

        print('Processed images: ' + str(index) + '/' + str(total_points), '\r')


# Make video from all the frames
def create_video():

    print('Making Video...')

    fps = 30
    image_folder = 'images/'
    video_name = 'video.avi'

    frame_array = []
    files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]

    files.sort(key = lambda x: int(x[5:-4]))

    # Adding files t the frame_array
    for i in range(len(files)):
        filename = image_folder + files[i]

        # Reading each file
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)

        # Inserting the frames into an image array
        frame_array.append(img)

    # Create video writer
    video = cv2.VideoWriter('out_video.avi', cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

    # Write frame to video
    for i in range(len(frame_array)):
        video.write(frame_array[i])

    cv2.destroyAllWindows()
    video.release()

    print('Done!')
    """
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, 0, 1, (width,height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()
    """


# Generate the image for complete path (DEBUG)
def create_path_image(points):
    global room_width
    global room_height

    color = [255, 0, 0]

    # Make the np array
    img = np.zeros((room_height,room_width,3), dtype=np.uint8)

    # Chek points array and color sourounding points
    for x in points:
        try:
            img[x[1]][x[0]] = color

            img[x[1]+1][x[0]] = color
            img[x[1]-1][x[0]] = color
            img[x[1]][x[0]+1] = color
            img[x[1]][x[0]-1] = color
        except:
            #print('Array index error')
            pass

    # Save the image
    img = Image.fromarray(img)
    img.save('test_img.png')
