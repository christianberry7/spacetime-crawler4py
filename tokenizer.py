class Tokenizer:
    
    final_dict = dict()
    max_count = 0

    def Tokenize(self, input_list):
        token_dict = dict()
        word_count = 0

        for word in input_list:

            word_count += 1

            word = word.lower().strip("!@#$%^&*(),-_=+./:;''\\][`")

            if token_dict.get(word) == None :
                token_dict[word] = 1
            else:
                token_dict[word] += 1

            if self.final_dict.get(word) == None:
                self.final_dict[word] = 1
            else:
                self.final_dict[word] += 1

        if word_count > self.max_count:
            self.max_count = word_count

    def Similarity(self,list1, list2):
        finalList = []
        for x in list1:
            for y in list2:
                if x == y:
                    finalList.append(x)
        return finalList == list1

    def Max_count(self):
        return self.max_count

    def Final_dict(self):
        return self.final_dict

           

        

