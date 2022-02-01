# HANDLES MOVIES LIST

class MovieHandler:
    movies = []
    id = 0

    def __init__(self, id):
        self.id = id
        try:
            open("Movies/MOV" + str(self.id) + ".txt", "x")
        except:
            pass

    def get_movies(self):
        movLs = []
        moviesFile = open("Movies/MOV" + str(self.id) + ".txt", "r")
        for line in moviesFile:
            movLs.append(line)
        moviesFile.close()
        movLs.sort()
        self.movies = movLs

    def moviesToString(self):
        outFl = ""
        for l in self.movies:
            outFl += l
        return outFl

    def moviesToOrderedString(self):
        outFl = ""
        for i in range(len(self.movies)):
            outFl += "[" + str(i) + "] " + self.movies[i]
        return outFl

    def add_movie(self, name):
        self.get_movies()
        self.movies.append(name + "\n")
        self.movies.sort()
        self.save_movies()

    def del_movie(self, index):
        self.get_movies()
        name = self.movies[index]
        del self.movies[index]
        self.save_movies()
        return name

    def save_movies(self):
        with open("Movies/MOV" + str(self.id) + ".txt", 'w') as file:
            file.write(self.moviesToString())
        file.close()
