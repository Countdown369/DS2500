
"""
DS2501 Lab for DS2500
This week: We leverage the power of graphs to build a social network.
Do not attempt this lab unless you have attended Tuesday's lecture or have watched the video.
We can't help you with the lab if you don't understand the basics of Graphs.
"""

from graph import Graph

class SocialNetwork:

    def __init__(self):
        """ Class constructor """
        self.g = Graph()

    def read_network(self, filename):
        """ Read pairs of friends from a file. e.g. 'John,Monica', etc. """
        links = []
        with open(filename, "r", encoding = "utf-8") as infile:
            for line in infile:
                line = line.strip("\n")
                links.append(line)
                
        for pair in links:
            pairs = pair.split(",")
            self.g.add_edge(pairs[0], pairs[1])

    def add_person(self, name):
        """ Add a person to the network without giving them any friends """
        self.g.add_vertex(name)

    def friend(self, name1, name2):
        """ Establish that two people are mutual friends """
        self.g.add_edge(name1, name2)

    def unfriend(self, name1, name2):
        """ Two people are no longer friends """
        pass

    def recommend_friends(self, name):
        """Recommend friends for a particular person. Do this by finding that person’s friends,
        and all of the friends of those friends. Don’t recommend anyone who is already a friend!
        Don’t recommend a person more than once. And definitely don't recommend that a person
        be friends with themselves! """
        
        friends = self.g.__getitem__(name)
        possiblerecs = []
        for friend in friends:
            friends_of_friend = self.g.__getitem__(friend)
            possiblerecs.append(friends_of_friend)
            
        for possiblerec in possiblerecs:
            for friend in possiblerec:
                if friend not in friends and friend != name:
                    return friend
        
    def network_stats(self):
        """Generate some statistics about the network such as the number of users
        and the average number of friends per user.
        Return the stats as an attribute->value dictionary.  """
        
        users = self.g.num_vertices()
        connections = self.g.num_edges()
        avg = (users/ connections) * 2
        
        stats = {"Number of Users": users, "Connections": connections,
                 "Average Number of Friends per User": avg}
        
        return stats

    def __repr__(self):
        """ Output the network as a string for printing """
        return self.g.__repr__()


def main():
    net = SocialNetwork()
    net.read_network('friends.txt')

    print("The social network")
    print(net)

    print("Network statistics")
    print(net.network_stats())

    print("Friend recommendations for Monica")
    print(net.recommend_friends('Monica'))

    # net.unfriend('Monica', 'John') # extra credit

    # print("\nFriend recommendations for Monica after unfriending John") # extra credit
    # print(net.recommend_friends('Monica'))


if __name__ == '__main__':
    main()
