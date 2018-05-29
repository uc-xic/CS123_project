from mrjob.job import MRJob
import re

def read_line(line):
    user, friends_str = line.split(':')
    friends = friends_str.split(',')
    return user, friends


class Degree_centrality(MRJob):
    
    def mapper_init(self):

        with open("comm_50.txt", "r") as f:
            self.communities = f.readlines()


    def mapper(self, _, line):

        user, friends = read_line(line)

        if friends != ['private'] and \
           friends != ['notfound'] and \
           friends != ['']:

            for comm in self.communities:

                center, community = comm.split('\t')
                center = center.strip('""')
                community = community.strip('[]\n').split(',')
                n = len(community)

                for member in community:
                    if member == user:

                        friend_ls = []
                        for friend in friends:
                            
                            if friend in community:
                                friend_ls.append(friend)

                        degree_centrality = len(friend_ls) / (n-1)
 
                        yield center, (member, round(degree_centrality, 4))
    

    def reducer(self, center, degree_tuple): 
        degree_dict = {}

        for i in degree_tuple:
            member = i[0]
            centrality = i[1]
            degree_dict[member] = centrality

        most_important = max(degree_dict, key = degree_dict.get)

        yield center, (most_important, degree_dict[most_important])


if __name__ == '__main__':
    Degree_centrality.run()