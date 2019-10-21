class Settings():
    def __init__(self):
        self.white = (136, 219, 236)
        self.grey = (93, 117, 129)
        self.brown = (58, 3, 12)
        self.blue = (136, 219, 236)
        self.w = 1024  # 32 tiles
        self.h = 704  # 24

        self.title = "Buzzing Bees"
        self.BGColor = self.white

        self.tileSize = 32

        """  FOR BEE LEVEL  """
        self.beeSpeed = 5
        self.upBeeSpeed = 5

        self.beeFalling = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3,
                              3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                              5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
                              5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
                              6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                              7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]


        self.honeyCount = 0
        self.totalHoney = 0
        self.levelHoney = 0

        self.timePassed = 60

        self.honeyDone = False
        self.newLoad = False
        self.imageCount = 0
        self.slowImage = 0
        self.image = 'images/loadingBar/'
        self.load = [(self.image + "loadOne.png"), (self.image + "loadTwo.png"), (self.image + "loadThree.png"),
                     (self.image + "loadFour.png")]

        self.image2 = 'images/forwardFlower/'
        self.imageCount2 = 0
        self.slowImage2 = 0
        self.movingFlower = [(self.image2 + "movingFlower1.png"), (self.image2 + "movingFlower2.png"),
                             (self.image2 + "movingFlower3.png"), (self.image2 + "movingFlower4.png"),
                             (self.image2 + "movingFlower5.png"), (self.image2 + "movingFlower6.png"),
                             (self.image2 + "movingFlower7.png")]

        self.rainSpeed = 5

        """  FOR WORM LEVEL  """

        self.wormSpeed = 32
        self.birdSpeed = 3
        
