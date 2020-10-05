import os
import glob


def rindex(input_list, input_value):
    """get the last occurrence of a value in a list

    Args:
        input_list (list): 
        input_value (int):

    Returns:
        [int]: index of last occurrence
    """
    return len(input_list) - input_list[::-1].index(input_value) - 1

def tag_labels(labels_dir, tagged_labels_dir, tagged_dir):
    """[summary]

    Args:
        labels_dir (str): 
        tagged_labels_dir (str):
        tagged_dir (str):
    """
    for frame in glob.glob(os.path.join(tagged_dir, '*')):
            frame_name = frame.split("/")[-1].split(".jpg")[0]
            print(frame_name)
            output_file = labels_dir[:labels_dir.rindex("/")]+"/train.txt"
            file_label = open(f"{output_file}", "w")
            filenames = []
            for classes in glob.glob(os.path.join(tagged_labels_dir, '*')):  
                    filenames.append(classes+"/"+frame_name.replace(".jpeg",".txt"))        
            for filename in filenames:
                    with open(filename) as infile:
                            for line in infile:
                                    file_label.write(line)
                                    file_label.write("\n")
            file_label.close()

if __name__ == "__main__":
    tag_labels(labels_dir = "./data/shopfront/shopfront_tagging", tagged_labels_dir = "./data/shopfront/shopfront_labels", tagged_dir = "./data/shopfront/shopfront_tagging/0")